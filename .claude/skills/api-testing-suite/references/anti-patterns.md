# API Testing Anti-Patterns

Common mistakes to avoid when testing APIs.

---

## 1. Testing Only Happy Paths

❌ **BAD:**
```python
def test_get_user():
    response = requests.get("/users/123")
    assert response.status_code == 200
    # Only tests successful case!
```

✅ **GOOD:**
```python
def test_get_user_success():
    response = requests.get("/users/123")
    assert response.status_code == 200

def test_get_user_not_found():
    response = requests.get("/users/999999")
    assert response.status_code == 404

def test_get_user_unauthorized():
    response = requests.get("/users/123")  # No auth
    assert response.status_code == 401
```

**Why it's bad:** Real users will encounter errors. Not testing error scenarios means bugs in error handling go undetected.

---

## 2. Hardcoding Credentials and URLs

❌ **BAD:**
```python
API_URL = "https://api.example.com"
API_KEY = "sk_live_abc123xyz789"  # Exposed secret!
JWT_TOKEN = "eyJhbGc..."  # Hardcoded token

response = requests.get(
    f"{API_URL}/users",
    headers={"Authorization": f"Bearer {JWT_TOKEN}"}
)
```

✅ **GOOD:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
JWT_TOKEN = os.getenv("JWT_TOKEN")
```

**Why it's bad:**
- Secrets committed to git are exposed forever
- Different environments need different configs
- Security risk if code is shared

---

## 3. Not Using Proper HTTP Methods

❌ **BAD:**
```python
# Using GET for everything
requests.get("/users/delete/123")
requests.get("/users/create?name=John")
requests.get("/users/update/123?name=Jane")
```

✅ **GOOD:**
```python
requests.delete("/users/123")
requests.post("/users", json={"name": "John"})
requests.put("/users/123", json={"name": "Jane"})
```

**Why it's bad:**
- Violates HTTP semantics
- GET requests can be cached incorrectly
- Breaks REST principles
- Side effects on safe methods

---

## 4. Ignoring Status Codes

❌ **BAD:**
```python
response = requests.get("/users")
data = response.json()  # Crashes if not JSON or request failed
```

❌ **BAD:**
```python
response = requests.post("/users", json={"name": "John"})
# Assumes success without checking
user_id = response.json()["id"]  # Crashes if request failed
```

✅ **GOOD:**
```python
response = requests.get("/users")
assert response.status_code == 200
data = response.json()
```

✅ **GOOD:**
```python
response = requests.post("/users", json={"name": "John"})

if response.status_code == 201:
    user_id = response.json()["id"]
else:
    print(f"Failed to create user: {response.status_code}")
```

**Why it's bad:** Missing errors leads to false positives and harder debugging.

---

## 5. Not Setting Timeouts

❌ **BAD:**
```python
response = requests.get("/users")  # Could hang forever
```

✅ **GOOD:**
```python
response = requests.get("/users", timeout=5)  # 5 second timeout
```

**Why it's bad:** Tests can hang indefinitely if API is slow or unresponsive.

---

## 6. Test Data Dependencies

❌ **BAD:**
```python
# test_1.py
def test_create_user():
    response = requests.post("/users", json={"id": 123, "name": "Test"})
    # Leaves user in database

# test_2.py
def test_update_user():
    # Assumes user 123 exists from test_1
    response = requests.put("/users/123", json={"name": "Updated"})
    assert response.status_code == 200  # Fails if test_1 didn't run!
```

✅ **GOOD:**
```python
def test_update_user():
    # Create test user
    create_response = requests.post("/users", json={"name": "Test"})
    user_id = create_response.json()["id"]

    # Test update
    response = requests.put(f"/users/{user_id}", json={"name": "Updated"})
    assert response.status_code == 200

    # Cleanup
    requests.delete(f"/users/{user_id}")
```

**Why it's bad:**
- Tests become order-dependent
- Random test failures
- Hard to debug
- Not truly isolated

---

## 7. Not Cleaning Up Test Data

❌ **BAD:**
```python
def test_create_user():
    response = requests.post("/users", json={"name": "Test User"})
    assert response.status_code == 201
    # User left in database forever!
```

✅ **GOOD:**
```python
def test_create_user():
    response = requests.post("/users", json={"name": "Test User"})
    assert response.status_code == 201

    user_id = response.json()["id"]

    # Cleanup
    requests.delete(f"/users/{user_id}")
```

✅ **BETTER:**
```python
class TestUserAPI:
    def setup_method(self):
        # Create test data
        response = requests.post("/users", json={"name": "Test"})
        self.user_id = response.json()["id"]

    def teardown_method(self):
        # Cleanup automatically after each test
        requests.delete(f"/users/{self.user_id}")

    def test_get_user(self):
        response = requests.get(f"/users/{self.user_id}")
        assert response.status_code == 200
