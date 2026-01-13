#!/usr/bin/env python3
"""
Comprehensive API Testing for JSONPlaceholder Users API
Target: https://jsonplaceholder.typicode.com/users
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class JSONPlaceholderTester:
    """Comprehensive tester for JSONPlaceholder API."""

    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def log_test(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Log test result."""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "PASS"
            icon = "[OK]"
        else:
            self.failed_tests += 1
            status = "FAIL"
            icon = "[X]"

        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)

        print(f"{icon} {test_name}")
        if not passed and "error" in details:
            print(f"    Error: {details['error']}")

    def test_get_all_users(self):
        """Test GET /users - retrieve all users."""
        print("\n[Test 1] GET All Users")

        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/users", timeout=10)
            duration = (time.time() - start_time) * 1000

            # Validate status code
            status_ok = response.status_code == 200

            # Validate response is JSON array
            users = response.json()
            is_array = isinstance(users, list)

            # Validate we have users
            has_users = len(users) > 0

            # Validate first user structure
            first_user = users[0] if users else {}
            required_fields = ["id", "name", "username", "email"]
            has_required_fields = all(field in first_user for field in required_fields)

            passed = status_ok and is_array and has_users and has_required_fields

            self.log_test("GET /users", passed, {
                "status_code": response.status_code,
                "response_time_ms": round(duration, 2),
                "user_count": len(users),
                "has_required_fields": has_required_fields,
                "sample_user": first_user.get("name", "N/A")
            })

            return users

        except Exception as e:
            self.log_test("GET /users", False, {"error": str(e)})
            return []

    def test_get_single_user(self):
        """Test GET /users/{id} - retrieve specific user."""
        print("\n[Test 2] GET Single User")

        try:
            user_id = 1
            start_time = time.time()
            response = requests.get(f"{self.base_url}/users/{user_id}", timeout=10)
            duration = (time.time() - start_time) * 1000

            status_ok = response.status_code == 200
            user = response.json()

            # Validate user structure
            required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
            has_all_fields = all(field in user for field in required_fields)

            # Validate nested objects
            has_address = "address" in user and "city" in user.get("address", {})
            has_company = "company" in user and "name" in user.get("company", {})

            passed = status_ok and has_all_fields and has_address and has_company

            self.log_test(f"GET /users/{user_id}", passed, {
                "status_code": response.status_code,
                "response_time_ms": round(duration, 2),
                "user_name": user.get("name"),
                "user_email": user.get("email"),
                "has_all_fields": has_all_fields,
                "has_nested_objects": has_address and has_company
            })

        except Exception as e:
            self.log_test(f"GET /users/{user_id}", False, {"error": str(e)})

    def test_get_invalid_user(self):
        """Test GET /users/{id} with invalid ID - should return 404."""
        print("\n[Test 3] GET Invalid User (404 Test)")

        try:
            invalid_id = 99999
            response = requests.get(f"{self.base_url}/users/{invalid_id}", timeout=10)

            # JSONPlaceholder returns 404 for non-existent users
            # But actually it returns empty object with 200, let's check
            passed = response.status_code in [404, 200]

            if response.status_code == 200:
                data = response.json()
                # Empty object means not found
                passed = data == {}

            self.log_test(f"GET /users/{invalid_id} (404 test)", passed, {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else None,
                "note": "JSONPlaceholder returns empty object for invalid IDs"
            })

        except Exception as e:
            self.log_test("GET invalid user", False, {"error": str(e)})

    def test_post_create_user(self):
        """Test POST /users - create new user."""
        print("\n[Test 4] POST Create User")

        try:
            new_user = {
                "name": "Abdullah Test",
                "username": "abdullah_test",
                "email": "abdullah@test.com",
                "phone": "123-456-7890",
                "website": "abdullah.test"
            }

            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/users",
                json=new_user,
                timeout=10
            )
            duration = (time.time() - start_time) * 1000

            # JSONPlaceholder returns 201 Created
            status_ok = response.status_code == 201

            created_user = response.json()

            # Validate created user has ID
            has_id = "id" in created_user

            # Validate data was echoed back
            name_matches = created_user.get("name") == new_user["name"]
            email_matches = created_user.get("email") == new_user["email"]

            passed = status_ok and has_id and name_matches and email_matches

            self.log_test("POST /users (create)", passed, {
                "status_code": response.status_code,
                "response_time_ms": round(duration, 2),
                "created_id": created_user.get("id"),
                "created_name": created_user.get("name"),
                "data_validation": "Data echoed correctly" if name_matches else "Data mismatch"
            })

        except Exception as e:
            self.log_test("POST /users", False, {"error": str(e)})

    def test_put_update_user(self):
        """Test PUT /users/{id} - update user."""
        print("\n[Test 5] PUT Update User")

        try:
            user_id = 1
            updated_data = {
                "id": user_id,
                "name": "Updated Name",
                "username": "updated_user",
                "email": "updated@test.com"
            }

            response = requests.put(
                f"{self.base_url}/users/{user_id}",
                json=updated_data,
                timeout=10
            )

            status_ok = response.status_code == 200
            updated_user = response.json()

            name_updated = updated_user.get("name") == updated_data["name"]

            passed = status_ok and name_updated

            self.log_test(f"PUT /users/{user_id} (update)", passed, {
                "status_code": response.status_code,
                "updated_name": updated_user.get("name"),
                "update_successful": name_updated
            })

        except Exception as e:
            self.log_test("PUT /users", False, {"error": str(e)})

    def test_patch_partial_update(self):
        """Test PATCH /users/{id} - partial update."""
        print("\n[Test 6] PATCH Partial Update")

        try:
            user_id = 1
            partial_data = {
                "email": "patched@test.com"
            }

            response = requests.patch(
                f"{self.base_url}/users/{user_id}",
                json=partial_data,
                timeout=10
            )

            status_ok = response.status_code == 200
            patched_user = response.json()

            email_updated = patched_user.get("email") == partial_data["email"]

            passed = status_ok and email_updated

            self.log_test(f"PATCH /users/{user_id} (partial)", passed, {
                "status_code": response.status_code,
                "patched_email": patched_user.get("email")
            })

        except Exception as e:
            self.log_test("PATCH /users", False, {"error": str(e)})

    def test_delete_user(self):
        """Test DELETE /users/{id} - delete user."""
        print("\n[Test 7] DELETE User")

        try:
            user_id = 1
            response = requests.delete(f"{self.base_url}/users/{user_id}", timeout=10)

            # JSONPlaceholder returns 200 for successful delete
            status_ok = response.status_code == 200

            passed = status_ok

            self.log_test(f"DELETE /users/{user_id}", passed, {
                "status_code": response.status_code,
                "note": "JSONPlaceholder simulates deletion (doesn't actually delete)"
            })

        except Exception as e:
            self.log_test("DELETE /users", False, {"error": str(e)})

    def test_response_headers(self):
        """Test response headers."""
        print("\n[Test 8] Response Headers Validation")

        try:
            response = requests.get(f"{self.base_url}/users/1", timeout=10)

            headers = response.headers

            # Check important headers
            has_content_type = "content-type" in headers
            is_json = "application/json" in headers.get("content-type", "").lower()
            has_cors = "access-control-allow-origin" in headers

            passed = has_content_type and is_json

            self.log_test("Response Headers", passed, {
                "content_type": headers.get("content-type"),
                "has_cors": has_cors,
                "cors_origin": headers.get("access-control-allow-origin", "Not set")
            })

        except Exception as e:
            self.log_test("Response Headers", False, {"error": str(e)})

    def test_response_time(self):
        """Test API response time."""
        print("\n[Test 9] Response Time Performance")

        try:
            times = []

            for i in range(5):
                start = time.time()
                response = requests.get(f"{self.base_url}/users", timeout=10)
                duration = (time.time() - start) * 1000
                times.append(duration)

            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            # Consider good if average < 2 seconds
            passed = avg_time < 2000

            self.log_test("Response Time Performance", passed, {
                "average_ms": round(avg_time, 2),
                "min_ms": round(min_time, 2),
                "max_ms": round(max_time, 2),
                "samples": 5
            })

        except Exception as e:
            self.log_test("Response Time", False, {"error": str(e)})

    def test_data_validation(self):
        """Test data type validation."""
        print("\n[Test 10] Data Type Validation")

        try:
            response = requests.get(f"{self.base_url}/users/1", timeout=10)
            user = response.json()

            # Validate data types
            id_is_int = isinstance(user.get("id"), int)
            name_is_str = isinstance(user.get("name"), str)
            email_is_str = isinstance(user.get("email"), str)
            address_is_dict = isinstance(user.get("address"), dict)

            # Validate email format
            email = user.get("email", "")
            email_has_at = "@" in email
            email_has_dot = "." in email

            passed = all([id_is_int, name_is_str, email_is_str, address_is_dict, email_has_at, email_has_dot])

            self.log_test("Data Type Validation", passed, {
                "id_type": type(user.get("id")).__name__,
                "name_type": type(user.get("name")).__name__,
                "email_format": "Valid" if email_has_at and email_has_dot else "Invalid",
                "address_type": type(user.get("address")).__name__
            })

        except Exception as e:
            self.log_test("Data Validation", False, {"error": str(e)})

    def generate_report(self):
        """Generate final test report."""
        print("\n" + "=" * 70)
        print("COMPREHENSIVE API TEST REPORT")
        print("=" * 70)
        print(f"Target API: {self.base_url}/users")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Pass Rate: {(self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0:.1f}%")
        print("=" * 70)

        # Save to JSON
        report = {
            "api": f"{self.base_url}/users",
            "test_date": datetime.now().isoformat(),
            "summary": {
                "total": self.total_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "pass_rate": f"{(self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0:.1f}%"
            },
            "results": self.results
        }

        with open("jsonplaceholder_test_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\nDetailed report saved to: jsonplaceholder_test_report.json")

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 70)
        print("COMPREHENSIVE API TESTING - JSONPlaceholder Users API")
        print("=" * 70)

        self.test_get_all_users()
        self.test_get_single_user()
        self.test_get_invalid_user()
        self.test_post_create_user()
        self.test_put_update_user()
        self.test_patch_partial_update()
        self.test_delete_user()
        self.test_response_headers()
        self.test_response_time()
        self.test_data_validation()

        self.generate_report()


if __name__ == "__main__":
    tester = JSONPlaceholderTester()
    tester.run_all_tests()
