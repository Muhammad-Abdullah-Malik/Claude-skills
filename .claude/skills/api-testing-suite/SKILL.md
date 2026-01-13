---
name: api-testing-suite
description: |
  Automates REST and GraphQL API testing with Python (requests/httpx). Use when users ask to test APIs, validate endpoints, check authentication, verify responses, perform security testing, or explore API behavior. Supports manual testing workflows, security validation (JWT, OAuth, API keys), request/response validation, mock data generation, and detailed reporting.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# API Testing Suite

Automates REST and GraphQL API testing with comprehensive validation, security testing, and reporting capabilities.

## How This Skill Works

```
User: "Test this API endpoint for authentication issues"
       ↓
Gather context (API docs, existing tests, environment)
       ↓
Generate test scripts with security validation
       ↓
Execute tests and generate reports
```

This skill provides automated workflows for testing APIs with focus on:
- Manual API exploration and testing
- Security validation (authentication, authorization, input validation)
- Request/response validation
- Error handling and edge cases

## What This Skill Does

- Tests REST and GraphQL APIs using Python (requests, httpx)
- Validates authentication mechanisms (JWT, OAuth 2.0, API keys)
- Checks authorization and role-based access control
- Validates request/response schemas and data types
- Tests error handling and edge cases
- Generates mock data for testing
- Creates detailed test reports with pass/fail status
- Supports multiple environments (dev, staging, production)

## What This Skill Does NOT Do

- Load/performance testing (use dedicated load testing tools)
- UI/browser-based API testing (use playwright skill)
- Real-time monitoring or alerting
- Deploy or modify production systems
- Store sensitive credentials (always use environment variables)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing API code, route definitions, authentication middleware, existing tests |
| **Conversation** | API endpoints to test, authentication method, expected behaviors, security concerns |
| **Skill References** | REST/GraphQL patterns from `references/` (authentication methods, validation patterns, best practices) |
| **User Guidelines** | Team conventions, security policies, environment setup, credential management |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Testing Workflows

### 1. Manual API Testing Workflow

```
Define endpoint → Configure auth → Send request → Validate response → Report results
```

**Steps:**

1. **Gather API Information**
   - Endpoint URL and HTTP method
   - Required headers (Content-Type, Accept, custom headers)
   - Authentication requirements
   - Request body schema (for POST/PUT/PATCH)

2. **Configure Authentication**
   - If JWT: Token in `Authorization: Bearer <token>` header
   - If API Key: Key in header or query parameter
   - If OAuth: Access token from OAuth flow
   - If Basic Auth: Base64-encoded credentials

3. **Prepare Request**
   - Construct request with proper headers
   - Format request body (JSON, form-data, XML)
   - Add query parameters if needed

4. **Execute Request**
   - Send HTTP request using requests/httpx
   - Handle timeouts (default: 30 seconds)
   - Capture full response (status, headers, body)

5. **Validate Response**
   - Check HTTP status code (2xx = success, 4xx = client error, 5xx = server error)
   - Validate response schema against expected structure
   - Check response data types and values
   - Verify required fields are present

6. **Generate Report**
   - Log request details (method, URL, headers, body)
   - Log response details (status, headers, body)
   - Report pass/fail with specific error messages
   - Include timestamps and execution time

### 2. Security Testing Workflow

```
Identify auth method → Test valid credentials → Test invalid credentials → Test authorization → Report vulnerabilities
```

**Security Test Categories:**

| Category | Tests |
|----------|-------|
| **Authentication** | Valid credentials, invalid credentials, expired tokens, missing tokens |
| **Authorization** | Role-based access, resource ownership, forbidden operations |
| **Input Validation** | SQL injection, XSS, invalid data types, boundary values |
| **Rate Limiting** | Excessive requests, DoS protection |
| **Token Security** | Token expiration, token refresh, token revocation |

**Steps:**

1. **Test Valid Authentication**
   - Send request with valid credentials
   - Verify 200/201 status code
   - Verify expected response data

