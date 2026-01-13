# API Testing Best Practices

## General Principles

### 1. Test Happy Paths AND Edge Cases

✅ **DO:**
```python
# Test successful request
test_get_user_success()

# Test error scenarios
test_get_user_not_found()
test_get_user_unauthorized()
test_get_user_invalid_id()
```

❌ **DON'T:**
```python
# Only test happy path
test_get_user()
```

### 2. Use Proper Assertions

✅ **DO:**
```python
response = requests.get(url)

assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert "id" in response.json(), "Response missing 'id' field"
assert response.json()["name"] == "John", f"Expected 'John', got {response.json()['name']}"
```

❌ **DON'T:**
```python
response = requests.get(url)
# No assertions - test always passes!
```

### 3. Test Independence

✅ **DO:**
```python
def test_create_user():
    # Create test data
    user_data = {"name": "Test", "email": "test@example.com"}

    # Test
    response = create_user(user_data)
    assert response.status_code == 201

    # Cleanup
    delete_user(response.json()["id"])
```

❌ **DON'T:**
```python
# Test depends on previous test creating user
def test_update_user():
    # Assumes user ID 123 exists from previous test
    response = update_user(123, {"name": "Updated"})
```

---

## Request Design

### 4. Use Environment Variables for Configuration

✅ **DO:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
```

Create `.env` file:
```bash
API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here
```

❌ **DON'T:**
```python
# Hardcoded credentials
API_BASE_URL = "https://api.example.com"
API_KEY = "abc123secret"  # Never commit secrets!
```

### 5. Set Proper Timeouts

✅ **DO:**
```python
response = requests.get(url, timeout=5)  # 5 second timeout
```

❌ **DON'T:**
```python
response = requests.get(url)  # No timeout - could hang forever
```

### 6. Handle Errors Gracefully

✅ **DO:**
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

❌ **DON'T:**
```python
response = requests.get(url)
return response.json()  # Will crash if request fails
```

---

## Response Validation

### 7. Validate Status Codes

✅ **DO:**
```python
# Test expected success
response = requests.get("/users")
assert response.status_code == 200

# Test expected errors
response = requests.get("/users/999999")
assert response.status_code == 404

response = requests.post("/protected")
assert response.status_code == 401
```

### 8. Validate Response Schema

✅ **DO:**
```python
from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["id", "name", "email"]
}

response = requests.get("/users/123")
validate(instance=response.json(), schema=user_schema)
```

### 9. Check Response Headers

✅ **DO:**
```python
response = requests.get("/users")

# Verify content type
assert response.headers["Content-Type"] == "application/json"

# Check caching headers
assert "Cache-Control" in response.headers

