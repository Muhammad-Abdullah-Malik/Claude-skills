# Project Structure Best Practices

Guidelines for organizing code, naming conventions, and folder structures.

---

## General Principles

### 1. Separation of Concerns

Organize code by **responsibility**, not by file type:

✅ **Good (by feature):**
```
users/
  ├── user.controller.ts
  ├── user.service.ts
  ├── user.model.ts
  └── user.routes.ts
```

❌ **Bad (by type):**
```
controllers/
  └── user.controller.ts
services/
  └── user.service.ts
models/
  └── user.model.ts
```

**Why?** Feature-based organization makes code easier to find and modify.

### 2. Limit Nesting Depth

Keep folder nesting to maximum 4-5 levels:

✅ **Good:**
```
src/components/common/Button/Button.tsx  (4 levels)
```

❌ **Bad:**
```
src/app/features/user/components/forms/inputs/text/TextInput.tsx  (8 levels)
```

### 3. Consistent Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Files | kebab-case | `user-service.ts` |
| Folders | kebab-case | `user-profile/` |
| Components | PascalCase | `UserProfile.tsx` |
| Functions | camelCase | `getUserById()` |
| Constants | UPPER_SNAKE_CASE | `API_URL` |
| Classes | PascalCase | `UserService` |

### 4. One Component Per File

Each file should have a single export (one component, one service, etc.):

✅ **Good:**
```typescript
// Button.tsx
export function Button() { }
```

❌ **Bad:**
```typescript
// components.tsx
export function Button() { }
export function Input() { }
export function Select() { }
```

---

## Node.js / Express Best Practices

### Folder Structure

**Layer-based architecture:**

```
src/
├── controllers/    # Handle HTTP requests
├── services/       # Business logic
├── models/         # Data models
├── routes/         # Route definitions
├── middleware/     # Custom middleware
├── utils/          # Helper functions
└── config/         # Configuration
```

**Key principles:**
- Controllers are thin (just handle request/response)
- Services contain business logic
- Models define data structure
- Keep routes separate from logic

### Example Structure

```typescript
// controllers/user.controller.ts
export const getUser = async (req, res) => {
  const user = await userService.getById(req.params.id);
  res.json(user);
};

// services/user.service.ts
export const getById = async (id: string) => {
  return await User.findById(id);
};
```

### Configuration Management

Use environment-based configs:

```typescript
// config/database.ts
export const dbConfig = {
  development: { url: process.env.DEV_DB_URL },
  production: { url: process.env.PROD_DB_URL }
};
```

---

## React Best Practices

### Component Organization

**Small projects (<15 components):**
```
src/
├── components/
├── hooks/
└── App.tsx
```

**Medium projects (15-50 components):**
```
src/
├── components/
│   ├── common/     # Reusable components
│   └── layout/     # Layout components
├── pages/
├── hooks/
└── services/
```

**Large projects (50+ components):**
```
src/
├── features/
│   └── users/
│       ├── components/
│       ├── hooks/
│       └── services/
├── components/     # Shared components
├── hooks/          # Shared hooks
└── services/       # Shared services
```

### Component Structure

Each component in its own folder:

```
Button/
├── Button.tsx          # Component
├── Button.test.tsx     # Tests
├── Button.module.css   # Styles
├── Button.types.ts     # Types
└── index.ts            # Barrel export
```

**index.ts:**
```typescript
export { Button } from './Button';
export type { ButtonProps } from './Button.types';
```

### Import Organization

```typescript
// 1. External libraries
import React from 'react';
import { useNavigate } from 'react-router-dom';

// 2. Internal components
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

// 3. Types
import type { User } from '@/types/user';

// 4. Styles
import styles from './Component.module.css';
```

---

## Python Best Practices

### Project Layout

**Src layout (recommended for production):**
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── module.py
├── tests/
├── setup.py
└── requirements.txt
```

**Flat layout (for simple projects):**
```
project/
├── package_name/
│   ├── __init__.py
│   └── module.py
├── tests/
└── requirements.txt
```

### Flask Best Practices

**Application factory pattern:**

```python
# app/__init__.py
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.routes import users
    app.register_blueprint(users.bp)

    return app
