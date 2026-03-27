#!/usr/bin/env python3
"""
API Endpoint Tester - Test HTTP endpoints
"""

import argparse
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import ssl

def test_endpoint(url, method="GET", data=None, headers=None):
    """Test a single endpoint."""
    headers = headers or {"User-Agent": "API-Tester/1.0"}
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    
    try:
        req = Request(url, data=req_data, headers=headers, method=method)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        start = time.time()
        with urlopen(req, context=ctx, timeout=10) as resp:
            duration = time.time() - start
            body = resp.read().decode()[:500]
            return {
                "status": resp.status,
                "duration": round(duration, 3),
                "body": body[:200]
            }
    except HTTPError as e:
        return {"status": e.code, "error": str(e)[:100]}
    except Exception as e:
        return {"error": str(e)[:100]}

def main():
    parser = argparse.ArgumentParser(description="API Endpoint Tester")
    parser.add_argument("url", help="URL to test")
    parser.add_argument("-m", "--method", default="GET", help="HTTP method")
    parser.add_argument("-d", "--data", help="JSON data to send")
    parser.add_argument("-H", "--header", action="append", help="Headers")
    
    args = parser.parse_args()
    
    headers = {}
    if args.header:
        for h in args.header:
            k, v = h.split(":")
            headers[k.strip()] = v.strip()
    
    data = None
    if args.data:
        data = json.loads(args.data)
    
    result = test_endpoint(args.url, args.method, data, headers)
    
    print(f"🔍 {args.method} {args.url}")
    print(f"   Status: {result.get('status', 'ERROR')}")
    print(f"   Duration: {result.get('duration', 'N/A')}s")
    if "body" in result:
        print(f"   Body: {result['body'][:100]}...")
    if "error" in result:
        print(f"   Error: {result['error']}")

if __name__ == "__main__":
    main()