#!/usr/bin/env python3
"""
Agent Memory Manager v3.1 - Lightweight memory for AI agents.

v3.1 Features:
- String TTL format ("7d", "1h", "30m", "2w")
- Encryption support (Fernet AES via PBKDF2HMAC key derivation)
- Redis write-through TTL cache (not a primary backend; local storage is authoritative)
- Storage backends: JSON (default), SQLite, FAISS
"""
import json
import os
import uuid
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
# Try to import optional dependencies
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO_KDF = True
except ImportError:
    HAS_CRYPTO_KDF = False


# Sentinel for unset parameters
_UNSET = object()


def parse_ttl(ttl_str: Optional[str]) -> Optional[float]:
    """
    Parse TTL string format to days (float).
    
    Supported formats:
        - "30s"  -> 30 seconds  = 0.00035 days
        - "5m"   -> 5 minutes   = 0.0035 days
        - "1h"   -> 1 hour      = 0.0417 days
        - "1d"   -> 1 day       = 1.0 days
        - "7d"   -> 7 days      = 7.0 days
        - "2w"   -> 2 weeks     = 14.0 days
    
    Args:
        ttl_str: TTL string like "7d", "1h", "30m", "2w"
    
    Returns:
        TTL in days as float, or None if ttl_str is None/invalid
    
    Examples:
        >>> parse_ttl("7d")
        7.0
        >>> parse_ttl("1h")
        0.0417
        >>> parse_ttl("30m")
        0.0208
        >>> parse_ttl("2w")
        14.0
    """
    if ttl_str is None:
        return None
    
    if isinstance(ttl_str, (int, float)):
        return float(ttl_str)
    
    ttl_str = str(ttl_str).strip().lower()
    
    if ttl_str.endswith("s"):
        return float(ttl_str[:-1]) / 86400
    elif ttl_str.endswith("m") and not ttl_str.endswith("am") and not ttl_str.endswith("pm"):
        return float(ttl_str[:-1]) / 1440
    elif ttl_str.endswith("h"):
        return float(ttl_str[:-1]) / 24
    elif ttl_str.endswith("d"):
        return float(ttl_str[:-1])
    elif ttl_str.endswith("w"):
        return float(ttl_str[:-1]) * 7
    else:
        # Plain number: treat as days
        return float(ttl_str)