```

**Blueprint organization:**

```python
# app/routes/users.py
bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
def get_users():
    return jsonify(users)
```

### Module Organization

```
app/
├── __init__.py       # App factory
├── models/           # Database models
├── routes/           # Blueprints
├── services/         # Business logic
├── utils/            # Helpers
└── config.py         # Configuration
```

---

## Configuration Files

### Environment Variables

**`.env.example` (committed):**
```bash
# Application
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# API Keys (placeholder)
API_KEY=your-api-key-here
```

**`.env` (NOT committed):**
```bash
# Actual values
API_KEY=sk_live_abc123xyz789
```

### TypeScript Configuration

**Strict mode enabled:**
```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

---

## Testing Structure

### Test Organization

Mirror source structure:

```
src/
├── services/
│   └── user.service.ts
tests/
├── unit/
│   └── services/
│       └── user.service.test.ts
└── integration/
    └── api/
        └── users.test.ts
```

### Naming Conventions

```typescript
describe('UserService', () => {
  describe('getById', () => {
    it('should return user when found', () => {});
    it('should throw error when not found', () => {});
  });
});
```

---

## Documentation

### README Structure

```markdown
# Project Name

Brief description

## Features
## Prerequisites
## Installation
## Development
## Testing
## Deployment
## License
```

### Code Comments

Only comment **why**, not **what**:

✅ **Good:**
```typescript
// Retry 3 times because API is unreliable during peak hours
const maxRetries = 3;
```

❌ **Bad:**
```typescript
// Set max retries to 3
const maxRetries = 3;
```

---

## Security Best Practices

### Environment Variables

- ✅ Use `.env` for secrets
- ✅ Add `.env` to `.gitignore`
- ✅ Provide `.env.example` with placeholders
- ❌ Never commit real secrets

### Input Validation

Always validate user input:

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
});

const user = userSchema.parse(req.body);
```

### Dependencies

- Pin dependency versions
- Regularly update dependencies
- Use `npm audit` or `safety` (Python)

---

## Performance Best Practices

### Code Splitting (React)

```typescript
// Lazy load components
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

### Database Queries

- Use indexes
- Avoid N+1 queries
- Paginate large datasets

### Caching

```typescript
// Cache expensive operations
const cache = new Map();

function expensiveOperation(key) {
  if (cache.has(key)) return cache.get(key);

  const result = /* expensive computation */;
  cache.set(key, result);
  return result;
}
```

---

## Git Best Practices

### .gitignore

Essential ignores:

```
# Dependencies
node_modules/
__pycache__/
venv/

# Build outputs
dist/
build/
*.log

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
```

### Commit Messages

Follow conventional commits:

```
feat: add user authentication
fix: resolve login redirect issue
docs: update README with setup instructions
test: add unit tests for user service
```

---

## Scalability Patterns

### Modular Architecture

Design for growth:

```
features/
├── auth/
│   ├── components/
│   ├── services/
│   └── types/
├── users/
└── products/
```

Each feature is self-contained and can be developed independently.

### Dependency Injection

Make code testable:

```typescript
class UserService {
  constructor(private db: Database) {}

  async getUser(id: string) {
    return this.db.findUser(id);
  }
}
```

---

## Summary Checklist

- [ ] Clear folder organization (feature-based or layer-based)
- [ ] Consistent naming conventions
- [ ] Separation of concerns
- [ ] Environment-based configuration
- [ ] TypeScript strict mode enabled
- [ ] Testing structure mirrors source
- [ ] .gitignore properly configured
- [ ] README with clear instructions
- [ ] No hardcoded secrets
- [ ] Dependencies pinned

---

## References

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [React Folder Structure](https://www.robinwieruch.de/react-folder-structure/)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)
- [12-Factor App](https://12factor.net/)
