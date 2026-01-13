# Python API Testing Examples

Complete examples using `requests` and `httpx` libraries.

## Setup

### Installation

```bash
pip install requests httpx python-dotenv jsonschema pyjwt
```

### Environment Configuration

Create `.env` file:

```bash
API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here
JWT_TOKEN=your_jwt_token_here
USERNAME=your_username
PASSWORD=your_password
```

Load environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
JWT_TOKEN = os.getenv("JWT_TOKEN")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
```

---

## Example 1: Basic GET Request

```python
import requests

def test_get_users():
    """Test GET endpoint to fetch users."""

    url = f"{API_BASE_URL}/users"

    response = requests.get(url)

    # Assert status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Parse JSON response
    data = response.json()

    # Validate response structure
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Response should not be empty"

    # Validate first user object
    user = data[0]
    assert "id" in user, "User should have 'id' field"
    assert "name" in user, "User should have 'name' field"
    assert "email" in user, "User should have 'email' field"

    print(f"✓ GET /users returned {len(data)} users")
```

---

## Example 2: POST Request with JSON Body

```python
import requests
import json

def test_create_user():
    """Test POST endpoint to create a new user."""

    url = f"{API_BASE_URL}/users"

    new_user = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }

    response = requests.post(
        url,
        json=new_user,  # Automatically sets Content-Type: application/json
        headers={"Authorization": f"Bearer {JWT_TOKEN}"}
    )

    # Assert successful creation
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Parse response
    created_user = response.json()

    # Validate created user
    assert created_user["name"] == new_user["name"]
    assert created_user["email"] == new_user["email"]
    assert "id" in created_user, "Created user should have an ID"

    print(f"✓ Created user with ID: {created_user['id']}")

    return created_user["id"]
```

---

## Example 3: PUT/PATCH Request

```python
import requests

def test_update_user(user_id):
    """Test PUT endpoint to update a user."""

    url = f"{API_BASE_URL}/users/{user_id}"

    updated_data = {
        "name": "John Updated",
        "age": 31
    }

    # PUT - full replacement
    response = requests.put(
        url,
        json=updated_data,
        headers={"Authorization": f"Bearer {JWT_TOKEN}"}
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    updated_user = response.json()
    assert updated_user["name"] == "John Updated"
    assert updated_user["age"] == 31

    print(f"✓ Updated user {user_id}")


def test_patch_user(user_id):
    """Test PATCH endpoint for partial update."""

    url = f"{API_BASE_URL}/users/{user_id}"

    partial_update = {
        "age": 32  # Only update age
    }

    # PATCH - partial update
    response = requests.patch(
        url,
        json=partial_update,
        headers={"Authorization": f"Bearer {JWT_TOKEN}"}
    )

    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["age"] == 32

    print(f"✓ Patched user {user_id}")
```

---

## Example 4: DELETE Request

```python
import requests

def test_delete_user(user_id):
    """Test DELETE endpoint to remove a user."""

    url = f"{API_BASE_URL}/users/{user_id}"

    response = requests.delete(
        url,
        headers={"Authorization": f"Bearer {JWT_TOKEN}"}
    )

    # DELETE usually returns 204 No Content or 200 OK
    assert response.status_code in [200, 204], f"Expected 200/204, got {response.status_code}"

    print(f"✓ Deleted user {user_id}")

    # Verify deletion
    get_response = requests.get(url)
    assert get_response.status_code == 404, "User should not exist after deletion"

    print(f"✓ Verified user {user_id} was deleted")
```

---

## Example 5: Query Parameters

```python
import requests

def test_query_parameters():
    """Test endpoint with query parameters."""

    url = f"{API_BASE_URL}/users"

    params = {
        "status": "active",
        "sort": "name",
        "limit": 10,
        "offset": 0
    }

    response = requests.get(url, params=params)

    assert response.status_code == 200

    # Check actual URL sent
    print(f"Request URL: {response.request.url}")
    # Output: https://api.example.com/users?status=active&sort=name&limit=10&offset=0

    data = response.json()
    assert len(data) <= 10, "Should respect limit parameter"

    print(f"✓ Query parameters test passed")
```

---

## Example 6: Custom Headers

```python
import requests

def test_custom_headers():
    """Test endpoint with custom headers."""

    url = f"{API_BASE_URL}/users"

    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "X-API-Key": API_KEY,
        "User-Agent": "MyTestClient/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200

    # Check request headers
    print(f"Request Headers: {response.request.headers}")

    print(f"✓ Custom headers test passed")
```

---

## Example 7: Error Handling

```python
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

def test_error_handling():
    """Test robust error handling."""

    url = f"{API_BASE_URL}/users/999999"  # Non-existent user

    try:
        response = requests.get(url, timeout=5)

        # Raise exception for 4xx/5xx status codes
        response.raise_for_status()

        # If we get here, request was successful
        data = response.json()
        print("Success:", data)

    except Timeout:
        print("✗ Request timed out")

    except ConnectionError:
        print("✗ Connection error occurred")

    except HTTPError as e:
        if e.response.status_code == 404:
            print("✓ User not found (expected)")
        elif e.response.status_code == 401:
            print("✗ Unauthorized")
        else:
            print(f"✗ HTTP error: {e.response.status_code}")

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
```

---

## Example 8: JSON Schema Validation

```python
import requests
from jsonschema import validate, ValidationError

def test_response_schema():
    """Test response matches expected JSON schema."""

    url = f"{API_BASE_URL}/users/123"

    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()

    # Define expected schema
    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0},
            "created_at": {"type": "string"}
        },
        "required": ["id", "name", "email"]
    }

    try:
        validate(instance=data, schema=user_schema)
        print("✓ Response matches schema")
    except ValidationError as e:
        print(f"✗ Schema validation failed: {e.message}")