```

**Why it's bad:** Database fills with garbage data, tests may conflict.

---

## 8. Over-Testing Implementation Details

❌ **BAD:**
```python
def test_user_serialization():
    # Testing internal implementation
    user = User(name="John", email="john@example.com")
    serialized = user.to_dict()
    assert "name" in serialized
    assert "email" in serialized
    # This should be a unit test, not API test
```

✅ **GOOD:**
```python
def test_get_user_response_format():
    # Test API contract
    response = requests.get("/users/123")
    user = response.json()

    assert "id" in user
    assert "name" in user
    assert "email" in user
```

**Why it's bad:** API tests should test the API contract, not implementation details.

---

## 9. Not Validating Response Schema

❌ **BAD:**
```python
response = requests.get("/users/123")
assert response.status_code == 200
# Doesn't validate response structure!
```

✅ **GOOD:**
```python
from jsonschema import validate

response = requests.get("/users/123")
assert response.status_code == 200

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["id", "name", "email"]
}

validate(instance=response.json(), schema=user_schema)
```

**Why it's bad:** API might return 200 but with wrong data structure.

---

## 10. Logging Sensitive Information

❌ **BAD:**
```python
headers = {"Authorization": f"Bearer {token}"}
print(f"Request headers: {headers}")  # Logs token!

response = requests.post("/login", json={
    "username": "user@example.com",
    "password": "secret123"
})
print(f"Login request: {response.request.body}")  # Logs password!
```

✅ **GOOD:**
```python
headers = {"Authorization": "Bearer ***REDACTED***"}
print(f"Request headers: {headers}")

print("Login request sent")  # Don't log credentials
```

**Why it's bad:** Sensitive data exposed in logs, security breach risk.

---

## 11. Using production APIs for Testing

❌ **BAD:**
```python
API_URL = "https://api.production.com"  # Testing against production!

def test_delete_user():
    requests.delete(f"{API_URL}/users/123")  # Deletes real user!
```

✅ **GOOD:**
```python
import os

ENVIRONMENT = os.getenv("TEST_ENV", "development")

ENV_URLS = {
    "development": "https://dev-api.example.com",
    "staging": "https://staging-api.example.com",
    "production": "https://api.example.com"  # Never used for automated tests
}

API_URL = ENV_URLS[ENVIRONMENT]

# For production, only run read-only tests
if ENVIRONMENT == "production":
    skip_destructive_tests = True
