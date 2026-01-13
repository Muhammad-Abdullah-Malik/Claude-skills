# GraphQL API Concepts

## What is GraphQL?

GraphQL is a query language for APIs and a runtime for executing those queries. Unlike REST, clients can request exactly the data they need in a single request.

## Key Differences: GraphQL vs REST

| Feature | REST | GraphQL |
|---------|------|---------|
| Endpoints | Multiple endpoints | Single endpoint |
| Data fetching | Fixed response structure | Client specifies fields |
| Over-fetching | Common | Eliminated |
| Under-fetching | Requires multiple requests | Single request |
| Versioning | URL versioning | Schema evolution |

## GraphQL Operations

### 1. Queries (Read Data)

```graphql
# Simple query
query {
  user(id: "123") {
    id
    name
    email
  }
}
```

With variables:

```graphql
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
    name
    email
    posts {
      title
      createdAt
    }
  }
}
```

Variables (sent separately):

```json
{
  "userId": "123"
}
```

### 2. Mutations (Modify Data)

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

Variables:

```json
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### 3. Subscriptions (Real-time Updates)

```graphql
subscription OnUserCreated {
  userCreated {
    id
    name
    email
  }
}
```

## GraphQL Schema

### Type Definitions

```graphql
type User {
  id: ID!              # Non-null ID
  name: String!        # Non-null String
  email: String!
  age: Int
  posts: [Post!]!      # Non-null array of non-null Posts
  profile: Profile
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
  createdAt: DateTime!
}

type Profile {
  bio: String
  avatar: String
  website: String
}
```

### Input Types

```graphql
input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

input UpdateUserInput {
  name: String
  email: String
  age: Int
}
```

### Enums

```graphql
enum UserRole {
  ADMIN
  USER
  GUEST
}

type User {
  id: ID!
  name: String!
  role: UserRole!
}
```

### Interfaces

```graphql
interface Node {
  id: ID!
  createdAt: DateTime!
}

type User implements Node {
  id: ID!
  createdAt: DateTime!
  name: String!
}

type Post implements Node {
  id: ID!
  createdAt: DateTime!
  title: String!
}
```

## GraphQL Request Format

### HTTP POST Request

```http
POST /graphql HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "query GetUser($id: ID!) { user(id: $id) { name email } }",
  "variables": {
    "id": "123"
  },
  "operationName": "GetUser"
}
```

### Python Example

```python
import requests

query = """
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      title
    }
  }
}
"""

variables = {"id": "123"}

response = requests.post(
    "https://api.example.com/graphql",
    json={
        "query": query,
        "variables": variables
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer <token>"
    }
)

