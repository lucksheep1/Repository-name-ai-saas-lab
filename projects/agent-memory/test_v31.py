#!/usr/bin/env python3
"""
v3.1 feature tests for agent_memory.py
Tests: parse_ttl, encrypt/decrypt round-trip, TTL expiry, SQLite persistence,
       sentinel _UNSET vs None, Redis graceful fallback.
"""
import sys, os, time, json, tempfile, shutil
sys.path.insert(0, os.path.dirname(__file__))

from agent_memory import parse_ttl, Memory, _UNSET, HAS_CRYPTO, HAS_REDIS

PASS = 0
FAIL = 0

def ok(name):
    global PASS
    PASS += 1
    print(f"  PASS  {name}")

def fail(name, detail=""):
    global FAIL
    FAIL += 1
    print(f"  FAIL  {name}" + (f": {detail}" if detail else ""))

# ── parse_ttl ────────────────────────────────────────────────────────────────
print("\n=== parse_ttl ===")

cases = [
    ("7d",  7.0),
    ("1d",  1.0),
    ("2w",  14.0),
    ("1h",  1/24),
    ("30m", 30/1440),
    ("60s", 60/86400),
    ("3",   3.0),
    (3,     3.0),
    (None,  None),
]
for arg, expected in cases:
    got = parse_ttl(arg)
    if got is None and expected is None:
        ok(f"parse_ttl({arg!r}) == None")
    elif got is not None and expected is not None and abs(got - expected) < 1e-9:
        ok(f"parse_ttl({arg!r}) ≈ {expected}")
    else:
        fail(f"parse_ttl({arg!r})", f"expected {expected}, got {got}")

# ── _UNSET sentinel ──────────────────────────────────────────────────────────
print("\n=== sentinel _UNSET ===")

tmpdir = tempfile.mkdtemp()
try:
    path = os.path.join(tmpdir, "mem.json")

    # Memory with default TTL of 7d
    m = Memory(path=path, ttl="7d")
    mid = m.add("test default ttl")
    rec = m.get(mid)
    if rec and rec.get("expires_at") is not None:
        ok("add() with _UNSET uses class default TTL")
    else:
        fail("add() with _UNSET uses class default TTL", f"rec={rec}")

    # Explicit ttl=None disables TTL even when default is set
    mid2 = m.add("no ttl", ttl=None)
    rec2 = m.get(mid2)
    if rec2 and rec2.get("expires_at") is None:
        ok("add(ttl=None) disables TTL despite class default")
    else:
        fail("add(ttl=None) disables TTL despite class default", f"rec2={rec2}")

finally:
    shutil.rmtree(tmpdir)

# ── TTL expiry ───────────────────────────────────────────────────────────────
print("\n=== TTL expiry ===")

tmpdir = tempfile.mkdtemp()
try:
    path = os.path.join(tmpdir, "mem_ttl.json")
    m = Memory(path=path)

    # Add with 1-second TTL (expressed as seconds)
    mid = m.add("expires soon", ttl="1s")
    rec_before = m.get(mid)
    if rec_before is not None:
        ok("entry visible before expiry")
    else:
        fail("entry visible before expiry")

    # Wait 2 seconds
    time.sleep(2)

    rec_after = m.get(mid)
    if rec_after is None:
        ok("entry returns None after TTL expires")
    else:
        fail("entry returns None after TTL expires", f"got {rec_after}")

    # ttl_remaining on expired entry
    rem = m.ttl_remaining(mid)
    if rem is None or rem <= 0:
        ok("ttl_remaining returns None/<=0 on expired entry")
    else:
        fail("ttl_remaining on expired entry", f"got {rem}")

finally:
    shutil.rmtree(tmpdir)

# ── Encrypt / decrypt round-trip ─────────────────────────────────────────────
print("\n=== Encryption ===")

if not HAS_CRYPTO:
    print("  SKIP  cryptography not installed")