2. **Test Invalid Authentication**
   - Send request without credentials → Expect 401 Unauthorized
   - Send request with invalid credentials → Expect 401 Unauthorized
   - Send request with expired token → Expect 401 Unauthorized

3. **Test Authorization**
   - Test user accessing their own resources → Expect 200
   - Test user accessing others' resources → Expect 403 Forbidden
   - Test different roles (admin vs regular user)

4. **Test Input Validation**
   - Send invalid data types → Expect 400 Bad Request
   - Send missing required fields → Expect 400 Bad Request
   - Send boundary values (empty strings, very long strings, negative numbers)
   - Test for injection vulnerabilities (SQL, XSS) → Should be sanitized

5. **Generate Security Report**
   - List all vulnerabilities found
   - Severity level (Critical, High, Medium, Low)
   - Recommendations for fixes
   - OWASP Top 10 mapping if applicable

### 3. GraphQL API Testing Workflow

```
Define query/mutation → Configure auth → Execute GraphQL request → Validate schema → Report results
```

**Steps:**

1. **Prepare GraphQL Query/Mutation**
   ```graphql
   query GetUser($id: ID!) {
     user(id: $id) {
       id
       name
       email
     }
   }
   ```

2. **Send GraphQL Request**
   - POST to GraphQL endpoint
   - Content-Type: application/json
   - Body: `{"query": "...", "variables": {...}}`

3. **Validate GraphQL Response**
   - Check for `errors` array in response
   - Validate `data` matches expected schema
   - Check field types match GraphQL schema
   - Verify nested objects and arrays

4. **GraphQL-Specific Tests**
   - Schema introspection (if enabled)
   - Query complexity/depth limits
   - Batched queries
   - Alias usage
   - Fragment usage

---

## Python Implementation Patterns

### Using `requests` Library

```python
import requests
import json
from typing import Dict, Any

def test_api_endpoint(
    url: str,
    method: str = "GET",
    headers: Dict[str, str] = None,
    data: Any = None,
    auth_token: str = None
) -> Dict[str, Any]:
    """
    Test an API endpoint with validation.

    Returns dict with status, response, and validation results.
    """
    # Prepare headers
    req_headers = headers or {}
    if auth_token:
        req_headers["Authorization"] = f"Bearer {auth_token}"

    # Send request
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=req_headers,
            json=data if data else None,
            timeout=30
        )

        # Validate response
        result = {
            "success": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text,
            "time_ms": response.elapsed.total_seconds() * 1000
        }

        return result

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Using `httpx` Library (Async Support)

```python
import httpx
import asyncio
from typing import Dict, Any, List