# Verify CORS headers (if applicable)
assert response.headers.get("Access-Control-Allow-Origin")
```

---

## Authentication & Security

### 10. Test Authentication Scenarios

✅ **DO:**
```python
def test_authentication():
    # Test with valid token
    response = requests.get(
        "/protected",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200

    # Test without token
    response = requests.get("/protected")
    assert response.status_code == 401

    # Test with invalid token
    response = requests.get(
        "/protected",
        headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401

    # Test with expired token
    response = requests.get(
        "/protected",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
```

### 11. Test Authorization (Role-Based Access)

✅ **DO:**
```python
def test_authorization():
    # Admin can delete users
    response = requests.delete(
        "/users/123",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # Regular user cannot delete users
    response = requests.delete(
        "/users/123",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
```

### 12. Never Log Sensitive Data

✅ **DO:**
```python
# Redact sensitive headers
headers_to_log = {
    k: "***REDACTED***" if k.lower() in ["authorization", "x-api-key"] else v
    for k, v in request_headers.items()
}
print(f"Request headers: {headers_to_log}")
```

❌ **DON'T:**
```python
print(f"Request headers: {request_headers}")  # Logs Authorization token!
```

---

## Data Validation

### 13. Test Input Validation

✅ **DO:**
```python
def test_input_validation():
    # Missing required field
    response = requests.post("/users", json={"name": "Test"})
    assert response.status_code == 400

    # Invalid email format
    response = requests.post("/users", json={
        "name": "Test",
        "email": "invalid-email"
    })
    assert response.status_code == 400

    # Invalid data type
    response = requests.post("/users", json={
        "name": "Test",
        "age": "invalid"  # Should be integer
    })
    assert response.status_code == 400
```

### 14. Test Boundary Values

✅ **DO:**
```python
def test_boundary_values():
    # Empty string
    response = requests.post("/users", json={"name": ""})
    assert response.status_code == 400

    # Very long string
    long_name = "a" * 1000
    response = requests.post("/users", json={"name": long_name})
    assert response.status_code == 400

    # Negative numbers
    response = requests.post("/users", json={"age": -1})
    assert response.status_code == 400

    # Maximum values
    response = requests.post("/users", json={"age": 999999})
    # Should either accept or reject with 400
```

---

## Performance & Reliability

### 15. Implement Retry Logic

✅ **DO:**
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

### 16. Test Rate Limiting

✅ **DO:**
```python
def test_rate_limiting():
    # Send many requests quickly
    for i in range(100):
        response = requests.get("/api/endpoint")

        if response.status_code == 429:
            # Rate limit hit
            retry_after = response.headers.get("Retry-After")
            print(f"Rate limited. Retry after {retry_after} seconds")
            break

    assert response.status_code == 429, "Rate limiting not implemented"
```

### 17. Measure Response Times

✅ **DO:**
```python
import time

def test_performance():
    start = time.time()
    response = requests.get("/users")
    elapsed = (time.time() - start) * 1000  # milliseconds

    assert response.status_code == 200
    assert elapsed < 1000, f"Response too slow: {elapsed}ms"

    print(f"Response time: {elapsed:.2f}ms")
```

---

## Test Organization

### 18. Use Descriptive Test Names

✅ **DO:**
```python
def test_get_user_returns_200_with_valid_id():
    pass

def test_get_user_returns_404_when_user_not_found():
    pass

def test_create_user_returns_400_when_email_missing():
    pass
```

❌ **DON'T:**
```python
def test1():
    pass

def test_user():
    pass
```

### 19. Group Related Tests

✅ **DO:**
```python
class TestUserAPI:
    def test_get_all_users(self):
        pass

    def test_get_user_by_id(self):
        pass

    def test_create_user(self):
        pass

class TestAuthenticationAPI:
    def test_login(self):
        pass

    def test_logout(self):
        pass
```

### 20. Use Setup and Teardown

✅ **DO:**
```python
class TestUserAPI:
    def setup_method(self):
        """Run before each test."""
        self.test_user_id = create_test_user()

    def teardown_method(self):
        """Run after each test."""
        delete_test_user(self.test_user_id)

    def test_update_user(self):
        # Test user already created in setup
        response = update_user(self.test_user_id, {"name": "Updated"})
        assert response.status_code == 200
```

---

## Documentation & Reporting

### 21. Document Test Cases

✅ **DO:**
```python
def test_create_user_with_valid_data():
    """
    Test: POST /users with valid user data
    Expected: 201 Created
    Response: User object with generated ID
    """
    new_user = {
        "name": "John Doe",
        "email": "john@example.com"
    }

    response = requests.post("/users", json=new_user)

    assert response.status_code == 201
    assert "id" in response.json()
```

### 22. Generate Test Reports

✅ **DO:**
```python
import json
from datetime import datetime

test_results = []

def run_test(test_name, test_func):
    start_time = datetime.now()

    try:
        test_func()
        status = "PASS"
        error = None
    except AssertionError as e:
        status = "FAIL"
        error = str(e)
    except Exception as e:
        status = "ERROR"
        error = str(e)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    test_results.append({
        "test": test_name,
        "status": status,
        "duration": duration,
        "error": error,
        "timestamp": start_time.isoformat()
    })

    print(f"{'✓' if status == 'PASS' else '✗'} {test_name} ({duration:.2f}s)")

# Save results
with open("test_results.json", "w") as f:
    json.dump(test_results, f, indent=2)
```

---

## API-Specific Best Practices

### REST APIs

✅ **DO:**
- Test all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Verify proper status codes for each operation
- Test pagination, filtering, sorting
- Validate resource URLs follow RESTful conventions
- Test HATEOAS links (if applicable)

### GraphQL APIs

✅ **DO:**
- Test queries, mutations, subscriptions separately
- Validate schema with introspection
- Test nested fields and relationships
- Check for N+1 query problems
- Test error responses (errors array)
- Validate field-level authorization

---

## Continuous Testing

### 23. Integrate with CI/CD

✅ **DO:**
```yaml
# .github/workflows/api-tests.yml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run API tests
        run: python -m pytest tests/
        env:
          API_BASE_URL: ${{ secrets.API_BASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
```

### 24. Test Against Multiple Environments

✅ **DO:**
```python
import os

ENVIRONMENT = os.getenv("TEST_ENV", "development")

ENV_CONFIGS = {
    "development": {
        "base_url": "https://dev-api.example.com",
        "timeout": 10
    },
    "staging": {
        "base_url": "https://staging-api.example.com",
        "timeout": 5
    },
    "production": {
        "base_url": "https://api.example.com",
        "timeout": 3
    }
}

config = ENV_CONFIGS[ENVIRONMENT]
```

---

## Summary Checklist

- [ ] Test both success and error scenarios
- [ ] Use descriptive test names
- [ ] Validate status codes, headers, and response body
- [ ] Test authentication and authorization
- [ ] Validate input with boundary values
- [ ] Handle errors gracefully with timeouts
- [ ] Never hardcode credentials
- [ ] Implement retry logic for transient failures
- [ ] Measure and assert on performance
- [ ] Generate test reports
- [ ] Integrate with CI/CD
- [ ] Test against multiple environments
- [ ] Document test cases
- [ ] Clean up test data

---

## References

- [API Design Best Practices](https://dev.to/cryptosandy/api-design-best-practices-in-2025-rest-graphql-and-grpc-2666)
- [GraphQL Testing Best Practices](https://amplication.com/blog/best-practices-in-testing-graphql-apis)
- [Postman Best Practices](https://blog.postman.com/)
