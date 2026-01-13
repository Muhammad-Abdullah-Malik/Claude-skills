import requests
import json
from datetime import datetime
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
        start_time = datetime.now()
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=req_headers,
            json=data if data else None,
            timeout=30
        )
        end_time = datetime.now()

        # Validate response
        result = {
            "success": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text,
            "time_ms": (end_time - start_time).total_seconds() * 1000,
            "timestamp": start_time.isoformat()
        }

        return result

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def validate_product_response(response_body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate product API response structure.
    """
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    # Check required fields
    required_fields = ["id", "title", "price"]
    for field in required_fields:
        if field not in response_body:
            validation_results["valid"] = False
            validation_results["errors"].append(f"Missing required field: {field}")

    # Check data types
    if "id" in response_body and not isinstance(response_body["id"], int):
        validation_results["errors"].append("Field 'id' should be an integer")

    if "price" in response_body and not isinstance(response_body["price"], (int, float)):
        validation_results["errors"].append("Field 'price' should be a number")

    if "title" in response_body and not isinstance(response_body["title"], str):
        validation_results["errors"].append("Field 'title' should be a string")

    return validation_results

def generate_report(result: Dict[str, Any], validation: Dict[str, Any]) -> str:
    """
    Generate a detailed test report.
    """
    report = []
    report.append("=" * 60)
    report.append("API TEST REPORT")
    report.append("=" * 60)
    report.append(f"\nTimestamp: {result.get('timestamp', 'N/A')}")
    report.append(f"URL: https://dummyjson.com/products/1")
    report.append(f"Method: GET")
    report.append(f"\n--- RESPONSE ---")
    report.append(f"Status Code: {result.get('status_code', 'N/A')}")
    report.append(f"Success: {result.get('success', False)}")
    report.append(f"Response Time: {result.get('time_ms', 0):.2f} ms")

    if result.get('success'):
        report.append(f"\n--- RESPONSE BODY ---")
        report.append(json.dumps(result.get('body', {}), indent=2))

        report.append(f"\n--- VALIDATION RESULTS ---")
        if validation['valid']:
            report.append("[PASS] Response structure is valid")
        else:
            report.append("[FAIL] Response validation failed")
            for error in validation['errors']:
                report.append(f"  - {error}")

        if validation['warnings']:
            report.append("\nWarnings:")
            for warning in validation['warnings']:
                report.append(f"  - {warning}")
    else:
        report.append(f"\n--- ERROR ---")
        report.append(f"Error: {result.get('error', 'Unknown error')}")

    report.append("\n" + "=" * 60)
    return "\n".join(report)

if __name__ == "__main__":
    # Test the DummyJSON products API
    print("Testing API: https://dummyjson.com/products/1\n")

    # Execute test
    result = test_api_endpoint(
        url="https://dummyjson.com/products/1",
        method="GET"
    )

    # Validate response
    validation = {"valid": True, "errors": [], "warnings": []}
    if result.get('success') and isinstance(result.get('body'), dict):
        validation = validate_product_response(result['body'])

    # Generate and print report
    report = generate_report(result, validation)
    print(report)

    # Save report to file
    with open("api_test_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n[SUCCESS] Report saved to: api_test_report.txt")
