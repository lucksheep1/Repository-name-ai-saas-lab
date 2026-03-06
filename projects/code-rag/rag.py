#!/usr/bin/env python3
"""
Local Code RAG CLI v2
Lightweight code search using TF-IDF with enhanced features.
"""
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
import subprocess

# Try optional dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class CodeRAG:
    """Local code RAG engine."""
    
    def __init__(self, index_path: str = ".code-rag.json"):
        self.index_path = index_path
        self.files: List[Dict] = []
        
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words=None,
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = None
        
        if os.path.exists(index_path):
            self._load()
    
    def _load(self):
        """Load index from file."""
        with open(self.index_path, 'r') as f:
            data = json.load(f)
            self.files = data.get('files', [])
    
    def _save(self):
        """Save index to file."""
        with open(self.index_path, 'w') as f:
            json.dump({'files': self.files}, f)
    
    def _extract_functions(self, content: str, language: str) -> List[str]:
        """Extract function/method definitions."""
        patterns = {
            'py': r'def\s+(\w+)\s*\([^)]*\):',
            'js': r'function\s+(\w+)\s*\([^)]*\)|const\s+(\w+)\s*=\s*\([^)]*\)',
            'ts': r'function\s+(\w+)\s*\([^)]*\)|const\s+(\w+)\s*=',
            'go': r'func\s+(\w+)\s*\([^)]*\)',
            'rs': r'fn\s+(\w+)\s*\([^)]*\)',
            'java': r'(public|private|protected)\s+\w+\s+(\w+)\s*\([^)]*\)',
        }
        
        pattern = patterns.get(language, r'')
        if not pattern:
            return []
        
        matches = re.findall(pattern, content)
        return [m[0] if isinstance(m, tuple) else m for m in matches]
    
    def _extract_classes(self, content: str, language: str) -> List[str]:
        """Extract class definitions."""
        patterns = {
            'py': r'class\s+(\w+)',
            'js': r'class\s+(\w+)',
            'ts': r'class\s+(\w+)',
            'java': r'class\s+(\w+)',
        }
        
        pattern = patterns.get(language, r'')
        if not pattern:
            return []
        
        return re.findall(pattern, content)
    
    def _extract_code_blocks(self, content: str, max_lines: int = 100) -> List[str]:
        """Extract meaningful code blocks."""
        blocks = []
        lines = content.split('\n')
        
        current_block = []
        
        for line in lines[:max_lines]:
            stripped = line.strip()
            
            if not stripped:
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                continue
            
            if stripped.startswith('#') or stripped.startswith('//'):
                continue
            
            current_block.append(line)
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def index_directory(self, path: str, extensions: List[str] = None) -> Dict:
        """Index a directory with detailed info."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp', '.c', '.h']
        
        path_obj = Path(path)
        self.files = []
        
        stats = {"files": 0, "functions": 0, "classes": 0, "blocks": 0}
        
        for ext in extensions:
            for filepath in path_obj.rglob(f'*{ext}'):
                if any(x in filepath.parts for x in ['node_modules', '.git', 'venv', '__pycache__', 'dist', 'build']):
                    continue
                
                try:
                    if filepath.stat().st_size > 1_000_000:
                        continue
                    
                    content = filepath.read_text(errors='ignore')
                    language = ext[1:]
                    
                    # Extract functions and classes
                    functions = self._extract_functions(content, language)
                    classes = self._extract_classes(content, language)
                    
                    blocks = self._extract_code_blocks(content)
                    
                    for i, block in enumerate(blocks):
                        if len(block.strip()) < 20:
                            continue
                        
                        self.files.append({
                            'path': str(filepath),
                            'block_id': i,
                            'content': block,
                            'language': language,
                            'functions': functions,
                            'classes': classes
                        })
                        
                        stats["blocks"] += 1
                    
                    stats["files"] += 1
                    stats["functions"] += len(functions)
                    stats["classes"] += len(classes)
                
                except Exception:
                    continue
        
        if self.files and HAS_SKLEARN:
            texts = [f['content'] for f in self.files]
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        self._save()
        return stats
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search the indexed code."""
        if not self.files:
            return []
        
        if HAS_SKLEARN and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([query])
                similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
                top_indices = np.argsort(similarities)[-top_k:][::-1]
                
                results = []
                for idx in top_indices:
                    if similarities[idx] > 0.05:
                        result = self.files[idx].copy()
                        result["score"] = float(similarities[idx])
                        results.append(result)
                return results
            except Exception:
                pass
        
        return self.files[:top_k]
    
    def search_function(self, name: str) -> List[Dict]:
        """Search for a specific function."""
        results = []
        for f in self.files:
            if name in f.get('functions', []):
                results.append(f)
        return results[:10]
    
    def search_class(self, name: str) -> List[Dict]:
        """Search for a specific class."""
        results = []
        for f in self.files:
            if name in f.get('classes', []):
                results.append(f)
        return results[:10]
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        return {
            "total_blocks": len(self.files),
            "languages": list(set(f.get('language', '') for f in self.files)),
            "files": len(set(f.get('path', '') for f in self.files))
        }
    
    def export_markdown(self, output_path: str = "code-rag-export.md"):
        """Export index to Markdown file."""
        with open(output_path, 'w') as f:
            f.write("# Code RAG Export\n\n")
            
            # Group by file
            by_file = {}
            for block in self.files:
                path = block.get('path', 'unknown')
                if path not in by_file:
                    by_file[path] = []
                by_file[path].append(block)
            
            for path, blocks in by_file.items():
                f.write(f"## {path}\n\n")
                for block in blocks:
                    funcs = block.get('functions', [])
                    classes = block.get('classes', [])
                    
                    if funcs:
                        f.write(f"**Functions:** {', '.join(funcs)}\n\n")
                    if classes:
                        f.write(f"**Classes:** {', '.join(classes)}\n\n")
                    
                    f.write("```" + block.get('language', '') + "\n")
                    f.write(block.get('content', '')[:500])
                    f.write("\n```\n\n")
                    f.write("---\n\n")
        
        return output_path
    
    def find_related(self, query: str, max_results: int = 10) -> List[Dict]:
        """Find related code blocks across the codebase."""
        results = self.search(query, top_k=max_results)
        
        # Also find by function/class names
        func_results = self.search_function(query)
        class_results = self.search_class(query)
        
        # Combine and dedupe
        seen = set()
        combined = []
        
        for r in results + func_results + class_results:
            key = (r.get('path'), r.get('block_id'))
            if key not in seen:
                seen.add(key)
                combined.append(r)
        
        return combined[:max_results]
    
    def find_imports(self, path: str) -> List[str]:
        """Find imports in a file."""
        try:
            content = Path(path).read_text()
        except Exception:
            return []
        
        imports = []
        
        # Python
        if path.endswith('.py'):
            imports.extend(re.findall(r'^import\s+(\S+)', content, re.MULTILINE))
            imports.extend(re.findall(r'^from\s+(\S+)\s+import', content, re.MULTILINE))
        
        # JavaScript/TypeScript
        elif path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            imports.extend(re.findall(r"import\s+.*\s+from\s+['\"]([^'\"]+)['\"]", content))
            imports.extend(re.findall(r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content))
        
        return list(set(imports))


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Local Code RAG CLI v2')
    subparsers = parser.add_subparsers()
    
    index_parser = subparsers.add_parser('index', help='Index a directory')
    index_parser.add_argument('path', help='Directory to index')
    index_parser.add_argument('--extensions', nargs='+', 
                             default=['.py', '.js', '.ts', '.go', '.rs'],
                             help='File extensions')
    
    search_parser = subparsers.add_parser('search', help='Search code')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--top-k', type=int, default=5)
    
    func_parser = subparsers.add_parser('function', help='Search function')
    func_parser.add_argument('name', help='Function name')
    
    class_parser = subparsers.add_parser('class', help='Search class')
    class_parser.add_argument('name', help='Class name')
    
    stats_parser = subparsers.add_parser('stats', help='Show index stats')
    
    args = parser.parse_args()
    
    rag = CodeRAG()
    
    if hasattr(args, 'path'):
        print(f"Indexing {args.path}...")
        stats = rag.index_directory(args.path, args.extensions)
        print(f"Indexed: {stats['files']} files, {stats['functions']} functions, {stats['classes']} classes")
    
    elif hasattr(args, 'query'):
        results = rag.search(args.query, args.top_k)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['path']}:{r['block_id']} ({r['language']})")
            print(f"   Score: {r.get('score', 0):.3f}")
            print(f"   {r['content'][:100]}...")
    
    elif hasattr(args, 'name') and hasattr(args, 'path') == False:
        # Could be function or class search
        pass
    
    elif hasattr(args, 'name') == False:
        # stats
        print(rag.get_stats())


if __name__ == '__main__':
    main()
