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

# ── Summary ──────────────────────────────────────────────────────────────────
print(f"\n{'='*40}")
print(f"Results: {PASS} passed, {FAIL} failed")
if FAIL > 0:
    sys.exit(1)
