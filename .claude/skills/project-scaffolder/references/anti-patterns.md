# Project Setup Anti-Patterns

Common mistakes to avoid when scaffolding projects.

---

## 1. Overemphasis on Detail at the Beginning

❌ **Bad:**
Creating overly complex structure for small project:

```
my-todo-app/
├── src/
│   ├── core/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── application/
│   ├── shared/
│   │   ├── interfaces/
│   │   ├── decorators/
│   │   └── utilities/
│   └── modules/
│       └── todo/
│           ├── entities/
│           ├── repositories/
│           ├── use-cases/
│           └── controllers/
```

For a simple todo app, this is over-engineered!

✅ **Good:**
Start simple, grow as needed:

```
my-todo-app/
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
```

**Lesson:** Don't build for imaginary future requirements.

---

## 2. Organizing Only by File Type

❌ **Bad:**
Separating by technical concern:

```
src/
├── controllers/
│   ├── user.controller.ts
│   ├── post.controller.ts
│   └── comment.controller.ts
├── services/
│   ├── user.service.ts
│   ├── post.service.ts
│   └── comment.service.ts
└── models/
    ├── user.model.ts
    ├── post.model.ts
    └── comment.model.ts
```

To work on "users", you navigate 3 different folders!

✅ **Good:**
Group by feature/domain:

```
src/
├── users/
│   ├── user.controller.ts
│   ├── user.service.ts
│   └── user.model.ts
├── posts/
└── comments/
```

Everything related to users is in one place.

---

## 3. Too Deep Nesting

❌ **Bad:**
```
src/app/features/users/components/forms/inputs/text/validation/rules/email/EmailValidator.tsx
```

10 levels deep!

✅ **Good:**
```
src/users/components/EmailInput.tsx
```

**Rule:** Max 4-5 levels of nesting.

---

## 4. Inconsistent Naming

❌ **Bad:**
```
UserComponent.tsx
user-service.ts
UserModel.ts
user_repository.ts
USER-ROUTES.ts
```

Every file uses different convention!

✅ **Good:**
```
User.tsx              (components)
user.service.ts       (services)
user.model.ts         (models)
user.repository.ts    (repositories)
user.routes.ts        (routes)
```

Consistent kebab-case for files.

---

## 5. God Files

❌ **Bad:**
Single file with everything:

```typescript
// utils.ts (2000 lines)
export function formatDate() {}
export function validateEmail() {}
export function hashPassword() {}
export function generateToken() {}
export function sendEmail() {}
export function uploadFile() {}
// ... 50 more functions
```

Impossible to maintain!

✅ **Good:**
Split by responsibility:

```
utils/
├── date.utils.ts
├── validation.utils.ts
├── crypto.utils.ts
├── email.utils.ts
└── file.utils.ts
```

---

## 6. No Configuration Management

❌ **Bad:**
Hardcoding values everywhere:

```typescript
// Scattered throughout code
const apiUrl = "https://api.example.com";
const port = 3000;
const dbUrl = "postgresql://localhost:5432/mydb";
```

Can't change environment!

✅ **Good:**
Centralized configuration:

```typescript
// config/env.ts
export const config = {
  apiUrl: process.env.API_URL,
  port: process.env.PORT || 3000,
  dbUrl: process.env.DATABASE_URL
};
```

---

## 7. Mixing Concerns in Components

❌ **Bad:**
Component doing everything:

```typescript
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // API call directly in component
    fetch('https://api.example.com/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  // Business logic in component
  const filteredUsers = users.filter(u =>
    u.age > 18 && u.status === 'active'
  );

  return <div>{/* render */}</div>;
}
```

Component knows too much!

✅ **Good:**
Separate concerns:

```typescript
// services/api.ts
export const getUsers = () => fetch('/api/users').then(r => r.json());

// hooks/useUsers.ts
export const useUsers = () => {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    getUsers().then(setUsers);
  }, []);
  return users;
};

// components/UserList.tsx
function UserList() {
  const users = useUsers();
  return <div>{/* render */}</div>;
}
```

---

## 8. No Error Handling

❌ **Bad:**
```typescript
async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();  // What if it fails?
}
```

No error handling at all!

✅ **Good:**
```typescript
async function getUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

---

## 9. Committing Secrets

❌ **Bad:**
```javascript
// config.js (committed to git)
export const config = {
  apiKey: "sk_live_abc123xyz789",
  dbPassword: "super_secret_password"
};
```

Secrets exposed forever in git history!

✅ **Good:**
```javascript
// config.js
export const config = {
  apiKey: process.env.API_KEY,
  dbPassword: process.env.DB_PASSWORD
};

// .env (NOT committed)
API_KEY=sk_live_abc123xyz789
DB_PASSWORD=super_secret_password

// .gitignore
.env
```

---

## 10. No Testing Structure

❌ **Bad:**
Tests scattered everywhere:

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx  ❌ Test with source
├── services/
│   └── api.ts
└── random-tests/
    └── api.spec.ts  ❌ Inconsistent location
```