data = response.json()
```

## GraphQL Response Format

### Success Response

```json
{
  "data": {
    "user": {
      "id": "123",
      "name": "John Doe",
      "email": "john@example.com",
      "posts": [
        {
          "title": "First Post"
        }
      ]
    }
  }
}
```

### Error Response

```json
{
  "errors": [
    {
      "message": "User not found",
      "locations": [{"line": 2, "column": 3}],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ],
  "data": null
}
```

### Partial Success (Some fields failed)

```json
{
  "data": {
    "user": {
      "id": "123",
      "name": "John Doe",
      "posts": null
    }
  },
  "errors": [
    {
      "message": "Failed to fetch posts",
      "path": ["user", "posts"]
    }
  ]
}
```

## Advanced Features

### 1. Aliases

Request same field multiple times with different arguments:

```graphql
{
  admin: user(id: "1") {
    name
  }
  guest: user(id: "2") {
    name
  }
}
```

Response:

```json
{
  "data": {
    "admin": {"name": "Admin User"},
    "guest": {"name": "Guest User"}
  }
}
```

### 2. Fragments

Reusable field sets:

```graphql
fragment UserFields on User {
  id
  name
  email
}

query {
  user1: user(id: "1") {
    ...UserFields
  }
  user2: user(id: "2") {
    ...UserFields
  }
}
```

### 3. Directives

Conditionally include/skip fields:

```graphql
query GetUser($id: ID!, $withPosts: Boolean!) {
  user(id: $id) {
    name
    email
    posts @include(if: $withPosts) {
      title
    }
  }
}
```

Common directives:
- `@include(if: Boolean)` - Include field if true
- `@skip(if: Boolean)` - Skip field if true
- `@deprecated(reason: String)` - Mark field as deprecated

### 4. Introspection

Query the schema itself:

```graphql
{
  __schema {
    types {
      name
      kind
    }
  }
}
```

Get specific type info:

```graphql
{
  __type(name: "User") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

## Testing GraphQL APIs

### Key Test Scenarios

1. **Valid Queries**: Successful data retrieval
2. **Invalid Queries**: Syntax errors, unknown fields
3. **Validation**: Type mismatches, required fields
4. **Authentication**: Protected queries/mutations
5. **Authorization**: Field-level permissions
6. **Error Handling**: Server errors, null handling
7. **Schema Validation**: Type safety, required fields
8. **Complexity Limits**: Query depth, breadth

### Example Test Cases

```python
import requests

GRAPHQL_URL = "https://api.example.com/graphql"

def test_valid_query():
    """Test successful query."""
    query = """
    query {
      user(id: "123") {
        name
        email
      }
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        json={"query": query}
    )

    data = response.json()
    assert "errors" not in data
    assert data["data"]["user"]["name"] is not None


def test_invalid_field():
    """Test query with non-existent field."""
    query = """
    query {
      user(id: "123") {
        invalidField
      }
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        json={"query": query}
    )

    data = response.json()
    assert "errors" in data
    assert "invalidField" in data["errors"][0]["message"]


def test_authentication():
    """Test protected query without auth."""
    query = """
    query {
      me {
        name
        email
      }
    }
    """

    # Without auth token
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query}
    )

    data = response.json()
    assert "errors" in data
    assert "Unauthorized" in str(data["errors"])


def test_mutation():
    """Test mutation with validation."""
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
        GRAPHQL_URL,
        json={
            "query": mutation,
            "variables": variables
        },
        headers={"Authorization": "Bearer <token>"}
    )

    data = response.json()
    assert "errors" not in data
    assert data["data"]["createUser"]["id"] is not None


def test_type_validation():
    """Test type mismatch."""
    query = """
    query {
      user(id: 123) {  # Should be string, passed int
        name
      }
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        json={"query": query}
    )

    data = response.json()
    assert "errors" in data
```

## Schema Validation

### Required Fields

```graphql
type User {
  id: ID!           # Required
  name: String!     # Required
  email: String     # Optional
}
```

Test:

```python
def test_required_fields():
    mutation = """
    mutation {
      createUser(input: {
        # Missing required 'name' field
        email: "test@example.com"
      }) {
        id
      }
    }
    """

    response = requests.post(GRAPHQL_URL, json={"query": mutation})
    data = response.json()

    assert "errors" in data
    assert "name" in str(data["errors"]).lower()
```

### Type Checking

```python
def test_type_checking():
    mutation = """
    mutation {
      createUser(input: {
        name: "Test",
        age: "invalid"  # Should be Int, not String
      }) {
        id
      }
    }
    """

    response = requests.post(GRAPHQL_URL, json={"query": mutation})
    data = response.json()

    assert "errors" in data
```

## Best Practices for Testing

1. **Test Both Success and Failure Cases**
   - Valid queries should return data
   - Invalid queries should return errors

2. **Validate Schema Compliance**
   - Check response matches expected types
   - Verify required fields are present
   - Test null/non-null constraints

3. **Test Authentication/Authorization**
   - Protected queries without auth → error
   - Valid auth → success
   - Field-level permissions

4. **Test Error Messages**
   - Errors should be descriptive
   - Include location and path
   - Provide actionable feedback

5. **Test Edge Cases**
   - Empty results
   - Large datasets
   - Deeply nested queries
   - Circular references

## Common GraphQL Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Syntax error | Invalid query syntax | Check query structure |
| Unknown field | Field doesn't exist | Check schema |
| Type mismatch | Wrong variable type | Match schema types |
| Required argument | Missing argument | Provide argument |
| Unauthorized | No/invalid auth | Add valid token |
| Forbidden | Insufficient permissions | Check user permissions |

## References

- [GraphQL Official Docs](https://graphql.org/learn/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Testing GraphQL APIs](https://amplication.com/blog/best-practices-in-testing-graphql-apis)