else:
    tmpdir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmpdir, "mem_enc.json")
        secret = "hunter2"
        m = Memory(path=path, encryption_key=secret)

        plaintext = "my secret api key"
        mid = m.add(plaintext, encrypt=True)
        rec = m.get(mid)  # get() auto-decrypts

        if rec and rec.get("text") == plaintext:
            ok("encrypt + auto-decrypt round-trip")
        else:
            fail("encrypt + auto-decrypt round-trip", f"got {rec}")

        # Verify stored bytes are NOT the plaintext
        with open(path) as f:
            raw = json.load(f)
        stored_rec = raw[0] if isinstance(raw, list) else list(raw.values())[0]
        stored = stored_rec.get("text", "")
        if stored != plaintext:
            ok("stored ciphertext differs from plaintext")
        else:
            fail("stored ciphertext differs from plaintext", "stored as plaintext!")

        # Encrypted flag set
        if stored_rec.get("metadata", {}).get("encrypted"):
            ok("metadata.encrypted flag set")
        else:
            fail("metadata.encrypted flag set")

    finally:
        shutil.rmtree(tmpdir)

# ── SQLite persistence ───────────────────────────────────────────────────────
print("\n=== SQLite persistence ===")

tmpdir = tempfile.mkdtemp()
try:
    path = os.path.join(tmpdir, "mem.db")
    m = Memory(storage="sqlite", path=path)

    mid = m.add("sqlite entry", metadata={"tag": "test"})
    rec = m.get(mid)
    if rec and rec.get("text") == "sqlite entry":
        ok("SQLite add + get round-trip")
    else:
        fail("SQLite add + get round-trip", f"rec={rec}")

    # Reload from disk to confirm persistence
    m2 = Memory(storage="sqlite", path=path)
    rec2 = m2.get(mid)
    if rec2 and rec2.get("text") == "sqlite entry":
        ok("SQLite data persists across Memory instances")
    else:
        fail("SQLite data persists across Memory instances", f"rec2={rec2}")

finally:
    shutil.rmtree(tmpdir)

# ── Redis graceful fallback ──────────────────────────────────────────────────
print("\n=== Redis graceful fallback ===")

if HAS_REDIS:
    print(f"  INFO  redis module installed (HAS_REDIS=True)")
    # Try connecting to a non-existent Redis; should not raise on import
    tmpdir = tempfile.mkdtemp()
    try:
        path = os.path.join(tmpdir, "mem.json")
        try:
            m = Memory(path=path, redis_url="redis://127.0.0.1:6399")  # bad port
            mid = m.add("fallback test")
            # Should silently fall back or raise — document actual behavior
            rec = m.get(mid)
            ok("Memory() with bad redis_url does not crash on init + add")
        except Exception as e:
            fail("Memory() with bad redis_url does not crash", str(e))
    finally:
        shutil.rmtree(tmpdir)
else:
    print("  INFO  redis not installed (HAS_REDIS=False) — testing import-level fallback")
    # Module imported fine despite missing redis — that's the fallback
    ok("import succeeds with HAS_REDIS=False (graceful fallback)")


# ── Redis live backend ───────────────────────────────────────────────────────
print("\n=== Redis live backend ===")

if not HAS_REDIS:
    print("  SKIP  redis not installed")
else:
    import json as _json, shutil as _shutil
    import redis as _redis_mod
    try:
        r = _redis_mod.from_url("redis://127.0.0.1:6379", decode_responses=True)
        r.ping()
        server_up = True
    except Exception:
        server_up = False

    if not server_up:
        print("  SKIP  redis-server not reachable on 127.0.0.1:6379")
    else:
        tmpdir = tempfile.mkdtemp()
        try:
            path = os.path.join(tmpdir, "mem.json")
            m = Memory(path=path, redis_url="redis://127.0.0.1:6379")
            if m._redis is None:
                fail("Redis connected", "_redis is None")
            else:
                ok("Redis connected")
                mid = m.add("redis live test", ttl="5m")
                key = f"memory:{mid}"
                val = m._redis.get(key)
                if val:
                    data = _json.loads(val)
                    ok("Redis key written after add()")
                    ttl_s = m._redis.ttl(key)
                    if 290 <= ttl_s <= 310:
                        ok(f"Redis TTL set correctly ({ttl_s}s)")
                    else:
                        fail("Redis TTL set correctly", f"got {ttl_s}s")
                else:
                    fail("Redis key written after add()")
                rec = m.get(mid)
                if rec and rec.get("text") == "redis live test":
                    ok("local get() works alongside Redis")
                else:
                    fail("local get() works alongside Redis", f"got {rec}")
        finally:
            _shutil.rmtree(tmpdir)