Can't find tests easily!

✅ **Good:**
Dedicated test directory:

```
src/
├── components/
│   └── Button.tsx
└── services/
    └── api.ts

tests/
├── components/
│   └── Button.test.tsx
└── services/
    └── api.test.ts
```

Or co-located consistently:
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx  ✓ Consistent co-location
```

---

## 11. Copying Entire Boilerplates

❌ **Bad:**
```bash
# Copying massive template with everything
npx create-react-app my-app
cd my-app
# 1000+ files, 200MB node_modules
# Only using 10% of features
```

Bloated from day one!

✅ **Good:**
Start minimal, add as needed:

```bash
# Start with Vite (lightweight)
npm create vite@latest my-app -- --template react-ts
# Clean, fast, only what you need
```

---

## 12. Poor Folder Naming

❌ **Bad:**
```
src/
├── stuff/
├── things/
├── helpers/  (too generic)
├── misc/     (too vague)
└── temp/     (permanent temporary folder)
```

Meaningless names!

✅ **Good:**
```
src/
├── components/
├── services/
├── utils/
├── hooks/
└── types/
```

Clear, descriptive names.

---

## 13. No Documentation

❌ **Bad:**
Empty README:

```markdown
# My Project

TODO: Add documentation
```

New developers are lost!

✅ **Good:**
Comprehensive README:

```markdown
# My Project

Brief description

## Prerequisites
- Node.js 18+
- PostgreSQL 14+

## Installation
\`\`\`bash
npm install
cp .env.example .env
\`\`\`

## Development
\`\`\`bash
npm run dev
\`\`\`

## Project Structure
\`\`\`
src/
├── components/  # Reusable UI components
├── services/    # API services
...
\`\`\`
```

---

## 14. Ignoring TypeScript

❌ **Bad:**
Using `any` everywhere:

```typescript
function processData(data: any): any {
  return data.map((item: any) => item.value);
}
```

No type safety!

✅ **Good:**
Proper types:

```typescript
interface DataItem {
  id: string;
  value: number;
}

function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}
```

---

## 15. Not Using Linter/Formatter

❌ **Bad:**
```javascript
function getUser(id){
const user=users.find(u=>u.id===id)
return user
}
```

Inconsistent formatting, hard to read!

✅ **Good:**
Setup ESLint + Prettier:

```json
{
  "scripts": {
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write src/**/*.ts"
  }
}
```

---

## 16. Monolithic Configuration

❌ **Bad:**
Single giant config file:

```typescript
// config.ts (500 lines)
export const config = {
  database: { /* 100 lines */ },
  api: { /* 100 lines */ },
  auth: { /* 100 lines */ },
  email: { /* 100 lines */ },
  // ...
};
```

Hard to maintain!

✅ **Good:**
Split by domain:

```
config/
├── database.ts
├── api.ts
├── auth.ts
├── email.ts
└── index.ts  (exports all)
```

---

## 17. No Environment Separation

❌ **Bad:**
Same config for dev and production:

```typescript
const config = {
  debug: true,  // ❌ Debug mode in production!
  apiUrl: "http://localhost:3000"  // ❌ Won't work in prod
};
```

Dangerous!

✅ **Good:**
Environment-specific configs:

```typescript
const config = {
  development: {
    debug: true,
    apiUrl: "http://localhost:3000"
  },
  production: {
    debug: false,
    apiUrl: process.env.API_URL
  }
};

export default config[process.env.NODE_ENV || 'development'];
```

---

## 18. Circular Dependencies

❌ **Bad:**
```typescript
// userService.ts
import { postService } from './postService';

export const userService = {
  getPosts: (userId) => postService.getByUser(userId)
};

// postService.ts
import { userService } from './userService';  // ❌ Circular!

export const postService = {
  getUser: (postId) => userService.getById(postId)
};
```

Can cause runtime errors!

✅ **Good:**
Introduce a middle layer:

```typescript
// userService.ts
export const userService = { /* ... */ };

// postService.ts
export const postService = { /* ... */ };

// combinedService.ts
import { userService } from './userService';
import { postService } from './postService';

export const getUserPosts = (userId) =>
  postService.getByUser(userId);
```

---

## Summary: Top 10 Mistakes

1. Over-engineering from start
2. Organizing only by file type
3. Too deep folder nesting
4. Inconsistent naming
5. No configuration management
6. Mixing concerns
7. Committing secrets
8. No error handling
9. Poor documentation
10. Ignoring TypeScript

---

## References

- [Common Folder Structure Mistakes](https://www.extensis.com/blog/how-to-create-a-manageable-and-logical-folder-structure)
- [Project Management Anti-Patterns](https://www.catalyte.io/insights/project-management-anti-patterns/)
- [Software Anti-Patterns](https://www.geeksforgeeks.org/blogs/types-of-anti-patterns-to-avoid-in-software-development/)
