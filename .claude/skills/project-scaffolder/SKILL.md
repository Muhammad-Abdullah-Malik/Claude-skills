---
name: project-scaffolder
description: |
  Quickly scaffolds new projects with production-ready boilerplate code and folder structures. Use when users ask to create new projects, set up starter templates, initialize applications, or generate boilerplate for Node.js, React, Python, or full-stack applications. Includes TypeScript support, testing setup, and best-practice folder structures.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Project Scaffolder

Rapidly create production-ready projects with optimized folder structures, boilerplate code, and configuration files.

## How This Skill Works

```
User: "Create a new React project with TypeScript"
       ↓
Ask clarifications (framework, features, preferences)
       ↓
Generate project structure with best practices
       ↓
Initialize git, install dependencies, provide next steps
```

This skill creates complete project scaffolds with:
- Production-ready folder structures
- TypeScript configuration
- Testing setup (Jest, Vitest, pytest)
- Linting and formatting (ESLint, Prettier, Black)
- Git initialization
- Environment configuration
- Documentation templates

## What This Skill Does

- Scaffolds new Node.js/Express projects
- Creates React/Next.js applications
- Sets up Python/Django/Flask projects
- Generates full-stack project templates
- Configures TypeScript for all supported frameworks
- Sets up testing infrastructure
- Initializes git repositories
- Creates development and production configs
- Generates README and documentation

## What This Skill Does NOT Do

- Deploy projects to production
- Install global dependencies
- Modify existing projects (use other skills for that)
- Create database schemas or migrations
- Set up CI/CD pipelines (generates basic configs only)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Check if directory is empty, existing files that might conflict |
| **Conversation** | User's framework choice, project name, features needed, TypeScript preference |
| **Skill References** | Framework-specific patterns from `references/` (folder structures, best practices, templates) |
| **User Guidelines** | Team conventions, coding standards, custom configurations |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Clarifications Workflow

Before scaffolding, gather user requirements:

### 1. Framework Selection

Ask user which framework/stack they want:

| Framework | Use Case | Template Features |
|-----------|----------|-------------------|
| **Node.js/Express** | REST APIs, Backend services | Express server, middleware, route structure, TypeScript |
| **React** | Frontend SPAs | Vite setup, component structure, hooks, routing, TypeScript |
| **Next.js** | Full-stack React apps | App router, API routes, TypeScript, SSR/SSG setup |
| **Python/Flask** | Python web APIs | Flask app structure, blueprints, SQLAlchemy, pytest |
| **Python/Django** | Full-featured web apps | Django project structure, apps, models, admin |
| **Full-Stack** | Complete application | Frontend + Backend + shared configs |

### 2. Project Configuration

Gather additional details:

```
- Project name? (validate: lowercase, hyphens, no spaces)
- Include testing setup? (Jest/Vitest/pytest)
- Include Docker configuration? (Dockerfile + docker-compose)
- Database needed? (PostgreSQL, MongoDB, SQLite)
- Authentication required? (JWT, OAuth, session-based)
```

### 3. Optional Features

Based on framework, ask about:
- State management (Redux, Zustand, Context)
- Styling (CSS Modules, Tailwind, Styled Components)
- API client (Axios, Fetch, tRPC)
- ORM/Database (Prisma, TypeORM, SQLAlchemy)
- Environment configs (dev, staging, production)

---

## Scaffolding Workflow

### Step 1: Validate Project Setup

```
Check current directory → Validate project name → Check dependencies available
```

**Validations:**
- Directory is empty or user confirms overwrite
- Project name follows conventions (lowercase, hyphens)
- Node.js/Python/npm/pip installed (depending on framework)
- No existing project with same name

### Step 2: Generate Folder Structure

Based on framework, create appropriate structure:

**Node.js/Express:**
```
project-name/
├── src/
│   ├── controllers/
│   ├── routes/
│   ├── middleware/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── config/
│   └── app.ts
├── tests/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── eslint.config.js
└── README.md
```

**React (Vite):**
```
project-name/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── public/
├── tests/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

**Python/Flask:**
```
project-name/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── config.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

### Step 3: Generate Configuration Files

Create essential config files:

**TypeScript (`tsconfig.json`):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**ESLint Configuration:**
```javascript
import js from '@eslint/js'
import typescript from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { project: './tsconfig.json' }
    },
    plugins: { '@typescript-eslint': typescript },
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'warn'
    }
  }
]
```

**Package.json:**
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/app.ts",
    "build": "tsc",
    "start": "node dist/app.js",
    "test": "vitest",
    "lint": "eslint src/**/*.ts"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "eslint": "^8.0.0",
    "vitest": "^1.0.0"
  }
}
```

**Environment Template (`.env.example`):**
```bash
# Application
NODE_ENV=development
PORT=3000
API_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d

# External APIs
API_KEY=your-api-key-here
```

**Git Ignore (`.gitignore`):**
```
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
env/

# Build outputs
dist/
build/
*.tsbuildinfo

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
```

### Step 4: Generate Boilerplate Code

Create starter files based on framework:

**Node.js Express Server (`src/app.ts`):**
```typescript
import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Hello World!' });
});

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