# ── SQLite per-record TTL persistence (Step 1) ──────────────────────────────
print("\n=== SQLite per-record TTL persistence ===")

tmpdir = tempfile.mkdtemp()
db = os.path.join(tmpdir, "ttl_persist.db")
try:
    m = Memory(storage="sqlite", path=db, ttl="7d")
    mid_short = m.add("short lived", ttl="2s")
    mid_none  = m.add("no ttl",     ttl=None)
    mid_3d    = m.add("3 day",      ttl="3d")

    m2 = Memory(storage="sqlite", path=db, ttl="7d")

    # short: survives reload (not expired yet)
    if m2.get(mid_short) is not None:
        ok("short TTL record present after reload")
    else:
        fail("short TTL record present after reload")

    # explicit None: no expires_at after reload
    rec_none = m2.get(mid_none)
    if rec_none and rec_none.get("expires_at") is None:
        ok("ttl=None record has no expires_at after reload")
    else:
        fail("ttl=None record has no expires_at after reload", f"got {rec_none}")

    # 3d: ~3d remaining, not 7d
    rec_3d = m2.get(mid_3d)
    if rec_3d:
        from datetime import datetime as _dt
        days_left = (_dt.fromisoformat(rec_3d["expires_at"]) - _dt.now()).total_seconds() / 86400
        if 2.9 < days_left < 3.1:
            ok(f"3d per-record TTL preserved after reload ({days_left:.2f}d)")
        else:
            fail("3d per-record TTL preserved after reload", f"got {days_left:.2f}d")
    else:
        fail("3d record missing after reload")

    # Wait for short to expire
    time.sleep(3)
    m3 = Memory(storage="sqlite", path=db, ttl="7d")
    if m3.get(mid_short) is None:
        ok("expired record absent after reload past TTL")
    else:
        fail("expired record absent after reload past TTL")
finally:
    shutil.rmtree(tmpdir)

# ── Expiry filtering in list methods (Step 2) ────────────────────────────────
print("\n=== Expiry filtering in list methods ===")

tmpdir = tempfile.mkdtemp()
path = os.path.join(tmpdir, "list.json")
try:
    m = Memory(path=path)
    mid_exp  = m.add("expires", ttl="1s")
    mid_perm = m.add("permanent", ttl=None)
    time.sleep(2)

    if m.count() == 1:
        ok("count() excludes expired entries")
    else:
        fail("count() excludes expired entries", f"got {m.count()}")

    recent = m.get_recent()
    if len(recent) == 1 and recent[0]["text"] == "permanent":
        ok("get_recent() excludes expired entries")
    else:
        fail("get_recent() excludes expired entries", f"got {recent}")

    timeline = m.get_timeline()
    if len(timeline) == 1:
        ok("get_timeline() excludes expired entries")
    else:
        fail("get_timeline() excludes expired entries", f"got {timeline}")

    ctx = m.get_context()
    if "expires" not in ctx and "permanent" in ctx:
        ok("get_context() excludes expired entries")
    else:
        fail("get_context() excludes expired entries", f"got {ctx!r}")
finally:
    shutil.rmtree(tmpdir)

# ── clear() for SQLite (Step 3) ──────────────────────────────────────────────
print("\n=== clear() for SQLite ===")

tmpdir = tempfile.mkdtemp()
db = os.path.join(tmpdir, "clear.db")
try:
    m = Memory(storage="sqlite", path=db)
    m.add("entry 1")
    m.add("entry 2")
    m.clear()
    m2 = Memory(storage="sqlite", path=db)
    if m2.count() == 0:
        ok("clear() empties SQLite — count=0 after reload")
    else:
        fail("clear() empties SQLite", f"count={m2.count()}")