```

---

## Example 9: File Upload

```python
import requests

def test_file_upload():
    """Test file upload endpoint."""

    url = f"{API_BASE_URL}/upload"

    # Upload a file
    with open("test_file.txt", "rb") as f:
        files = {"file": ("test_file.txt", f, "text/plain")}

        response = requests.post(
            url,
            files=files,
            headers={"Authorization": f"Bearer {JWT_TOKEN}"}
        )

    assert response.status_code == 200

    result = response.json()
    assert "file_id" in result

    print(f"✓ File uploaded with ID: {result['file_id']}")
```

---

## Example 10: Session Management

```python
import requests

def test_session():
    """Use session to persist cookies and headers."""

    session = requests.Session()

    # Set default headers for all requests in this session
    session.headers.update({
        "Authorization": f"Bearer {JWT_TOKEN}",
        "User-Agent": "MyTestClient/1.0"
    })

    # Make multiple requests using same session
    response1 = session.get(f"{API_BASE_URL}/users")
    response2 = session.get(f"{API_BASE_URL}/posts")

    assert response1.status_code == 200
    assert response2.status_code == 200

    print("✓ Session test passed")

    # Close session when done
    session.close()
```

---

## Example 11: Async Requests with httpx

```python
import httpx
import asyncio

async def test_async_requests():
    """Test multiple endpoints concurrently."""

    async with httpx.AsyncClient() as client:
        # Create multiple concurrent requests
        tasks = [
            client.get(f"{API_BASE_URL}/users"),
            client.get(f"{API_BASE_URL}/posts"),
            client.get(f"{API_BASE_URL}/comments")
        ]

        # Wait for all requests to complete
        responses = await asyncio.gather(*tasks)

        # Validate all responses
        for i, response in enumerate(responses):
            assert response.status_code == 200
            print(f"✓ Request {i+1} completed: {response.json()}")

# Run async function
asyncio.run(test_async_requests())
```

---

## Example 12: GraphQL Testing

```python
import requests