export default app;
```

**React Component (`src/App.tsx`):**
```typescript
import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <h1>Welcome to Your New Project</h1>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
    </div>
  );
}

export default App;
```

**Flask App (`app/__init__.py`):**
```python
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    CORS(app)

    @app.route('/')
    def index():
        return jsonify({'message': 'Hello World!'})

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

### Step 5: Initialize Git Repository

```bash
# Initialize git
git init

# Create initial commit
git add .
git commit -m "Initial commit: Project scaffolding"

# Create .gitignore if not exists
# Add default branch
git branch -M main
```

### Step 6: Generate Documentation

**README.md Template:**
```markdown
# Project Name

Brief description of your project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Node.js 18+ (or Python 3.10+)
- npm/yarn (or pip)
- [Other dependencies]

## Installation

\`\`\`bash
# Install dependencies
npm install  # or: pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values
\`\`\`

## Development

\`\`\`bash
# Run development server
npm run dev  # or: python run.py

# Run tests
npm test  # or: pytest

# Build for production
npm run build  # or: python setup.py build
\`\`\`

## Project Structure

\`\`\`
src/
├── components/   # Reusable components
├── services/     # API services
├── utils/        # Helper functions
└── ...
\`\`\`

## Technologies

- [Framework name and version]
- TypeScript
- [Other key technologies]

## License

MIT
```

### Step 7: Install Dependencies (Optional)

Ask user if they want to install dependencies now:

```bash
# Node.js
npm install
# or
yarn install

# Python
pip install -r requirements.txt
# or
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

---

## Best Practices Checklist

After scaffolding, verify:

### Structure
- [ ] Clear folder organization (by feature or layer)
- [ ] Maximum 4-5 nesting levels
- [ ] Consistent naming conventions (kebab-case for files, PascalCase for components)
- [ ] Separation of concerns (routes, controllers, services, models)

### Configuration
- [ ] TypeScript configured with strict mode
- [ ] ESLint/Prettier set up
- [ ] Environment variables template provided
- [ ] Git initialized with proper .gitignore
- [ ] README with clear instructions

### Code Quality
- [ ] No hardcoded secrets or credentials
- [ ] Type safety enabled
- [ ] Testing framework configured
- [ ] Error handling patterns included
- [ ] Logging setup (development vs production)

### Security
- [ ] .env file in .gitignore
- [ ] No sensitive data in code
- [ ] CORS configured (for APIs)
- [ ] Input validation patterns
- [ ] Security headers (for web apps)

### Development Experience
- [ ] Hot reload configured
- [ ] Scripts for common tasks (dev, build, test, lint)
- [ ] Clear error messages
- [ ] Development vs production modes
- [ ] Documentation for setup and usage

---

## Output Format

After scaffolding, display to user:

```
✓ Project scaffolded successfully!

Project: [project-name]
Framework: [framework-name]
Location: [/path/to/project]

Created:
- 📁 Folder structure ([X] files, [Y] directories)
- ⚙️  Configuration files (TypeScript, ESLint, etc.)
- 📝 Documentation (README.md)
- 🔧 Development setup
- 🧪 Testing infrastructure
- 📦 Package configuration

Next steps:
1. cd [project-name]
2. npm install  (or pip install -r requirements.txt)
3. cp .env.example .env  (and configure)
4. npm run dev  (to start development server)

For more information, see README.md
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/frameworks.md` | Detailed specs for each framework (Node.js, React, Python) |
| `references/folder-structures.md` | Best practice folder structures with rationale |
| `references/best-practices.md` | Code organization, naming conventions, patterns |
| `references/anti-patterns.md` | Common mistakes to avoid in project setup |
| `references/typescript-config.md` | TypeScript configuration options and best practices |

---

## Quick Examples

### Example 1: Node.js API Project

```
User: "Create a new Node.js API project with TypeScript"

Clarifications:
- Project name? → "my-api"
- Include testing? → Yes (Vitest)
- Database? → PostgreSQL
- Auth? → JWT

Generated:
- Express TypeScript server
- Route/controller structure
- Prisma ORM setup
- JWT middleware
- Vitest tests
- Docker configuration
```

### Example 2: React Frontend

```
User: "Scaffold a React app with TypeScript and Tailwind"

Clarifications:
- Project name? → "my-app"
- Routing? → React Router
- State management? → Zustand
- API client? → Axios

Generated:
- Vite + React + TypeScript
- Tailwind CSS configured
- React Router setup
- Zustand store template
- Axios service layer
- Component library structure
```

### Example 3: Python Flask API

```
User: "Create a Flask API project"

Clarifications:
- Project name? → "flask-api"
- Database? → SQLAlchemy + PostgreSQL
- Testing? → pytest
- Docker? → Yes

Generated:
- Flask application factory
- Blueprint structure
- SQLAlchemy models
- pytest configuration
- Docker + docker-compose
- Requirements.txt
```

---

## Notes

- Always create `.env.example` but never `.env` with real values
- Initialize git AFTER creating .gitignore
- Verify user has required tools installed before scaffolding
- Provide clear next steps after project creation
- Use production-ready defaults, not minimal setups
- TypeScript is default for JavaScript projects
- Follow official framework conventions
