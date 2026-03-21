#!/usr/bin/env python3
"""
v3.1 Backend Verification Script
Run: python3 test_all_backends.py
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_memory import Memory, parse_ttl


def test_parse_ttl():
    print("Testing parse_ttl()...")
    tests = [
        ("7d", 7.0),
        ("1h", 1/24),
        ("30m", 30/1440),
        ("2w", 14.0),
        ("30s", 30/86400),
        ("0s", 0.0),
        (None, None),
        (5, 5.0),
    ]
    for input_val, expected in tests:
        result = parse_ttl(input_val)
        if result is None and expected is None:
            continue
        if abs(result - expected) < 0.0001:
            continue
        print(f"  FAIL: parse_ttl({input_val!r}) = {result}, expected {expected}")
        return False
    print("  PASS: All parse_ttl tests passed")
    return True


def test_json_backend():
    print("Testing JSON backend...")
    path = tempfile.mktemp(suffix=".json")
    m = Memory(storage="json", path=path, ttl="7d", encryption_key="test_key")
    
    mid1 = m.add("test data", ttl="1h")
    mid2 = m.add("encrypted secret", ttl="30m", encrypt=True)
    mid3 = m.add("no TTL", ttl=None)
    mid4 = m.add("default TTL")
    
    rem1 = m.ttl_remaining(mid1)
    rem2 = m.ttl_remaining(mid2)
    rem3 = m.ttl_remaining(mid3)
    rem4 = m.ttl_remaining(mid4)
    
    assert 3500 < rem1 < 3700, f"TTL 1h failed: {rem1}"
    assert 1700 < rem2 < 1900, f"TTL 30m failed: {rem2}"
    assert rem3 is None, f"TTL None failed: {rem3}"
    assert 600000 < rem4 < 610000, f"TTL default failed: {rem4}"
    
    ret1 = m.get(mid1)
    assert ret1["text"] == "test data", "decryption failed"
    ret2 = m.get(mid2)
    assert ret2["text"] == "encrypted secret", "encrypted decryption failed"
    ret3 = m.get(mid3)
    assert ret3["text"] == "no TTL", "no TTL failed"
    
    results = m.search("test")
    assert len(results) >= 1, "search failed"
    
    os.unlink(path)
    print("  PASS: JSON backend")
    return True


def test_sqlite_backend():
    print("Testing SQLite backend...")
    path = tempfile.mktemp(suffix=".db")
    m = Memory(storage="sqlite", path=path, ttl="7d")
    
    mid = m.add("sqlite test", ttl="1h")
    rem = m.ttl_remaining(mid)
    assert 3500 < rem < 3700, f"SQLite TTL failed: {rem}"
    
    ret = m.get(mid)
    assert ret["text"] == "sqlite test", "sqlite get failed"
    
    os.unlink(path.replace(".db", ".db"))
    print("  PASS: SQLite backend")
    return True


def test_redis_backend():
    print("Testing Redis backend...")
    try:
        import redis
        r = redis.Redis(host="localhost", port=6379)
        r.ping()
    except Exception as e:
        print(f"  SKIP: Redis not available ({e})")
        return True
    
    r.flushall()
    
    m = Memory(storage="redis", redis_url="redis://localhost:6379", ttl="7d", encryption_key="redis_key")
    
    mid1 = m.add("redis test", ttl="1h")
    mid2 = m.add("redis encrypted", ttl="30m", encrypt=True)
    
    rem1 = m.ttl_remaining(mid1)
    rem2 = m.ttl_remaining(mid2)
    assert 3500 < rem1 < 3700, f"Redis TTL 1h failed: {rem1}"
    assert 1700 < rem2 < 1900, f"Redis TTL 30m failed: {rem2}"
    
    ret1 = m.get(mid1)
    assert ret1["text"] == "redis test", f"Redis get failed: {ret1}"
    ret2 = m.get(mid2)
    assert ret2["text"] == "redis encrypted", f"Redis decrypt failed: {ret2}"
    
    r.flushall()
    print("  PASS: Redis backend")
    return True


def main():
    print("=" * 50)
    print("Agent Memory v3.1 - Backend Verification")
    print("=" * 50)
    print()
    
    results = []
    results.append(test_parse_ttl())
    results.append(test_json_backend())
    results.append(test_sqlite_backend())
    results.append(test_redis_backend())
    
    print()
    if all(results):
        print("=" * 50)
        print("ALL TESTS PASSED ✅")
        print("=" * 50)
        return 0
    else:
        print("SOME TESTS FAILED ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
