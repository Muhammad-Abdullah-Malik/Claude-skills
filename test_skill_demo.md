# API Testing Skill - Quick Test Guide

## Step 1: Install Dependencies

```bash
cd ".claude/skills/api-testing-suite"
pip install -r scripts/requirements.txt
```

## Step 2: Test Single API Endpoint

```bash
# Test GET request
python scripts/test_api.py \
  --url "https://jsonplaceholder.typicode.com/users" \
  --method GET

# Test specific user
python scripts/test_api.py \
  --url "https://jsonplaceholder.typicode.com/users/1" \
  --method GET

# Test POST request
python scripts/test_api.py \
  --url "https://jsonplaceholder.typicode.com/posts" \
  --method POST \
  --data '{"title":"Test Post","body":"Test content","userId":1}'
```

## Step 3: Test with Config File

Create `test_config.json`:

```json
{
  "base_url": "https://jsonplaceholder.typicode.com",
  "tests": [
    {
      "name": "Get all users",
      "url": "/users",
      "method": "GET",
      "expected_status": 200
    },
    {
      "name": "Get user 1",
      "url": "/users/1",
      "method": "GET",
      "expected_status": 200
    },
    {
      "name": "Create post",
      "url": "/posts",
      "method": "POST",
      "data": {
        "title": "Test",
        "body": "Content",
        "userId": 1
      },
      "expected_status": 201
    }
  ]
}
```

Then run:

```bash
python scripts/test_api.py --config test_config.json --verbose
```

## Step 4: Security Testing

```bash
python scripts/security_test.py \
  --url "https://jsonplaceholder.typicode.com"
```

## Step 5: View Results

Results are saved to:
- `test_results.json` - API test results
- `security_report.json` - Security test results
