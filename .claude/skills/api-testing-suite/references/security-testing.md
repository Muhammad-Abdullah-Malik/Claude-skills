# API Security Testing

Comprehensive guide for testing API security vulnerabilities and best practices.

---

## OWASP API Security Top 10 (2023)

### 1. Broken Object Level Authorization (BOLA)

**Description:** Users can access objects belonging to other users.

**Test Cases:**

```python
def test_bola_vulnerability():
    """Test if users can access others' resources."""

    # User A creates a resource
    user_a_token = login("user_a@example.com", "password")
    response = requests.post(
        "/api/documents",
        json={"title": "Private Document"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    document_id = response.json()["id"]

    # User B tries to access User A's resource
    user_b_token = login("user_b@example.com", "password")
    response = requests.get(
        f"/api/documents/{document_id}",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403, "BOLA vulnerability: User B accessed User A's document!"

    print("✓ BOLA test passed - proper authorization enforced")
```

**Expected Behavior:**
- ✅ 403 Forbidden when accessing another user's resource
- ❌ 200 OK = BOLA vulnerability

---

### 2. Broken Authentication

**Description:** Weak authentication mechanisms allow attackers to compromise accounts.

**Test Cases:**

```python
def test_weak_password_policy():
    """Test if API accepts weak passwords."""

    weak_passwords = ["123", "password", "abc", ""]

    for weak_pass in weak_passwords:
        response = requests.post(
            "/api/register",
            json={
                "email": f"test_{weak_pass}@example.com",
                "password": weak_pass
            }
        )

        # Should reject weak passwords
        assert response.status_code == 400, f"Weak password '{weak_pass}' was accepted!"

    print("✓ Password policy test passed")


def test_brute_force_protection():
    """Test if API has brute force protection."""

    # Try multiple failed login attempts
    for i in range(10):
        response = requests.post(
            "/api/login",
            json={
                "email": "user@example.com",
                "password": "wrong_password"
            }
        )

    # Should be rate limited or locked out
    assert response.status_code == 429, "No brute force protection!"

    print("✓ Brute force protection active")


def test_jwt_expiration():
    """Test if JWT tokens expire."""

    # Get token
    response = requests.post(
        "/api/login",
        json={"email": "user@example.com", "password": "correct_password"}
    )
    token = response.json()["access_token"]

    # Decode to check expiration
    import jwt
    payload = jwt.decode(token, options={"verify_signature": False})

    assert "exp" in payload, "Token has no expiration!"

    # Check expiration is reasonable (e.g., < 24 hours)
    from datetime import datetime
    exp_time = datetime.fromtimestamp(payload["exp"])
    now = datetime.now()
    hours_until_expiry = (exp_time - now).total_seconds() / 3600

    assert hours_until_expiry < 24, f"Token expires in {hours_until_expiry} hours - too long!"

    print(f"✓ Token expires in {hours_until_expiry:.1f} hours")
```

---

### 3. Broken Object Property Level Authorization

**Description:** Users can modify properties they shouldn't be able to.

**Test Cases:**

```python
def test_mass_assignment_vulnerability():
    """Test if users can set admin-only fields."""

    # Regular user tries to set 'role' to 'admin'
    user_token = login("user@example.com", "password")

    response = requests.post(
        "/api/users",
        json={
            "name": "Hacker",
            "email": "hacker@example.com",
            "role": "admin"  # Trying to set privileged field
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    if response.status_code == 201:
        user = response.json()
        # Check if role was actually set to admin
        assert user.get("role") != "admin", "Mass assignment vulnerability: regular user set admin role!"

    print("✓ Mass assignment protection active")


def test_read_only_fields():
    """Test if users can modify read-only fields."""

    user_token = login("user@example.com", "password")

    # Try to update created_at (should be read-only)
    response = requests.put(
        "/api/users/123",
        json={
            "name": "Updated Name",
            "created_at": "2020-01-01T00:00:00Z"  # Try to change creation date
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    user = response.json()

    # created_at should not have changed
    assert user["created_at"] != "2020-01-01T00:00:00Z", "Read-only field was modified!"

    print("✓ Read-only fields protected")
```

---

### 4. Unrestricted Resource Consumption

**Description:** APIs don't limit resource usage, allowing DoS attacks.

**Test Cases:**