async def test_api_endpoints_async(
    endpoints: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Test multiple API endpoints concurrently.

    endpoints format: [{"url": "...", "method": "GET", ...}, ...]
    """
    async with httpx.AsyncClient() as client:
        tasks = []
        for endpoint in endpoints:
            task = client.request(
                method=endpoint.get("method", "GET"),
                url=endpoint["url"],
                headers=endpoint.get("headers", {}),
                json=endpoint.get("data"),
                timeout=30.0
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                results.append({
                    "endpoint": endpoints[i]["url"],
                    "success": False,
                    "error": str(response)
                })
            else:
                results.append({
                    "endpoint": endpoints[i]["url"],
                    "success": 200 <= response.status_code < 300,
                    "status_code": response.status_code,
                    "body": response.json() if "application/json" in response.headers.get("content-type", "") else response.text
                })

        return results
```

---

## Error Handling Best Practices

### Common HTTP Status Codes

| Code | Meaning | Testing Action |
|------|---------|----------------|
| 200 | OK | Validate response data |
| 201 | Created | Verify resource was created |
| 204 | No Content | Expect empty response |
| 400 | Bad Request | Check error message, invalid input |
| 401 | Unauthorized | Authentication failed or missing |
| 403 | Forbidden | Authorization failed |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Server overloaded or maintenance |

### Error Handling Pattern

```python
def handle_api_error(response):
    """Handle different error scenarios with appropriate actions."""
    if response.status_code == 401:
        return {
            "error": "Authentication failed",
            "action": "Check credentials or refresh token"
        }
    elif response.status_code == 403:
        return {
            "error": "Authorization failed",
            "action": "Verify user has required permissions"
        }
    elif response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "60")
        return {
            "error": "Rate limit exceeded",
            "action": f"Wait {retry_after} seconds before retrying"
        }
    elif response.status_code >= 500:
        return {
            "error": "Server error",
            "action": "Retry request or contact API provider"
        }
    else:
        return {
            "error": f"Unexpected status code: {response.status_code}",
            "action": "Check API documentation"
        }
```

---

## Dependencies

### Required Python Packages

```bash
# Core HTTP libraries
pip install requests httpx

# For async support
pip install httpx[http2]

# For JSON schema validation
pip install jsonschema

# For environment variables
pip install python-dotenv

# For JWT decoding
pip install pyjwt

# For reporting
pip install pytest pytest-html  # If using pytest framework
```

### Environment Setup

Create `.env` file for sensitive credentials:

```bash
# .env file (NEVER commit to version control)
API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here
JWT_TOKEN=your_jwt_token_here
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret
```

Load environment variables in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
JWT_TOKEN = os.getenv("JWT_TOKEN")
```

---

## Usage Examples

### Example 1: Test REST API Endpoint

```python
# Test GET endpoint with JWT authentication
result = test_api_endpoint(
    url="https://api.example.com/users/123",
    method="GET",
    auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)

print(f"Status: {result['status_code']}")
print(f"Success: {result['success']}")
print(f"Response: {result['body']}")
```

### Example 2: Test Authentication

```python
# Test with valid token
valid_result = test_api_endpoint(
    url="https://api.example.com/protected",
    auth_token="valid_token_here"
)
assert valid_result['status_code'] == 200, "Valid token should work"

# Test without token
invalid_result = test_api_endpoint(
    url="https://api.example.com/protected"
)
assert invalid_result['status_code'] == 401, "No token should return 401"
```

### Example 3: Test GraphQL Query

```python
graphql_query = """
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
"""

result = test_api_endpoint(
    url="https://api.example.com/graphql",
    method="POST",
    data={
        "query": graphql_query,
        "variables": {"id": "123"}
    },
    auth_token="your_jwt_token"
)

# Validate GraphQL response
if "errors" in result['body']:
    print("GraphQL Errors:", result['body']['errors'])
else:
    print("User Data:", result['body']['data']['user'])
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/rest-api-concepts.md` | REST fundamentals, HTTP methods, status codes |
| `references/graphql-concepts.md` | GraphQL queries, mutations, schema validation |
| `references/authentication-methods.md` | JWT, OAuth 2.0, API keys implementation |
| `references/python-examples.md` | Complete Python examples with requests/httpx |
| `references/best-practices.md` | API testing best practices and patterns |
| `references/anti-patterns.md` | Common mistakes to avoid |
| `references/security-testing.md` | Security testing patterns and OWASP guidelines |

---

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install requests httpx python-dotenv jsonschema pyjwt
   ```

2. **Set up environment variables:**
   Create `.env` file with API credentials

3. **Run basic test:**
   ```bash
   python scripts/test_api.py --url https://api.example.com/endpoint --method GET
   ```

4. **Run security tests:**
   ```bash
   python scripts/security_test.py --config config.json
   ```

5. **View reports:**
   Test results saved to `reports/` directory

---

## Notes

- Always use HTTPS for API requests
- Never hardcode credentials in scripts
- Store sensitive data in environment variables
- Rotate API keys and tokens regularly
- Implement rate limiting in tests to avoid being blocked
- Use descriptive test names and assertions
- Generate detailed reports for debugging
- Follow API provider's terms of service
