# API Authentication Methods

## Overview

Authentication verifies WHO you are. Authorization determines WHAT you can do.

| Method | Security | Complexity | Use Case |
|--------|----------|------------|----------|
| **API Keys** | Low | Low | Public APIs, server-to-server |
| **Basic Auth** | Low | Low | Simple internal APIs |
| **Bearer Token** | Medium | Low | Short-lived tokens |
| **JWT** | High | Medium | Stateless authentication |
| **OAuth 2.0** | High | High | Third-party access delegation |

---

## 1. API Keys

### How It Works

Client includes static API key in request header or query parameter.

### Implementation

**Header (Recommended):**

```http
GET /api/users HTTP/1.1
Host: api.example.com
X-API-Key: abc123def456ghi789
```

**Query Parameter (Less Secure):**

```http
GET /api/users?api_key=abc123def456ghi789
```

### Python Example

```python
import requests

API_KEY = "abc123def456ghi789"

# Header method (recommended)
response = requests.get(
    "https://api.example.com/users",
    headers={"X-API-Key": API_KEY}
)

# Query parameter method
response = requests.get(
    "https://api.example.com/users",
    params={"api_key": API_KEY}
)
```

### Testing API Keys

```python
def test_api_key_auth():
    """Test API key authentication."""

    # Test with valid API key
    response = requests.get(
        "https://api.example.com/protected",
        headers={"X-API-Key": "valid_key"}
    )
    assert response.status_code == 200

    # Test with invalid API key
    response = requests.get(
        "https://api.example.com/protected",
        headers={"X-API-Key": "invalid_key"}
    )
    assert response.status_code == 401

    # Test without API key
    response = requests.get(
        "https://api.example.com/protected"
    )
    assert response.status_code == 401
```

### Security Best Practices

✅ **DO:**
- Use HTTPS only
- Store keys in environment variables
- Rotate keys regularly
- Use different keys for different environments
- Implement rate limiting

❌ **DON'T:**
- Commit keys to version control
- Include keys in URLs (logs may expose them)
- Use same key for all users
- Share keys publicly

---

## 2. Basic Authentication

### How It Works

Client sends username:password encoded in Base64.

### Implementation

```http
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

Where `dXNlcm5hbWU6cGFzc3dvcmQ=` is Base64 encoding of `username:password`.

### Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

# Method 1: Using requests.auth
response = requests.get(
    "https://api.example.com/users",
    auth=HTTPBasicAuth("username", "password")
)

# Method 2: Shorthand
response = requests.get(
    "https://api.example.com/users",
    auth=("username", "password")
)

# Method 3: Manual header
import base64

credentials = base64.b64encode(b"username:password").decode("utf-8")
response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": f"Basic {credentials}"}
)
```

### Testing Basic Auth

```python
def test_basic_auth():
    """Test basic authentication."""

    # Valid credentials
    response = requests.get(
        "https://api.example.com/protected",
        auth=("valid_user", "valid_pass")
    )
    assert response.status_code == 200

    # Invalid credentials
    response = requests.get(
        "https://api.example.com/protected",
        auth=("invalid_user", "invalid_pass")
    )
    assert response.status_code == 401

    # No credentials
    response = requests.get(
        "https://api.example.com/protected"
    )
    assert response.status_code == 401
```

### Security Notes

⚠️ Basic Auth is **insecure without HTTPS** (credentials sent unencrypted)
⚠️ Not suitable for user-facing applications
⚠️ Better for server-to-server communication

---

## 3. Bearer Token

### How It Works

Client includes token in Authorization header with "Bearer" scheme.

### Implementation

```http
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Python Example

```python
import requests

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
)
```

### Token Acquisition

Usually obtained via login endpoint:

```python
def get_access_token(username, password):
    """Login and get access token."""

    response = requests.post(
        "https://api.example.com/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Login failed")

# Usage
token = get_access_token("user@example.com", "password123")

