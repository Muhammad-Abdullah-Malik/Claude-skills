#!/usr/bin/env python3
"""
API Testing Script

Usage:
    python test_api.py --url https://api.example.com/endpoint --method GET
    python test_api.py --url https://api.example.com/users --method POST --data '{"name":"John"}'
    python test_api.py --config config.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError


class APITester:
    """Main API testing class."""

    def __init__(self, base_url: str = None, auth_token: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "")
        self.auth_token = auth_token or os.getenv("JWT_TOKEN")
        self.api_key = api_key or os.getenv("API_KEY")
        self.session = requests.Session()
        self.results = []

        # Set default headers
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def test_endpoint(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        expected_status: int = None
    ) -> Dict[str, Any]:
        """
        Test an API endpoint.

        Args:
            url: Full URL or path (if base_url is set)
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            headers: Additional headers
            data: Request body (will be JSON-encoded)
            params: Query parameters
            timeout: Request timeout in seconds
            expected_status: Expected HTTP status code

        Returns:
            Dict with test results
        """
        # Build full URL
        if url.startswith("http"):
            full_url = url
        else:
            full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"

        # Merge headers
        req_headers = dict(self.session.headers)
        if headers:
            req_headers.update(headers)

        # Prepare request
        start_time = datetime.now()

        try:
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                headers=req_headers,
                json=data if data else None,
                params=params,
                timeout=timeout
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() * 1000  # ms

            # Parse response
            try:
                response_body = response.json()
            except:
                response_body = response.text

            result = {
                "success": True,
                "url": full_url,
                "method": method.upper(),
                "status_code": response.status_code,
                "duration_ms": round(duration, 2),
                "headers": dict(response.headers),
                "body": response_body,
                "timestamp": start_time.isoformat()
            }

            # Check expected status
            if expected_status and response.status_code != expected_status:
                result["success"] = False
                result["error"] = f"Expected status {expected_status}, got {response.status_code}"

            # Check for successful status codes
            if not (200 <= response.status_code < 300):
                result["success"] = False
                if "error" not in result:
                    result["error"] = f"Non-success status code: {response.status_code}"

            self.results.append(result)
            return result

        except Timeout:
            result = {
                "success": False,
                "url": full_url,
                "method": method.upper(),
                "error": "Request timeout",
                "timestamp": start_time.isoformat()
            }
            self.results.append(result)
            return result

        except ConnectionError:
            result = {
                "success": False,
                "url": full_url,
                "method": method.upper(),
                "error": "Connection error",
                "timestamp": start_time.isoformat()
            }
            self.results.append(result)
            return result

        except Exception as e:
            result = {
                "success": False,
                "url": full_url,
                "method": method.upper(),
                "error": str(e),
                "timestamp": start_time.isoformat()
            }
            self.results.append(result)
            return result

    def print_result(self, result: Dict[str, Any]):
        """Print test result in a readable format."""
        success_icon = "✓" if result.get("success") else "✗"
        status = result.get("status_code", "N/A")
        duration = result.get("duration_ms", "N/A")

        print(f"\n{success_icon} {result['method']} {result['url']}")
        print(f"  Status: {status}")

        if duration != "N/A":
            print(f"  Duration: {duration}ms")

        if not result.get("success"):
            print(f"  Error: {result.get('error', 'Unknown error')}")

        if result.get("body"):
            body = result["body"]
            if isinstance(body, dict) or isinstance(body, list):
                print(f"  Response: {json.dumps(body, indent=2)[:500]}...")
            else:
                print(f"  Response: {str(body)[:500]}...")

    def save_results(self, filename: str = "test_results.json"):
        """Save test results to a JSON file."""
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Results saved to {filename}")

    def generate_report(self):
        """Generate a summary report."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("success"))
        failed = total - passed

        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Pass Rate: {(passed/total*100) if total > 0 else 0:.1f}%")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="API Testing Tool")

    # Single test mode
    parser.add_argument("--url", help="API endpoint URL")
    parser.add_argument("--method", default="GET", help="HTTP method (GET, POST, PUT, DELETE)")
    parser.add_argument("--data", help="Request body as JSON string")
    parser.add_argument("--headers", help="Additional headers as JSON string")
    parser.add_argument("--params", help="Query parameters as JSON string")
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--expected-status", type=int, help="Expected HTTP status code")

    # Config file mode
    parser.add_argument("--config", help="Path to configuration JSON file")

    # Output options
    parser.add_argument("--output", default="test_results.json", help="Output file for results")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Initialize tester
    tester = APITester(auth_token=args.token, api_key=args.api_key)

    # Config file mode
    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)

        if "base_url" in config:
            tester.base_url = config["base_url"]

        tests = config.get("tests", [])

        print(f"Running {len(tests)} tests from config file...\n")

        for test in tests:
            result = tester.test_endpoint(
                url=test.get("url"),
                method=test.get("method", "GET"),
                headers=test.get("headers"),
                data=test.get("data"),
                params=test.get("params"),
                expected_status=test.get("expected_status")
            )

            if args.verbose:
                tester.print_result(result)

    # Single test mode
    elif args.url:
        # Parse optional JSON arguments
        data = json.loads(args.data) if args.data else None
        headers = json.loads(args.headers) if args.headers else None
        params = json.loads(args.params) if args.params else None

        result = tester.test_endpoint(
            url=args.url,
            method=args.method,
            headers=headers,
            data=data,
            params=params,
            expected_status=args.expected_status
        )

        tester.print_result(result)

    else:
        parser.print_help()
        sys.exit(1)

    # Generate report and save results
    tester.generate_report()
    tester.save_results(args.output)


if __name__ == "__main__":
    main()
