#!/usr/bin/env python
"""Simple test to verify backend & frontend are running."""
import requests
import sys

BASE = "http://127.0.0.1:8000"

print("=" * 50)
print("Product Search & Recommendation System - Test")
print("=" * 50)

try:
    # Test 1: Backend root
    r = requests.get(BASE + "/", timeout=2)
    if r.status_code == 200:
        print("✓ Backend running at http://127.0.0.1:8000")
    else:
        print("✗ Backend returned:", r.status_code)
        sys.exit(1)
except Exception as e:
    print("✗ Backend not running:", e)
    sys.exit(1)

try:
    # Test 2: Get a product
    r = requests.get(BASE + "/products/1", timeout=2)
    if r.status_code == 200:
        print(f"✓ Product endpoint working")
    else:
        print("✗ Product endpoint returned:", r.status_code)
        # Try popular instead
        r2 = requests.get(BASE + "/popular", timeout=2)
        if r2.status_code == 200:
            print(f"✓ Popular endpoint working ({len(r2.json())} products)")
        else:
            sys.exit(1)
except Exception as e:
    print("✗ API error:", e)
    sys.exit(1)

try:
    # Test 3: Frontend
    r = requests.get("http://127.0.0.1:3000", timeout=2)
    if r.status_code == 200:
        print("✓ Frontend running at http://127.0.0.1:3000")
    else:
        print("✗ Frontend returned:", r.status_code)
        sys.exit(1)
except Exception as e:
    print("✗ Frontend not running:", e)
    sys.exit(1)

print("=" * 50)
print("Hello! ✓ Everything is working!")
print("=" * 50)
print("\nOpen in browser:")
print("  Frontend: http://127.0.0.1:3000")
print("  API Docs: http://127.0.0.1:8000/docs")