response = requests.get(
    "https://api.example.com/protected",
    headers={"Authorization": f"Bearer {token}"}
)
```

### Testing Bearer Tokens

```python
def test_bearer_token():
    """Test bearer token authentication."""

    # Get valid token
    token = get_access_token("valid_user", "valid_pass")

    # Test with valid token
    response = requests.get(
        "https://api.example.com/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Test with invalid token
    response = requests.get(
        "https://api.example.com/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

    # Test without token
    response = requests.get(
        "https://api.example.com/protected"
    )
    assert response.status_code == 401
```

---

## 4. JWT (JSON Web Token)

### How It Works

JWT is a self-contained token with encoded user info and signature.

### JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

│                  Header                  │                  Payload                   │         Signature         │
```

**Decoded Parts:**

Header:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Payload:
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

### Python Example

```python
import requests
import jwt
from datetime import datetime, timedelta

# Decode JWT (for inspection, not for verification)
def decode_jwt(token):
    """Decode JWT without verification."""
    return jwt.decode(token, options={"verify_signature": False})

# Using JWT with requests
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
)

# Check token expiration
def is_token_expired(token):
    """Check if JWT token is expired."""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp:
            return datetime.utcnow().timestamp() > exp
        return False
    except:
        return True
```

### Testing JWT

```python
import jwt
from datetime import datetime, timedelta

def test_jwt_authentication():
    """Test JWT authentication scenarios."""

    # Test with valid token
    valid_token = get_jwt_token("user@example.com", "password")
    response = requests.get(
        "https://api.example.com/protected",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200


def test_jwt_expiration():
    """Test expired JWT."""

    # Get token (assume it expires quickly)
    token = get_jwt_token("user@example.com", "password")

    # Wait for expiration (or use pre-expired token)
    # time.sleep(expiration_time + 1)

    response = requests.get(
        "https://api.example.com/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


def test_jwt_tampering():
    """Test tampered JWT."""

    valid_token = get_jwt_token("user@example.com", "password")

    # Tamper with token (change one character)
    tampered_token = valid_token[:-5] + "XXXXX"

    response = requests.get(
        "https://api.example.com/protected",
        headers={"Authorization": f"Bearer {tampered_token}"}
    )
    assert response.status_code == 401


def test_jwt_claims():
    """Test JWT claims validation."""

    token = get_jwt_token("user@example.com", "password")

    # Decode and check claims
    payload = jwt.decode(token, options={"verify_signature": False})

    assert "sub" in payload  # Subject (user ID)
    assert "exp" in payload  # Expiration
    assert "iat" in payload  # Issued at
```

### Common JWT Claims

| Claim | Name | Purpose |
|-------|------|---------|
| `sub` | Subject | User identifier |
| `iss` | Issuer | Who issued the token |
| `aud` | Audience | Who token is intended for |
| `exp` | Expiration | When token expires (Unix timestamp) |
| `iat` | Issued At | When token was issued |
| `nbf` | Not Before | Token not valid before this time |

---

## 5. OAuth 2.0

### How It Works

OAuth 2.0 is a delegation protocol allowing third-party access without sharing credentials.

### OAuth 2.0 Flow (Authorization Code)

```
1. User → Client App: "Login with Google"
2. Client → Auth Server: Redirect to authorization URL
3. User → Auth Server: Grants permission
4. Auth Server → Client: Returns authorization code
5. Client → Auth Server: Exchange code for access token
6. Auth Server → Client: Returns access token
7. Client → API: Use access token
```

### Python Example

```python
import requests
from urllib.parse import urlencode

# OAuth Configuration
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "https://accounts.example.com/oauth/authorize"
TOKEN_URL = "https://accounts.example.com/oauth/token"
API_URL = "https://api.example.com"

# Step 1: Generate authorization URL
def get_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "read write"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

# Step 2: Exchange authorization code for access token
def get_access_token(auth_code):
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to get access token")

# Step 3: Use access token
def call_api(access_token):
    response = requests.get(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()

# Token refresh
def refresh_access_token(refresh_token):
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to refresh token")
```

### Testing OAuth 2.0

```python
def test_oauth_flow():
    """Test complete OAuth flow."""

    # Step 1: Get authorization URL
    auth_url = get_authorization_url()
    assert "client_id" in auth_url
    assert "redirect_uri" in auth_url

    # Step 2: Simulate user authorization (in real test, use browser automation)
    # auth_code = simulate_user_authorization(auth_url)

    # Step 3: Exchange code for token
    # access_token = get_access_token(auth_code)
    # assert access_token is not None

    # Step 4: Use token to call API
    # response = call_api(access_token)
    # assert response.status_code == 200


def test_oauth_token_refresh():
    """Test token refresh."""

    # Assume we have a refresh token
    refresh_token = "refresh_token_here"

    new_access_token = refresh_access_token(refresh_token)
    assert new_access_token is not None

    # Use new token
    response = call_api(new_access_token)
    assert response.status_code == 200
```

### OAuth 2.0 Grant Types

| Grant Type | Use Case |
|------------|----------|
| **Authorization Code** | Web applications with backend |
| **Implicit** | Single-page applications (deprecated) |
| **Password** | First-party apps (not recommended) |
| **Client Credentials** | Machine-to-machine |
| **Refresh Token** | Get new access token |

---

## Comparison Table

| Feature | API Key | Basic Auth | Bearer Token | JWT | OAuth 2.0 |
|---------|---------|------------|--------------|-----|-----------|
| **Stateless** | Yes | No | No | Yes | Hybrid |
| **Expiration** | No | No | Yes | Yes | Yes |
| **Revocation** | Manual | Manual | Server-side | Challenging | Yes |
| **User Info** | No | No | No | Yes | Yes |
| **Third-party** | No | No | No | No | Yes |
| **Complexity** | Low | Low | Low | Medium | High |

---

## Security Testing Checklist

### For All Authentication Methods

- [ ] Valid credentials → 200 OK
- [ ] Invalid credentials → 401 Unauthorized
- [ ] Missing credentials → 401 Unauthorized
- [ ] HTTPS enforced
- [ ] Rate limiting implemented
- [ ] Credentials not logged

### For Tokens (Bearer, JWT, OAuth)

- [ ] Expired token → 401
- [ ] Tampered token → 401
- [ ] Token refresh works
- [ ] Token revocation works
- [ ] Short expiration times
- [ ] Secure token storage

### For OAuth 2.0

- [ ] Authorization flow completes
- [ ] Invalid redirect_uri rejected
- [ ] CSRF protection (state parameter)
- [ ] Scope validation
- [ ] Token refresh works
- [ ] Revocation endpoint works

---

## References

- [REST API Authentication Guide](https://www.knowi.com/blog/4-ways-of-rest-api-authentication-methods/)
- [JWT Introduction](https://jwt.io/introduction)
- [OAuth 2.0 RFC](https://oauth.net/2/)
- [API Security Best Practices](https://frontegg.com/guides/api-authentication-api-authorization)
