#!/usr/bin/env python3
"""Simple API test demo"""

import requests
import json

print("=" * 60)
print("API TESTING DEMO")
print("=" * 60)

# Test 1: GET request
print("\n[Test 1] Testing GET /users/1")
response = requests.get("https://jsonplaceholder.typicode.com/users/1")

print(f"Status Code: {response.status_code}")
print(f"Response Time: {response.elapsed.total_seconds() * 1000:.2f}ms")

if response.status_code == 200:
    data = response.json()
    print(f"User Name: {data.get('name')}")
    print(f"User Email: {data.get('email')}")
    print("[PASS] GET request successful")
else:
    print("[FAIL] GET request failed")

# Test 2: POST request
print("\n[Test 2] Testing POST /posts")
new_post = {
    "title": "Test Post",
    "body": "This is a test post",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post
)

print(f"Status Code: {response.status_code}")

if response.status_code == 201:
    data = response.json()
    print(f"Created Post ID: {data.get('id')}")
    print("[PASS] POST request successful")
else:
    print("[FAIL] POST request failed")

# Test 3: Authentication test (should fail)
print("\n[Test 3] Testing authentication (no token)")
response = requests.get(
    "https://jsonplaceholder.typicode.com/users/1",
    headers={"Authorization": ""}
)

print(f"Status Code: {response.status_code}")
print("[INFO] Public API doesn't require auth")

# Test 4: Invalid endpoint
print("\n[Test 4] Testing 404 error")
response = requests.get("https://jsonplaceholder.typicode.com/invalid-endpoint")

print(f"Status Code: {response.status_code}")

if response.status_code == 404:
    print("[PASS] 404 error handled correctly")
else:
    print("[INFO] Got status:", response.status_code)

print("\n" + "=" * 60)
print("TESTS COMPLETED")
print("=" * 60)