```

**Why it's bad:**
- Risk of data corruption
- Can't run destructive tests
- Performance impact on real users

---

## 12. Not Handling Network Errors

❌ **BAD:**
```python
response = requests.get("/users")
data = response.json()  # Crashes if network error
```

✅ **GOOD:**
```python
try:
    response = requests.get("/users", timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection failed")
except requests.exceptions.HTTPError:
    print(f"HTTP error: {response.status_code}")
```

**Why it's bad:** Tests crash instead of reporting clear errors.

---

## 13. Testing Everything in One Test

❌ **BAD:**
```python
def test_user_api():
    # Create user
    response = requests.post("/users", json={"name": "John"})
    assert response.status_code == 201

    # Get user
    user_id = response.json()["id"]
    response = requests.get(f"/users/{user_id}")
    assert response.status_code == 200

    # Update user
    response = requests.put(f"/users/{user_id}", json={"name": "Jane"})
    assert response.status_code == 200

    # Delete user
    response = requests.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # This test does too much!
```

✅ **GOOD:**
```python
def test_create_user():
    response = requests.post("/users", json={"name": "John"})
    assert response.status_code == 201
    cleanup(response.json()["id"])

def test_get_user():
    user_id = setup_test_user()
    response = requests.get(f"/users/{user_id}")
    assert response.status_code == 200
    cleanup(user_id)

def test_update_user():
    user_id = setup_test_user()
    response = requests.put(f"/users/{user_id}", json={"name": "Jane"})
    assert response.status_code == 200
    cleanup(user_id)

def test_delete_user():
    user_id = setup_test_user()
    response = requests.delete(f"/users/{user_id}")
    assert response.status_code == 204
```

**Why it's bad:**
- Hard to identify which part failed
- Can't run tests independently
- Difficult to maintain

---

## 14. Assuming Response Format

❌ **BAD:**
```python
response = requests.get("/users")
users = response.json()
first_user = users[0]  # Crashes if list is empty
name = first_user["name"]  # Crashes if field missing
```

✅ **GOOD:**
```python
response = requests.get("/users")
assert response.status_code == 200

users = response.json()
assert isinstance(users, list)
assert len(users) > 0

first_user = users[0]
assert "name" in first_user
name = first_user["name"]
```

**Why it's bad:** Tests crash with unclear errors instead of meaningful assertions.

---

## 15. Not Testing Rate Limiting

❌ **BAD:**
```python
# Never tests rate limits
def test_get_users():
    response = requests.get("/users")
    assert response.status_code == 200
```

✅ **GOOD:**
```python
def test_rate_limiting():
    # Send requests until rate limited
    for i in range(100):
        response = requests.get("/users")

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            assert retry_after is not None
            print(f"Rate limited after {i} requests")
            return

    # If we get here, rate limiting not implemented
    assert False, "Rate limiting not enforced"
```

**Why it's bad:** Users may abuse API if rate limiting isn't tested.

---

## 16. Mocking External APIs in Integration Tests

❌ **BAD:**
```python
# Integration test that mocks the actual API
@mock.patch('requests.get')
def test_get_user(mock_get):
    mock_get.return_value.json.return_value = {"id": 123, "name": "John"}
    mock_get.return_value.status_code = 200

    # This is a unit test, not integration test!
    response = requests.get("/users/123")
    assert response.status_code == 200
```

✅ **GOOD:**
```python
# Real integration test
def test_get_user():
    # Actually call the API
    response = requests.get(f"{API_URL}/users/123")
    assert response.status_code == 200
    assert "id" in response.json()
```

**Why it's bad:** You're testing the mock, not the actual API.

---

## 17. Ignoring HTTP Headers

❌ **BAD:**
```python
response = requests.post("/users", data={"name": "John"})
# Doesn't set Content-Type, server may reject or misinterpret
```

✅ **GOOD:**
```python
response = requests.post(
    "/users",
    json={"name": "John"},  # Automatically sets Content-Type: application/json
    headers={"Accept": "application/json"}
)
```

**Why it's bad:** Ambiguous requests, server may misinterpret data format.

---

## 18. Not Testing Edge Cases

❌ **BAD:**
```python
def test_create_user():
    response = requests.post("/users", json={"name": "John", "age": 30})
    assert response.status_code == 201
```

✅ **GOOD:**
```python
def test_create_user_valid():
    response = requests.post("/users", json={"name": "John", "age": 30})
    assert response.status_code == 201

def test_create_user_empty_name():
    response = requests.post("/users", json={"name": "", "age": 30})
    assert response.status_code == 400

def test_create_user_negative_age():
    response = requests.post("/users", json={"name": "John", "age": -1})
    assert response.status_code == 400

def test_create_user_very_long_name():
    response = requests.post("/users", json={"name": "a" * 1000, "age": 30})
    assert response.status_code in [400, 413]
```

**Why it's bad:** Edge cases are where bugs hide.

---

## 19. Returning 200 for All Responses

❌ **BAD (Server Implementation):**
```python
# Server always returns 200, even for errors
@app.route("/users/<id>")
def get_user(id):
    user = db.get_user(id)
    if not user:
        return {"success": False, "error": "User not found"}, 200  # Wrong!
    return {"success": True, "data": user}, 200
```

✅ **GOOD (Server Implementation):**
```python
@app.route("/users/<id>")
def get_user(id):
    user = db.get_user(id)
    if not user:
        return {"error": "User not found"}, 404  # Correct status code
    return {"data": user}, 200
```

✅ **Test for this anti-pattern:**
```python
def test_proper_status_codes():
    # Success should return 200
    response = requests.get("/users/123")
    assert response.status_code == 200

    # Not found should return 404, not 200
    response = requests.get("/users/999999")
    assert response.status_code == 404, "API incorrectly returns 200 for errors"
```

**Why it's bad:**
- Breaks HTTP semantics
- Clients can't use standard error handling
- Caching breaks

---

## 20. Not Validating Content-Type

❌ **BAD:**
```python
response = requests.get("/users/123")
data = response.json()  # Assumes JSON, crashes if HTML error page
```

✅ **GOOD:**
```python
response = requests.get("/users/123")
assert response.status_code == 200

content_type = response.headers.get("Content-Type", "")
assert "application/json" in content_type, f"Expected JSON, got {content_type}"

data = response.json()
```

**Why it's bad:** Server might return HTML error page, causing JSON parsing to fail.

---

## Summary: Quick Checklist

Avoid these anti-patterns:

- [ ] Testing only happy paths
- [ ] Hardcoding credentials/URLs
- [ ] Using wrong HTTP methods
- [ ] Ignoring status codes
- [ ] No timeouts
- [ ] Test dependencies
- [ ] Not cleaning up test data
- [ ] Over-testing implementation
- [ ] Not validating schemas
- [ ] Logging sensitive data
- [ ] Testing on production
- [ ] Not handling network errors
- [ ] Giant multi-purpose tests
- [ ] Assuming response format
- [ ] Ignoring rate limits
- [ ] Mocking in integration tests
- [ ] Ignoring HTTP headers
- [ ] Not testing edge cases
- [ ] Returning 200 for errors
- [ ] Not checking Content-Type

---

## References

- [REST Anti-Patterns](https://www.infoq.com/articles/rest-anti-patterns/)
- [Common API Mistakes](https://zuplo.com/learning-center/common-pitfalls-in-restful-api-design)
- [API Design Anti-Patterns](https://blog.xapihub.io/2024/06/19/API-Design-Anti-patterns.html)
