#!/usr/bin/env python3
"""
API Security Testing Script

Tests for OWASP API Security Top 10 vulnerabilities.

Usage:
    python security_test.py --url https://api.example.com --token YOUR_JWT_TOKEN
    python security_test.py --config security_config.json
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any
import requests


class SecurityTester:
    """API security testing class."""

    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.vulnerabilities = []
        self.session = requests.Session()

        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

    def log_vulnerability(self, test_name: str, severity: str, description: str, details: Dict = None):
        """Log a security vulnerability."""
        vuln = {
            "test": test_name,
            "severity": severity,  # Critical, High, Medium, Low
            "description": description,
            "details": details or {}
        }
        self.vulnerabilities.append(vuln)

        # Print vulnerability
        severity_icon = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢"
        }
        icon = severity_icon.get(severity, "⚪")

        print(f"\n{icon} {severity} - {test_name}")
        print(f"   {description}")
        if details:
            print(f"   Details: {json.dumps(details, indent=2)[:200]}")

    def test_broken_authentication(self):
        """Test for weak authentication mechanisms."""
        print("\n🔐 Testing Authentication Security...")

        # Test 1: Weak password acceptance
        weak_passwords = ["123", "password", "abc"]

        for weak_pass in weak_passwords:
            try:
                response = requests.post(
                    f"{self.base_url}/register",
                    json={"email": f"test_{weak_pass}@test.com", "password": weak_pass},
                    timeout=10
                )

                if response.status_code == 201:
                    self.log_vulnerability(
                        "Weak Password Policy",
                        "High",
                        f"API accepts weak password: '{weak_pass}'",
                        {"password": weak_pass}
                    )
            except:
                pass

        # Test 2: No rate limiting on login
        failed_attempts = 0
        for i in range(10):
            try:
                response = requests.post(
                    f"{self.base_url}/login",
                    json={"email": "test@test.com", "password": "wrong"},
                    timeout=5
                )

                if response.status_code != 429:
                    failed_attempts += 1
            except:
                break

        if failed_attempts >= 5:
            self.log_vulnerability(
                "No Brute Force Protection",
                "Critical",
                f"Successfully made {failed_attempts} failed login attempts without rate limiting"
            )

        print("✓ Authentication tests complete")

    def test_broken_object_level_authorization(self):
        """Test for BOLA vulnerabilities."""
        print("\n🔒 Testing Object-Level Authorization...")

        # Test accessing other users' resources
        test_ids = [1, 999, "abc", "../admin"]

        for test_id in test_ids:
            try:
                response = self.session.get(
                    f"{self.base_url}/users/{test_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    # Check if we got data we shouldn't have access to
                    data = response.json()
                    if "id" in data and str(data["id"]) == str(test_id):
                        self.log_vulnerability(
                            "BOLA - Broken Object Level Authorization",
                            "Critical",
                            f"Able to access user {test_id} without proper authorization",
                            {"endpoint": f"/users/{test_id}", "status": 200}
                        )
            except:
                pass

        print("✓ BOLA tests complete")

    def test_sql_injection(self):
        """Test for SQL injection vulnerabilities."""
        print("\n💉 Testing SQL Injection...")

        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users;--",
            "' UNION SELECT * FROM users--",
            "admin'--"
        ]

        endpoints = ["/users", "/search", "/login"]

        for endpoint in endpoints:
            for payload in sql_payloads:
                try:
                    # Test in query parameter
                    response = requests.get(
                        f"{self.base_url}{endpoint}",
                        params={"q": payload},
                        timeout=10
                    )

                    error_keywords = ["sql", "syntax", "mysql", "postgresql", "database error"]

                    if any(keyword in response.text.lower() for keyword in error_keywords):
                        self.log_vulnerability(
                            "SQL Injection",
                            "Critical",
                            f"Potential SQL injection at {endpoint}",
                            {"payload": payload, "endpoint": endpoint}
                        )
                except:
                    pass

        print("✓ SQL injection tests complete")

    def test_xss(self):
        """Test for XSS vulnerabilities."""
        print("\n🎭 Testing XSS (Cross-Site Scripting)...")

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]

        # Try to create resources with XSS payloads
        for payload in xss_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/comments",
                    json={"text": payload},
                    timeout=10
                )

                if response.status_code == 201:
                    # Retrieve and check if payload is escaped
                    comment_id = response.json().get("id")
                    if comment_id:
                        get_response = self.session.get(
                            f"{self.base_url}/comments/{comment_id}",
                            timeout=10
                        )

                        if get_response.status_code == 200:
                            comment_text = get_response.json().get("text", "")

                            if "<script>" in comment_text or "onerror=" in comment_text:
                                self.log_vulnerability(
                                    "XSS - Cross-Site Scripting",
                                    "High",
                                    "XSS payload not properly escaped",
                                    {"payload": payload}
                                )
            except:
                pass

        print("✓ XSS tests complete")

    def test_security_headers(self):
        """Test for missing security headers."""
        print("\n🛡️  Testing Security Headers...")

        try:
            response = requests.get(f"{self.base_url}/", timeout=10)

            required_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                "Strict-Transport-Security": "max-age",
                "Content-Security-Policy": None
            }

            for header, expected in required_headers.items():
                if header not in response.headers:
                    self.log_vulnerability(
                        "Missing Security Header",
                        "Medium",
                        f"Missing security header: {header}"
                    )
                elif expected:
                    header_value = response.headers[header]
                    if isinstance(expected, list):
                        if not any(exp in header_value for exp in expected):
                            self.log_vulnerability(
                                "Incorrect Security Header",
                                "Medium",
                                f"Header {header} has incorrect value: {header_value}"
                            )
                    elif expected not in header_value:
                        self.log_vulnerability(
                            "Incorrect Security Header",
                            "Medium",
                            f"Header {header} has incorrect value: {header_value}"
                        )

        except Exception as e:
            print(f"   Error testing security headers: {e}")

        print("✓ Security headers tests complete")

    def test_rate_limiting(self):
        """Test for rate limiting."""
        print("\n⏱️  Testing Rate Limiting...")

        rate_limited = False

        for i in range(100):
            try:
                response = requests.get(f"{self.base_url}/users", timeout=5)

                if response.status_code == 429:
                    rate_limited = True
                    print(f"   ✓ Rate limited after {i} requests")
                    break
            except:
                break

        if not rate_limited:
            self.log_vulnerability(
                "No Rate Limiting",
                "High",
                "No rate limiting detected after 100 requests"
            )

        print("✓ Rate limiting tests complete")

    def test_https_enforcement(self):
        """Test if HTTPS is enforced."""
        print("\n🔐 Testing HTTPS Enforcement...")

        # Try HTTP version
        if self.base_url.startswith("https://"):
            http_url = self.base_url.replace("https://", "http://")

            try:
                response = requests.get(http_url, allow_redirects=False, timeout=10)

                if response.status_code not in [301, 302, 308, 403]:
                    self.log_vulnerability(
                        "HTTPS Not Enforced",
                        "Critical",
                        "API accessible over HTTP without redirect to HTTPS"
                    )
                else:
                    print("   ✓ HTTPS properly enforced")
            except:
                print("   ✓ HTTP connection refused (HTTPS enforced)")

        print("✓ HTTPS tests complete")

    def test_sensitive_data_exposure(self):
        """Test for sensitive data in responses."""
        print("\n🔍 Testing Sensitive Data Exposure...")

        try:
            response = self.session.get(f"{self.base_url}/users/me", timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Check for password fields
                sensitive_fields = ["password", "password_hash", "secret", "api_key", "token"]

                for field in sensitive_fields:
                    if field in data or field in str(data).lower():
                        self.log_vulnerability(
                            "Sensitive Data Exposure",
                            "Critical",
                            f"Sensitive field '{field}' exposed in API response"
                        )
        except:
            pass

        print("✓ Sensitive data tests complete")

    def run_all_tests(self):
        """Run all security tests."""
        print("\n" + "=" * 60)
        print("API SECURITY TESTING")
        print("=" * 60)
        print(f"Target: {self.base_url}")
        print("=" * 60)

        # Run all tests
        self.test_broken_authentication()
        self.test_broken_object_level_authorization()
        self.test_sql_injection()
        self.test_xss()
        self.test_security_headers()
        self.test_rate_limiting()
        self.test_https_enforcement()
        self.test_sensitive_data_exposure()

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate security test report."""
        print("\n" + "=" * 60)
        print("SECURITY REPORT")
        print("=" * 60)

        if not self.vulnerabilities:
            print("✓ No vulnerabilities found!")
        else:
            severity_counts = {
                "Critical": 0,
                "High": 0,
                "Medium": 0,
                "Low": 0
            }

            for vuln in self.vulnerabilities:
                severity_counts[vuln["severity"]] += 1

            print(f"Total Vulnerabilities: {len(self.vulnerabilities)}")
            print(f"  Critical: {severity_counts['Critical']}")
            print(f"  High: {severity_counts['High']}")
            print(f"  Medium: {severity_counts['Medium']}")
            print(f"  Low: {severity_counts['Low']}")

        print("=" * 60)

        # Save report
        with open("security_report.json", "w") as f:
            json.dump(self.vulnerabilities, f, indent=2)

        print("\n✓ Report saved to security_report.json")


def main():
    parser = argparse.ArgumentParser(description="API Security Testing Tool")

    parser.add_argument("--url", help="Base URL of the API to test")
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--config", help="Path to configuration JSON file")

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)

        base_url = config.get("base_url")
        auth_token = config.get("auth_token")
    elif args.url:
        base_url = args.url
        auth_token = args.token or os.getenv("JWT_TOKEN")
    else:
        parser.print_help()
        sys.exit(1)

    # Run security tests
    tester = SecurityTester(base_url, auth_token)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
