# REST API Concepts

## What is REST?

REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP requests to perform CRUD operations (Create, Read, Update, Delete).

## HTTP Methods

| Method | Purpose | Idempotent | Safe | Request Body | Response Body |
|--------|---------|------------|------|--------------|---------------|
| **GET** | Retrieve resource(s) | Yes | Yes | No | Yes |
| **POST** | Create new resource | No | No | Yes | Yes |
| **PUT** | Update/replace resource | Yes | No | Yes | Yes |
| **PATCH** | Partial update | No | No | Yes | Yes |
| **DELETE** | Delete resource | Yes | No | No | Maybe |
| **HEAD** | Get headers only | Yes | Yes | No | No |
| **OPTIONS** | Get allowed methods | Yes | Yes | No | Yes |

### Idempotent vs Safe

- **Idempotent**: Multiple identical requests have same effect as single request
- **Safe**: Request doesn't modify server state

## HTTP Status Codes

### Success Codes (2xx)

| Code | Name | Usage |
|------|------|-------|
| 200 | OK | Request succeeded, response has body |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted for processing (async) |
| 204 | No Content | Success but no response body |

### Client Error Codes (4xx)

| Code | Name | Common Causes |
|------|------|---------------|
| 400 | Bad Request | Invalid syntax, validation failed |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Validation error (semantic) |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes (5xx)

| Code | Name | Meaning |
|------|------|---------|
| 500 | Internal Server Error | Generic server error |
| 502 | Bad Gateway | Invalid response from upstream |
| 503 | Service Unavailable | Server temporarily unavailable |
| 504 | Gateway Timeout | Upstream server timeout |

## Request Components

### 1. URL Structure

```
https://api.example.com/v1/users/123?include=profile&sort=name
│      │                │  │       │  │                      │
│      │                │  │       │  └─ Query Parameters
│      │                │  │       └─ Resource ID
│      │                │  └─ Resource Collection
│      │                └─ Version
│      └─ Host/Domain
└─ Protocol
```

### 2. Headers

Common request headers:

```http
Content-Type: application/json          # Request body format
Accept: application/json                # Desired response format
Authorization: Bearer <token>           # Authentication
User-Agent: MyApp/1.0                  # Client identification
Accept-Language: en-US                 # Preferred language
```

Common response headers:

```http
Content-Type: application/json         # Response body format
Content-Length: 1234                   # Body size in bytes
Cache-Control: max-age=3600           # Caching directives
ETag: "abc123"                        # Resource version
Location: /users/123                  # Created resource location
Retry-After: 60                       # Retry delay (for 429, 503)
```

### 3. Request Body

Example JSON request body (POST/PUT/PATCH):

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```

### 4. Response Body

Example JSON response:

```json
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-11T10:30:00Z"
  },
  "meta": {
    "version": "1.0"
  }
}
```

Error response format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {
        "field": "email",
        "issue": "Missing required field"
      }
    ]
  }
}
```

## REST Design Principles

### 1. Resource-Based URLs

✅ Good:
```
GET    /users           # Get all users
GET    /users/123       # Get specific user
POST   /users           # Create user
PUT    /users/123       # Update user
DELETE /users/123       # Delete user
```

❌ Bad (verbs in URL):
```
GET    /getAllUsers
POST   /createUser
POST   /deleteUser/123
```

### 2. Use Proper HTTP Methods

Don't use GET for operations that modify state:

❌ Bad:
```
GET /users/123/delete
GET /users/123/update?name=John
```

✅ Good:
```
DELETE /users/123
PUT    /users/123  (with body)
```

### 3. Return Appropriate Status Codes

❌ Bad:
```json
HTTP 200 OK
{
  "success": false,
  "error": "User not found"
}
```

✅ Good:
```json
HTTP 404 Not Found
{
  "error": "User not found"
}
```

### 4. Use Query Parameters for Filtering/Sorting

```
GET /users?status=active&sort=name&limit=10&offset=20
```

### 5. Version Your API

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

Or via headers:
```http
Accept: application/vnd.myapi.v1+json
```

## Content Negotiation

Client specifies desired format via `Accept` header:

```http
Accept: application/json        # JSON response
Accept: application/xml         # XML response
Accept: text/html              # HTML response
```

Server specifies response format via `Content-Type`:

```http
Content-Type: application/json
```

## CORS (Cross-Origin Resource Sharing)

Response headers for cross-origin requests:

```http
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600
```

## Pagination

### Offset-Based Pagination

```
GET /users?limit=10&offset=20
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "limit": 10,
    "offset": 20,
    "total": 100
  }
}
```

### Cursor-Based Pagination

```
GET /users?limit=10&cursor=abc123
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "def456",
    "has_more": true
  }
}
```

## Testing REST APIs

### Key Test Scenarios

1. **Happy Path**: Valid requests with expected responses
2. **Invalid Input**: Malformed data, missing fields
3. **Authentication**: Valid/invalid credentials
4. **Authorization**: Access control checks
5. **Edge Cases**: Boundary values, empty responses
6. **Error Handling**: Server errors, timeouts
7. **Idempotency**: Multiple identical requests
8. **Rate Limiting**: Exceeding request limits

### Example Test Cases

```python
# Test GET endpoint
response = requests.get("https://api.example.com/users/123")
assert response.status_code == 200
assert "id" in response.json()

# Test POST with validation error
response = requests.post(
    "https://api.example.com/users",
    json={"name": ""}  # Empty name
)
assert response.status_code == 400

# Test authentication
response = requests.get(
    "https://api.example.com/protected",
    headers={"Authorization": "Bearer invalid_token"}
)
assert response.status_code == 401

# Test 404
response = requests.get("https://api.example.com/users/999999")
assert response.status_code == 404
```

## References

- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [MDN Web Docs - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