```python
def test_rate_limiting():
    """Test if API implements rate limiting."""

    endpoint = "/api/users"
    rate_limited = False

    # Send many requests quickly
    for i in range(100):
        response = requests.get(endpoint)

        if response.status_code == 429:
            rate_limited = True
            retry_after = response.headers.get("Retry-After")
            print(f"✓ Rate limited after {i} requests. Retry-After: {retry_after}")
            break

    assert rate_limited, "No rate limiting implemented!"


def test_pagination_limits():
    """Test if API limits pagination size."""

    # Try to request huge page size
    response = requests.get("/api/users?limit=999999")

    data = response.json()

    # Should not return more than reasonable limit (e.g., 100)
    if isinstance(data, list):
        assert len(data) <= 100, f"API returned {len(data)} items - no pagination limit!"
    elif isinstance(data, dict) and "data" in data:
        assert len(data["data"]) <= 100, f"API returned {len(data['data'])} items!"

    print("✓ Pagination limits enforced")


def test_request_size_limits():
    """Test if API limits request body size."""

    # Try to send very large payload
    huge_payload = {"data": "x" * 10_000_000}  # 10MB of data

    response = requests.post(
        "/api/upload",
        json=huge_payload
    )

    # Should return 413 Payload Too Large
    assert response.status_code == 413, "No request size limit!"

    print("✓ Request size limits enforced")
```

---

### 5. Broken Function Level Authorization

**Description:** Regular users can access admin endpoints.

**Test Cases:**

```python
def test_admin_endpoint_access():
    """Test if regular users can access admin endpoints."""

    # Login as regular user
    user_token = login("user@example.com", "password")

    # Try to access admin endpoint
    response = requests.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403, "Regular user accessed admin endpoint!"

    print("✓ Admin endpoints protected")


def test_method_level_authorization():
    """Test if users have proper permissions for different methods."""

    user_token = login("user@example.com", "password")

    # User should be able to GET
    response = requests.get(
        "/api/users",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

    # But not DELETE (admin only)
    response = requests.delete(
        "/api/users/123",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403, "User can delete without admin permission!"

    print("✓ Method-level authorization enforced")
```

---

### 6. Unrestricted Access to Sensitive Business Flows

**Description:** Users can abuse critical business flows.

**Test Cases:**

```python
def test_purchase_flow_validation():
    """Test if purchase flow validates inventory."""

    # Try to buy more items than available
    response = requests.post(
        "/api/orders",
        json={
            "product_id": 123,
            "quantity": 999999  # More than available
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Should reject
    assert response.status_code == 400, "Inventory validation bypassed!"

    print("✓ Inventory validation works")


def test_discount_code_abuse():
    """Test if discount codes can be reused."""

    # Use discount code first time
    response1 = requests.post(
        "/api/orders",
        json={
            "product_id": 123,
            "discount_code": "SAVE50"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response1.status_code == 201

    # Try to reuse same code
    response2 = requests.post(
        "/api/orders",
        json={
            "product_id": 456,
            "discount_code": "SAVE50"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Should reject reuse
    assert response2.status_code == 400, "Discount code reused!"

    print("✓ Discount code validation works")
```

---

### 7. Server Side Request Forgery (SSRF)

**Description:** API makes requests to attacker-controlled URLs.

**Test Cases:**

```python
def test_ssrf_vulnerability():
    """Test if API validates URLs before fetching."""

    # Try to make API fetch internal resource
    malicious_urls = [
        "http://localhost:8080/admin",
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata
        "http://internal-server/secrets"
    ]

    for url in malicious_urls:
        response = requests.post(
            "/api/fetch-url",
            json={"url": url},
            headers={"Authorization": f"Bearer {user_token}"}
        )

        # Should reject internal URLs
        assert response.status_code == 400, f"SSRF vulnerability: fetched {url}!"

    print("✓ SSRF protection active")
```

---

### 8. Security Misconfiguration

**Description:** Improper security settings expose sensitive information.

**Test Cases:**

```python
def test_verbose_error_messages():
    """Test if errors expose sensitive information."""

    # Trigger error
    response = requests.get("/api/users/invalid_id")

    error_message = response.text.lower()

    # Should not expose stack traces, file paths, or database details
    sensitive_info = ["stack trace", "exception", "file path", "sql", "database"]

    for info in sensitive_info:
        assert info not in error_message, f"Error message exposes: {info}"

    print("✓ Error messages don't expose sensitive info")


def test_security_headers():
    """Test if API sets proper security headers."""

    response = requests.get("/api/users")

    headers = response.headers

    # Check for security headers
    assert "X-Content-Type-Options" in headers, "Missing X-Content-Type-Options"
    assert "X-Frame-Options" in headers, "Missing X-Frame-Options"
    assert "Strict-Transport-Security" in headers, "Missing HSTS header"

    print("✓ Security headers present")


def test_cors_configuration():
    """Test if CORS is properly configured."""

    response = requests.options(
        "/api/users",
        headers={"Origin": "https://evil.com"}
    )

    # Should not allow all origins
    allow_origin = response.headers.get("Access-Control-Allow-Origin")

    assert allow_origin != "*", "CORS allows all origins!"
    assert allow_origin != "https://evil.com", "CORS allows untrusted origin!"

    print("✓ CORS properly configured")
```