class Memory:
    """Lightweight memory manager for AI agents."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json", 
                 vector_dim: int = 512, ttl: Optional[str] = None,
                 encryption_key: Optional[str] = None,
                 redis_url: Optional[str] = None):
        self.storage = storage
        self.path = path
        self.vector_dim = vector_dim
        self.ttl_days = parse_ttl(ttl) if ttl else None
        self.encryption_key = encryption_key
        self.redis_url = redis_url
        self._cipher = None
        self.memories: List[Dict] = []
        
        # Encryption setup
        if encryption_key and HAS_CRYPTO:
            import base64
            try:
                # Try as base64-encoded key first
                self._cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
            except Exception:
                # Derive a valid Fernet key from a password string using PBKDF2
                if not HAS_CRYPTO_KDF:
                    import warnings
                    warnings.warn("cryptography kdf not available. Using simple key derivation.")
                    # Simple fallback: hash the key to 32 bytes
                    import hashlib
                    h = hashlib.sha256((encryption_key if isinstance(encryption_key, str) else encryption_key.decode()).encode()).digest()
                    self._cipher = Fernet(base64.urlsafe_b64encode(h))
                else:
                    password = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
                    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'agent_memory_v3_salt', iterations=100000, backend=default_backend())
                    derived_key = kdf.derive(password)
                    fernet_key = base64.urlsafe_b64encode(derived_key)
                    self._cipher = Fernet(fernet_key)
        elif encryption_key and not HAS_CRYPTO:
            import warnings
            warnings.warn("cryptography library not installed. Encryption unavailable. Run: pip install cryptography")
        
        # Redis setup
        self._redis = None
        if redis_url and HAS_REDIS:
            try:
                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
            except Exception as e:
                import warnings
                warnings.warn(f"Redis connection failed: {e}. Falling back to local storage.")
                self._redis = None
        elif redis_url and not HAS_REDIS:
            import warnings
            warnings.warn("redis library not installed. Redis unavailable. Run: pip install redis")
        
        # TF-IDF based
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(max_features=vector_dim)
            self.tfidf_matrix = None
        
        # FAISS index
        if storage == "faiss" and HAS_FAISS:
            self.index = faiss.IndexFlatL2(vector_dim)
        else:
            self.index = None
        
        # SQLite backend
        if storage == "sqlite":
            self.db_path = self.path.replace('.json', '.db')
            self._init_sqlite()
            self._load_sqlite()
        elif storage == "redis" and self._redis:
            self._load_redis()
        elif storage == "json" and os.path.exists(path):
            self._load()
    
    def _init_sqlite(self):
        """Initialize SQLite database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT,
                priority INTEGER DEFAULT 0,
                metadata TEXT,
                expires_at TEXT
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_expires ON memories(expires_at)")
        self.conn.commit()
    
    def _load_sqlite(self):
        """Load memories from SQLite."""
        cursor = self.conn.execute(
            "SELECT id, text, timestamp, tags, priority, metadata, expires_at FROM memories WHERE expires_at IS NULL OR expires_at > ?",
            (datetime.now().isoformat(),)
        )
        self.memories = []
        for row in cursor.fetchall():
            m = {
                "id": row[0],
                "text": row[1],
                "timestamp": row[2],
                "tags": json.loads(row[3]) if row[3] else [],
                "priority": row[4] or 0,
                "metadata": json.loads(row[5]) if row[5] else {}
            }
            if row[6]:
                m["expires_at"] = row[6]
            self.memories.append(m)
        # Prune any records that expired between last save and now (race window)
        self.memories = [m for m in self.memories if not self._is_expired(m)]
    
    def _save_sqlite(self):
        """Save memories to SQLite."""
        for m in self.memories:
            # Use the per-record expires_at already set by add(); do not recalculate.
            expires_at = m.get("expires_at")
            self.conn.execute("""
                INSERT OR REPLACE INTO memories (id, text, timestamp, tags, priority, metadata, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (m["id"], m["text"], m["timestamp"], json.dumps(m.get("tags", [])),
                  m.get("priority", 0), json.dumps(m.get("metadata", {})), expires_at))
        self.conn.commit()
    
    def _load(self):
        """Load memories from file, pruning any expired records."""
        with open(self.path, 'r') as f:
            self.memories = json.load(f)
        self._prune_expired()
    
    def _save(self):
        """Save memories to file, SQLite, or Redis."""
        if self.storage == "sqlite":
            self._save_sqlite()
        elif self.storage == "redis" and self._redis:
            self._save_redis()
        else:
            with open(self.path, 'w') as f:
                json.dump(self.memories, f, indent=2)
    
    def _save_redis(self):
        """Save all memories to Redis."""
        if not self._redis:
            return
        pipe = self._redis.pipeline()
        for m in self.memories:
            key = f"memory:{m['id']}"
            ttl_seconds = None
            if m.get("expires_at"):
                expiry = datetime.fromisoformat(m["expires_at"])
                ttl_seconds = int((expiry - datetime.now()).total_seconds())
                if ttl_seconds <= 0:
                    continue  # Skip expired
            pipe.set(key, json.dumps(m), ex=ttl_seconds)
        pipe.execute()
    
    def _load_redis(self):
        """Load all memories from Redis."""
        if not self._redis:
            return
        keys = self._redis.keys("memory:*")
        self.memories = []
        for key in keys:
            data = self._redis.get(key)
            if data:
                m = json.loads(data)
                if not self._is_expired(m):
                    self.memories.append(m)
    
    def _is_expired(self, m: Dict) -> bool:
        """Return True if memory record m has passed its expiry time."""
        expires_at = m.get("expires_at")
        if not expires_at:
            return False
        return datetime.fromisoformat(expires_at) <= datetime.now()

    def _active_memories(self) -> List[Dict]:
        """Return only non-expired records from self.memories."""
        return [m for m in self.memories if not self._is_expired(m)]

    def _prune_expired(self):
        """Remove expired records from self.memories and persist. Call at load time."""
        before = len(self.memories)
        self.memories = self._active_memories()
        if len(self.memories) < before:
            self._save()

    def add(self, text: str, metadata: Optional[Dict] = None, ttl: object = _UNSET, 
            encrypt: bool = False) -> str:
        """Add a new memory with optional TTL and encryption.
        
        Args:
            text: Memory content text
            metadata: Optional metadata dict
            ttl: Optional TTL string (e.g., "7d", "1h", "30m", "2w"). 
                 Pass ttl=None to explicitly disable TTL even if Memory has default.
            encrypt: If True, encrypt the text before storing
        
        Returns:
            Memory ID string
        
        Examples:
            >>> m = Memory()
            >>> m.add("session data", ttl="1h")
            >>> m.add("api key", encrypt=True)
            >>> m.add("permanent note", ttl=None)  # explicitly no TTL
        """
        memory_id = str(uuid.uuid4())[:8]
        
        # Determine effective TTL: explicit None = disable, unset = use default
        if ttl is _UNSET:
            effective_ttl_days = self.ttl_days
        else:
            effective_ttl_days = parse_ttl(ttl) if ttl is not None else None
        
        metadata = metadata or {}
        
        # Encrypt text if requested
        stored_text = text
        if encrypt or metadata.get("encrypt"):
            if self._cipher:
                stored_text = self._cipher.encrypt(text.encode()).decode()
                metadata["encrypted"] = True
            else:
                import warnings
                warnings.warn("Encryption requested but no key configured. Storing plaintext.")
        
        memory = {
            "id": memory_id,
            "text": stored_text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "priority": metadata.get("priority", 0),
            "tags": metadata.get("tags", [])
        }
        
        if effective_ttl_days:
            memory["expires_at"] = (datetime.now() + timedelta(days=effective_ttl_days)).isoformat()
        
        # Store in Redis if available
        if self._redis:
            import json as _json
            ttl_seconds = int(effective_ttl_days * 86400) if effective_ttl_days else 86400 * 30
            redis_data = {"id": memory_id, "text": stored_text, "timestamp": memory["timestamp"], "metadata": metadata}
            if effective_ttl_days:
                redis_data["expires_at"] = memory["expires_at"]
            self._redis.setex(f"memory:{memory_id}", ttl_seconds, _json.dumps(redis_data))
        
        self.memories.append(memory)
        self._save()
        return memory_id
    
    def get(self, memory_id: str) -> Optional[Dict]:
        """Retrieve a memory by ID, decrypting if needed. Checks Redis for Redis backend."""
        # First try local list
        for m in self.memories:
            if m["id"] == memory_id:
                expires_at = m.get("expires_at")
                if expires_at and datetime.fromisoformat(expires_at) <= datetime.now():
                    return None
                result = m.copy()
                # Decrypt if needed
                if result.get("metadata", {}).get("encrypted") and self._cipher:
                    result["text"] = self._cipher.decrypt(result["text"].encode()).decode()
                return result
        # Fallback: check Redis directly
        if self._redis:
            import json as _json
            data = self._redis.get(f"memory:{memory_id}")
            if data:
                m = _json.loads(data)
                if not self._is_expired(m):
                    result = m.copy()
                    if result.get("metadata", {}).get("encrypted") and self._cipher:
                        result["text"] = self._cipher.decrypt(result["text"].encode()).decode()
                    return result
        return None
    
    def ttl_remaining(self, memory_id: str) -> Optional[float]:
        """Get remaining TTL in seconds for a memory, or None if no expiry."""
        # Check Redis first
        if self._redis:
            ttl = self._redis.ttl(f"memory:{memory_id}")
            if ttl > 0:
                return float(ttl)
            return None
        # Fallback to local list
        for m in self.memories:
            if m["id"] == memory_id:
                expires_at = m.get("expires_at")
                if not expires_at:
                    return None
                expiry = datetime.fromisoformat(expires_at)
                remaining = (expiry - datetime.now()).total_seconds()
                return max(0.0, remaining)
        return None
        return None
    
    def add_batch(self, texts: List[str], metadata: Optional[Dict] = None) -> List[str]:
        """Add multiple memories at once."""
        ids = []
        for text in texts:
            memory_id = self.add(text, metadata)
            ids.append(memory_id)
        return ids
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search memories by similarity."""
        active = self._active_memories()
        if not active:
            return []
        
        if HAS_SKLEARN:
            texts = [m["text"] for m in active]
            try:
                tfidf_matrix = self.vectorizer.fit_transform(texts + [query])
                query_vec = tfidf_matrix[-1]
                memory_vecs = tfidf_matrix[:-1]
                similarities = cosine_similarity(query_vec, memory_vecs)[0]
                if HAS_NUMPY:
                    top_indices = np.argsort(similarities)[-top_k:][::-1]
                else:
                    indexed_sims = list(enumerate(similarities))
                    indexed_sims.sort(key=lambda x: x[1], reverse=True)
                    top_indices = [x[0] for x in indexed_sims[:top_k]]
                
                results = []
                for idx in top_indices:
                    if similarities[idx] > 0:
                        result = active[idx].copy()
                        result["score"] = float(similarities[idx])
                        results.append(result)
                return results
            except ValueError:
                pass
        
        # Fallback: return recent active memories
        return active[:top_k]
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent non-expired memories."""
        sorted_memories = sorted(
            self._active_memories(),
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        return sorted_memories[:limit]
    
    def get_context(self, max_tokens: int = 2000, max_memories: int = 10) -> str:
        """Get condensed context for agent."""
        active = self._active_memories()
        if not active:
            return ""
        
        sorted_memories = sorted(
            active,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        
        context_parts = []
        total_chars = 0
        
        for memory in sorted_memories[:max_memories]:
            text = memory["text"]
            if total_chars + len(text) > max_tokens * 4:
                break
            context_parts.append(f"- {text}")
            total_chars += len(text)
        
        if not context_parts:
            return ""
        
        return "Relevant memories:\n" + "\n".join(context_parts)
    
    def summarize(self) -> str:
        """Generate a summary of all memories."""
        if not self.memories:
            return "No memories stored."
        
        count = len(self.memories)
        recent = self.get_recent(3)
        
        summary = f"Total memories: {count}\n\nRecent memories:\n"
        for m in recent:
            summary += f"- {m['text'][:100]}...\n"
        
        return summary
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory by ID from local storage and Redis cache."""
        for i, m in enumerate(self.memories):
            if m["id"] == memory_id:
                del self.memories[i]
                self._save()
                if self._redis:
                    try:
                        self._redis.delete(f"memory:{memory_id}")
                    except Exception:
                        pass
                return True
        return False
    
    def clear(self):
        """Clear all memories from RAM and persistent storage."""
        self.memories = []
        if self.storage == "sqlite":
            self.conn.execute("DELETE FROM memories")
            self.conn.commit()
        elif self.storage == "redis" and self._redis:
            keys = self._redis.keys("memory:*")
            if keys:
                self._redis.delete(*keys)
        else:
            self._save()
    
    def count(self) -> int:
        """Get number of non-expired memories."""
        return len(self._active_memories())
    
    def export(self, filepath: str):
        """Export memories to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def export_markdown(self, filepath: str):
        """Export memories to a Markdown file."""
        with open(filepath, 'w') as f:
            f.write("# Agent Memory Export\n\n")
            for m in self.memories:
                f.write(f"## {m['id']} - {m['timestamp']}\n\n")
                f.write(f"{m['text']}\n\n")
                if m.get('tags'):
                    f.write(f"**Tags:** {', '.join(m['tags'])}\n\n")
                f.write("---\n\n")
    
    def add_with_tags(self, text: str, tags: List[str], metadata: Optional[Dict] = None,
                      ttl: object = _UNSET, encrypt: bool = False) -> str:
        """Add a memory with tags. Delegates to add() so TTL and encryption apply."""
        meta = dict(metadata or {})
        meta["tags"] = tags
        return self.add(text, metadata=meta, ttl=ttl, encrypt=encrypt)
    
    def get_by_tag(self, tag: str) -> List[Dict]:
        """Get non-expired memories by tag."""
        return [m for m in self._active_memories() if tag in m.get('tags', [])]
    
    def import_(self, filepath: str):
        """Import memories from a file."""
        with open(filepath, 'r') as f:
            self.memories = json.load(f)
        self._save()
    
    def set_priority(self, memory_id: str, priority: int) -> bool:
        """Set memory priority (1-5)."""
        for m in self.memories:
            if m["id"] == memory_id:
                m["priority"] = priority
                self._save()
                return True
        return False
    
    def get_by_priority(self, min_priority: int = 3) -> List[Dict]:
        """Get non-expired memories by minimum priority."""
        return [m for m in self._active_memories() if m.get("priority", 0) >= min_priority]
    
    def merge(self, other_memories: List[Dict]):
        """Merge memories from another source (avoid duplicates)."""
        existing_ids = set(m["id"] for m in self.memories)
        for m in other_memories:
            if m["id"] not in existing_ids:
                self.memories.append(m)
        self._save()
    
    def get_timeline(self, limit: int = 20) -> List[Dict]:
        """Get non-expired memories as a timeline."""
        sorted_memories = sorted(self._active_memories(),
                                 key=lambda x: x.get("timestamp", ""),
                                 reverse=True)
        return sorted_memories[:limit]


# CLI interface
def main():
    """Entry point for the agent-memory CLI (agent-memory command)."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Memory CLI v3.1")
    parser.add_argument("command", choices=["add", "search", "clear", "context", "recent", "summarize", "delete", "stats", "tags", "by-tag", "by-priority", "export", "import", "timeline"])
    parser.add_argument("--text", help="Text for add/search")
    parser.add_argument("--path", default="./memory.json", help="Memory file path")
    parser.add_argument("--top-k", type=int, default=5, help="Top K results")
    parser.add_argument("--storage", default="json", choices=["json", "faiss", "sqlite"], help="Storage backend")
    parser.add_argument("--ttl", help="Default TTL for memories, e.g. '7d', '1h', '30m'")
    parser.add_argument("--encryption-key", help="Encryption key (string password or base64 Fernet key)")
    parser.add_argument("--redis-url", help="Redis URL for write-through cache, e.g. redis://localhost:6379")
    parser.add_argument("--id", help="Memory ID for delete")
    parser.add_argument("--tag", help="Tag for by-tag command")
    parser.add_argument("--priority", type=int, help="Priority for by-priority command")
    parser.add_argument("--file", help="File for export/import")
    parser.add_argument("--format", default="json", choices=["json", "markdown"], help="Export format")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt this entry (requires --encryption-key)")
    
    args = parser.parse_args()
    memory = Memory(
        storage=args.storage,
        path=args.path,
        ttl=args.ttl,
        encryption_key=args.encryption_key,
        redis_url=args.redis_url,
    )
    
    if args.command == "add":
        if not args.text:
            print("Error: --text required for add")
            exit(1)
        memory_id = memory.add(args.text, encrypt=getattr(args, "encrypt", False))
        print(f"Added memory: {memory_id}")
    
    elif args.command == "search":
        if not args.text:
            print("Error: --text required for search")
            exit(1)
        results = memory.search(args.text, args.top_k)
        for r in results:
            score = r.get("score", 0)
            print(f"[{score:.2f}] {r['text'][:80]}...")
    
    elif args.command == "clear":
        memory.clear()
        print("Memory cleared")
    
    elif args.command == "context":
        ctx = memory.get_context()
        print(ctx or "(no context)")
    
    elif args.command == "recent":
        recent = memory.get_recent(args.top_k)
        for r in recent:
            print(f"- {r['text'][:80]}...")
    
    elif args.command == "summarize":
        print(memory.summarize())
    
    elif args.command == "delete":
        if args.id:
            if memory.delete(args.id):
                print(f"Deleted memory: {args.id}")
            else:
                print(f"Memory not found: {args.id}")
        else:
            print("Error: --id required for delete")
    
    elif args.command == "stats":
        print(f"Total memories: {memory.count()}")
        all_tags = set()
        priorities = []
        for m in memory.memories:
            if m.get('tags'):
                all_tags.update(m['tags'])
            if m.get('priority'):
                priorities.append(m['priority'])
        print(f"Unique tags: {len(all_tags)}")
        if priorities:
            print(f"Average priority: {sum(priorities)/len(priorities):.2f}")
    
    elif args.command == "tags":
        all_tags = set()
        for m in memory.memories:
            if m.get('tags'):
                all_tags.update(m['tags'])
        if all_tags:
            print("Tags:", ", ".join(sorted(all_tags)))
        else:
            print("No tags found")
    
    elif args.command == "by-tag":
        if args.tag:
            results = memory.get_by_tag(args.tag)
            for r in results:
                print(f"- {r['text'][:80]}...")
            print(f"Found {len(results)} memories")
        else:
            print("Error: --tag required for by-tag")
    
    elif args.command == "by-priority":
        priority = args.priority or 3
        results = memory.get_by_priority(priority)
        for r in results:
            print(f"- [{r.get('priority', 0)}] {r['text'][:80]}...")
        print(f"Found {len(results)} memories")
    
    elif args.command == "export":
        filepath = args.file or "memory_export.json"
        if args.format == "markdown":
            memory.export_markdown(filepath.replace(".json", ".md"))
            print(f"Exported to {filepath.replace('.json', '.md')}")
        else:
            memory.export(filepath)
            print(f"Exported to {filepath}")
    
    elif args.command == "import":
        if args.file:
            memory.import_(args.file)
            print(f"Imported from {args.file}")
        else:
            print("Error: --file required for import")
    
    elif args.command == "timeline":
        timeline = memory.get_timeline(args.top_k)
        for t in timeline:
            print(f"[{t['timestamp'][:16]}] {t['text'][:60]}...")

if __name__ == "__main__":
    main()