finally:
    shutil.rmtree(tmpdir)

# ── add_with_tags() uses shared add() path (Step 4) ──────────────────────────
print("\n=== add_with_tags() via shared add() ===")

tmpdir = tempfile.mkdtemp()
path = os.path.join(tmpdir, "tags.json")
try:
    m = Memory(path=path, ttl="7d")

    mid = m.add_with_tags("tagged entry", ["tech", "news"])
    rec = m.get(mid)
    if rec and rec.get("expires_at") is not None:
        ok("add_with_tags() applies class default TTL")
    else:
        fail("add_with_tags() applies class default TTL", f"rec={rec}")

    if rec and set(rec.get("tags", [])) == {"tech", "news"}:
        ok("add_with_tags() preserves tags")
    else:
        fail("add_with_tags() preserves tags", f"tags={rec.get('tags') if rec else 'missing'}")

    mid2 = m.add_with_tags("expires fast", ["temp"], ttl="1s")
    time.sleep(2)
    if m.get(mid2) is None:
        ok("add_with_tags() with explicit ttl='1s' expires correctly")
    else:
        fail("add_with_tags() with explicit ttl='1s' expires correctly")
finally:
    shutil.rmtree(tmpdir)

# ── CLI parameter correctness (Step 5) ──────────────────────────────────────
print("\n=== CLI parameter correctness ===")

import subprocess, sys as _sys
cli = "/root/.openclaw/workspace/projects/agent-memory/agent_memory.py"

# --ttl works
r = subprocess.run([_sys.executable, cli, "add", "--text", "cli ttl test", "--ttl", "3d"],
                   capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0 and "Added memory" in r.stdout:
    ok("CLI --ttl accepted without error")
else:
    fail("CLI --ttl accepted without error", r.stderr[:200])

# old --ttl-days rejected
r2 = subprocess.run([_sys.executable, cli, "add", "--text", "x", "--ttl-days", "7"],
                    capture_output=True, text=True, cwd="/tmp")
if r2.returncode != 0:
    ok("CLI --ttl-days correctly rejected (removed)")
else:
    fail("CLI --ttl-days correctly rejected", "it still accepted the arg")

# --encryption-key accepted
r3 = subprocess.run([_sys.executable, cli, "add", "--text", "enc test",
                     "--encryption-key", "mykey", "--encrypt"],
                    capture_output=True, text=True, cwd="/tmp")
if r3.returncode == 0 and "Added memory" in r3.stdout:
    ok("CLI --encryption-key and --encrypt accepted")
else:
    fail("CLI --encryption-key and --encrypt accepted", r3.stderr[:200])

# ── Redis delete coherence (Step 6) ─────────────────────────────────────────
print("\n=== Redis delete coherence ===")

if not HAS_REDIS:
    print("  SKIP  redis not installed")
else:
    import redis as _redis_mod, json as _json, shutil as _shutil
    try:
        r = _redis_mod.from_url("redis://127.0.0.1:6379", decode_responses=True)
        r.ping()
        server_up = True
    except Exception:
        server_up = False

    if not server_up:
        print("  SKIP  redis-server not reachable")
    else:
        tmpdir = tempfile.mkdtemp()
        try:
            m = Memory(path=os.path.join(tmpdir, "mem.json"),
                       redis_url="redis://127.0.0.1:6379")
            mid = m.add("to delete")
            key = f"memory:{mid}"
            assert r.exists(key), "key missing after add()"
            m.delete(mid)
            if not r.exists(key):
                ok("delete() removes key from Redis")
            else:
                fail("delete() removes key from Redis", "key still present")
        finally:
            _shutil.rmtree(tmpdir)
# ── Summary ──────────────────────────────────────────────────────────────────
print(f"\n{'='*40}")
print(f"Results: {PASS} passed, {FAIL} failed")
if FAIL > 0:
    sys.exit(1)