---

### 9. Improper Inventory Management

**Description:** API doesn't track and limit API versions/endpoints.

**Test Cases:**

```python
def test_deprecated_endpoints():
    """Test if deprecated API versions are disabled."""

    # Try old API version
    response = requests.get("/api/v1/users")  # Assume v1 is deprecated

    # Should return 410 Gone or 404
    assert response.status_code in [404, 410], "Deprecated endpoint still accessible!"

    print("✓ Deprecated endpoints disabled")
```

---

### 10. Unsafe Consumption of APIs

**Description:** API doesn't validate responses from third-party APIs.

**Test Cases:**

```python
def test_third_party_api_validation():
    """Test if API validates third-party responses."""

    # This test would require mocking third-party API
    # to return malicious data

    # Example: API fetches user data from external service
    # and should validate it before using
```

---

## Additional Security Tests

### SQL Injection

```python
def test_sql_injection():
    """Test if API is vulnerable to SQL injection."""

    sql_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users;--",
        "' UNION SELECT * FROM users--"
    ]

    for payload in sql_payloads:
        response = requests.get(
            f"/api/users?name={payload}"
        )

        # Should not return SQL errors
        assert "sql" not in response.text.lower(), "SQL injection vulnerability!"
        assert "syntax" not in response.text.lower()

    print("✓ SQL injection protection active")
```

### XSS (Cross-Site Scripting)

```python
def test_xss_vulnerability():
    """Test if API sanitizes user input."""

    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')"
    ]

    for payload in xss_payloads:
        response = requests.post(
            "/api/comments",
            json={"text": payload},
            headers={"Authorization": f"Bearer {user_token}"}
        )

        # Get comment back
        if response.status_code == 201:
            comment_id = response.json()["id"]
            get_response = requests.get(f"/api/comments/{comment_id}")

            comment_text = get_response.json()["text"]

            # Should be escaped/sanitized
            assert "<script>" not in comment_text, "XSS vulnerability: script tag not escaped!"

    print("✓ XSS protection active")
```

### Sensitive Data Exposure

```python
def test_password_in_response():
    """Test if API returns password hashes."""

    response = requests.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    user = response.json()

    # Should not include password field
    assert "password" not in user, "Password field exposed in API response!"
    assert "password_hash" not in user, "Password hash exposed!"

    print("✓ Passwords not exposed")


def test_https_enforcement():
    """Test if API enforces HTTPS."""

    # Try HTTP request
    try:
        response = requests.get(
            "http://api.example.com/users",  # HTTP, not HTTPS
            allow_redirects=False
        )

        # Should redirect to HTTPS or reject
        assert response.status_code in [301, 302, 403], "HTTP not redirected to HTTPS!"

    except requests.exceptions.SSLError:
        print("✓ HTTPS enforced")
```

---

## Security Testing Checklist

### Authentication & Authorization

- [ ] Weak password policy tested
- [ ] Brute force protection tested
- [ ] JWT expiration tested
- [ ] Token refresh tested
- [ ] BOLA (object-level auth) tested
- [ ] Function-level auth tested
- [ ] Admin endpoints protected

### Input Validation

- [ ] SQL injection tested
- [ ] XSS tested
- [ ] Mass assignment tested
- [ ] Field validation tested
- [ ] Boundary values tested

### Rate Limiting & DoS

- [ ] Rate limiting tested
- [ ] Pagination limits tested
- [ ] Request size limits tested
- [ ] Query complexity limits tested (GraphQL)

### Data Protection

- [ ] Passwords not exposed
- [ ] Sensitive fields redacted
- [ ] HTTPS enforced
- [ ] Proper encryption used

### Security Headers

- [ ] X-Content-Type-Options
- [ ] X-Frame-Options
- [ ] Strict-Transport-Security
- [ ] Content-Security-Policy
- [ ] CORS properly configured

### Error Handling

- [ ] No stack traces in errors
- [ ] No file paths exposed
- [ ] No database details leaked
- [ ] Consistent error format

---

## Tools for Security Testing

### Python Libraries

```bash
pip install requests pytest safety bandit
```

### Security Scanners

- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Security testing platform
- **Postman**: API testing with security checks
- **Safety**: Check Python dependencies for vulnerabilities
- **Bandit**: Security linter for Python code

---

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [API Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/12-API_Testing/)
- [JWT Security Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [GraphQL Security](https://escape.tech/blog/graphql-input-validation-and-sanitization/)