def test_graphql_query():
    """Test GraphQL query."""

    url = f"{API_BASE_URL}/graphql"

    query = """
    query GetUser($id: ID!) {
      user(id: $id) {
        id
        name
        email
        posts {
          title
          createdAt
        }
      }
    }
    """

    variables = {"id": "123"}

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JWT_TOKEN}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Check for GraphQL errors
    if "errors" in data:
        print(f"✗ GraphQL errors: {data['errors']}")
        return

    # Validate response
    assert "data" in data
    assert "user" in data["data"]
    assert data["data"]["user"]["id"] == "123"

    print(f"✓ GraphQL query successful")


def test_graphql_mutation():
    """Test GraphQL mutation."""

    url = f"{API_BASE_URL}/graphql"

    mutation = """
    mutation CreateUser($input: CreateUserInput!) {
      createUser(input: $input) {
        id
        name
        email
      }
    }
    """

    variables = {
        "input": {
            "name": "Test User",
            "email": "test@example.com"
        }
    }

    response = requests.post(
        url,
        json={
            "query": mutation,
            "variables": variables
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JWT_TOKEN}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    if "errors" in data:
        print(f"✗ Mutation failed: {data['errors']}")
        return

    created_user = data["data"]["createUser"]
    assert "id" in created_user

    print(f"✓ Created user via GraphQL: {created_user['id']}")
```

---

## Example 13: Complete Test Suite

```python
import requests
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
JWT_TOKEN = os.getenv("JWT_TOKEN")

class APITestSuite:
    """Complete API test suite."""

    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        })

    def test_get_all_users(self):
        """Test GET /users."""
        response = self.session.get(f"{self.base_url}/users")
        assert response.status_code == 200
        print("✓ GET /users")

    def test_get_user_by_id(self, user_id):
        """Test GET /users/:id."""
        response = self.session.get(f"{self.base_url}/users/{user_id}")
        assert response.status_code == 200
        print(f"✓ GET /users/{user_id}")

    def test_create_user(self):
        """Test POST /users."""
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        response = self.session.post(f"{self.base_url}/users", json=new_user)
        assert response.status_code == 201
        user_id = response.json()["id"]
        print(f"✓ POST /users (created ID: {user_id})")
        return user_id

    def test_update_user(self, user_id):
        """Test PUT /users/:id."""
        updated_data = {"name": "Updated Name"}
        response = self.session.put(
            f"{self.base_url}/users/{user_id}",
            json=updated_data
        )
        assert response.status_code == 200
        print(f"✓ PUT /users/{user_id}")

    def test_delete_user(self, user_id):
        """Test DELETE /users/:id."""
        response = self.session.delete(f"{self.base_url}/users/{user_id}")
        assert response.status_code in [200, 204]
        print(f"✓ DELETE /users/{user_id}")

    def run_all_tests(self):
        """Run complete test suite."""
        print("Starting API Test Suite...")
        print("-" * 50)

        # Run tests in order
        self.test_get_all_users()

        user_id = self.test_create_user()

        self.test_get_user_by_id(user_id)
        self.test_update_user(user_id)
        self.test_delete_user(user_id)

        print("-" * 50)
        print("✓ All tests passed!")

        # Close session
        self.session.close()

# Run test suite
if __name__ == "__main__":
    test_suite = APITestSuite(API_BASE_URL, JWT_TOKEN)
    test_suite.run_all_tests()
```

---

## Example 14: Retry Logic

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def test_with_retry():
    """Test with automatic retry logic."""

    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Make request with retry
    response = session.get(f"{API_BASE_URL}/users", timeout=5)

    assert response.status_code == 200
    print("✓ Request with retry successful")

    session.close()
```

---

## Example 15: Performance Timing

```python
import requests
import time

def test_performance():
    """Measure API response time."""

    url = f"{API_BASE_URL}/users"

    start_time = time.time()

    response = requests.get(url)

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

    assert response.status_code == 200

    print(f"✓ Request completed in {elapsed_time:.2f}ms")

    # Assert performance requirements
    assert elapsed_time < 1000, f"Request too slow: {elapsed_time}ms"

    print("✓ Performance test passed")
```

---

## References

- [Requests Documentation](https://requests.readthedocs.io/)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)
- [JSON Schema Validation](https://python-jsonschema.readthedocs.io/)
