# Framework-Specific Templates

Detailed specifications for each supported framework.

---

## Node.js / Express

### Overview

Node.js with Express is ideal for building REST APIs, backend services, and server-side applications.

### Folder Structure

```
project-name/
├── src/
│   ├── controllers/        # Request handlers
│   │   └── user.controller.ts
│   ├── routes/            # Route definitions
│   │   └── user.routes.ts
│   ├── middleware/        # Custom middleware
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── validate.middleware.ts
│   ├── models/            # Data models (if using ORM)
│   │   └── user.model.ts
│   ├── services/          # Business logic
│   │   └── user.service.ts
│   ├── utils/             # Helper functions
│   │   ├── logger.ts
│   │   └── validator.ts
│   ├── config/            # Configuration
│   │   ├── database.ts
│   │   └── env.ts
│   ├── types/             # TypeScript types
│   │   └── express.d.ts
│   └── app.ts             # App entry point
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── eslint.config.js
├── vitest.config.ts
└── README.md
```

### Essential Dependencies

```json
{
  "dependencies": {
    "express": "^4.18.0",
    "dotenv": "^16.0.0",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/express": "^4.17.0",
    "@types/node": "^20.0.0",
    "@types/cors": "^2.8.0",
    "tsx": "^4.0.0",
    "vitest": "^1.0.0",
    "eslint": "^8.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  }
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "types": ["node", "vitest/globals"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### Starter Code

**app.ts:**
```typescript
import express, { Express } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Routes
// app.use('/api/users', userRoutes);

// Error handling middleware
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

export default app;
```

---

## React (with Vite)

### Overview

React with Vite provides fast development experience for single-page applications.

### Folder Structure

```
project-name/
├── src/
│   ├── components/        # Reusable components
│   │   ├── common/        # Generic components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── Button.css
│   │   │   └── Input/
│   │   └── layout/        # Layout components
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── pages/             # Page components
│   │   ├── Home.tsx
│   │   └── About.tsx
│   ├── hooks/             # Custom React hooks
│   │   └── useAuth.ts
│   ├── services/          # API services
│   │   └── api.ts
│   ├── store/             # State management
│   │   └── userStore.ts
│   ├── utils/             # Helper functions
│   │   └── formatters.ts
│   ├── types/             # TypeScript types
│   │   └── user.types.ts
│   ├── assets/            # Static assets
│   │   ├── images/
│   │   └── styles/
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── public/
│   └── favicon.ico
├── tests/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
├── eslint.config.js
└── README.md
```

### Essential Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-react": "^7.33.0",
    "eslint-plugin-react-hooks": "^4.6.0"
  }
}
```

### Vite Configuration

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
})
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Starter Code

**App.tsx:**
```typescript
import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <h1>Welcome to Your New React App</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
    </div>
  )
}

export default App
```

---

## Next.js

### Overview

Next.js is a full-stack React framework with server-side rendering, API routes, and file-based routing.

### Folder Structure (App Router)

```
project-name/
├── app/
│   ├── (auth)/            # Route group
│   │   ├── login/
│   │   └── register/
│   ├── api/               # API routes
│   │   └── users/
│   │       └── route.ts
│   ├── components/        # App-specific components
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css
├── components/            # Shared components
├── lib/                   # Utilities and helpers
├── public/
├── types/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── next.config.js
└── README.md
```

### Essential Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
```

---

## Python / Flask

### Overview

Flask is a lightweight Python web framework for building APIs and web applications.

### Folder Structure

```
project-name/
├── app/
│   ├── __init__.py        # App factory
│   ├── routes/            # Blueprints
│   │   ├── __init__.py
│   │   └── users.py
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/          # Business logic
│   │   └── user_service.py
│   ├── utils/             # Helper functions
│   │   └── validators.py
│   └── config.py          # Configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_users.py
├── migrations/            # Database migrations (if using Flask-Migrate)
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.py
├── pytest.ini
└── README.md
```

### Essential Dependencies

**requirements.txt:**
```
Flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
flask-sqlalchemy==3.1.0
flask-migrate==4.0.0
pytest==7.4.0
pytest-flask==1.3.0
black==23.0.0
flake8==6.1.0
mypy==1.7.0
```

### Starter Code

**app/__init__.py:**
```python
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes import users
    app.register_blueprint(users.bp)

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app
```

---

## Python / Django

### Overview

Django is a full-featured web framework with built-in admin, ORM, and authentication.

### Folder Structure

```
project-name/
├── project_name/          # Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                  # Django apps
│   └── users/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       ├── admin.py
│       └── tests.py
├── static/
├── media/
├── templates/
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

### Essential Dependencies

**requirements.txt:**
```
Django==5.0.0
djangorestframework==3.14.0
django-cors-headers==4.3.0
python-dotenv==1.0.0
psycopg2-binary==2.9.0
pytest-django==4.7.0
```

---

## Comparison Table

| Feature | Node/Express | React | Next.js | Flask | Django |
|---------|-------------|-------|---------|-------|--------|
| **Type** | Backend | Frontend | Full-stack | Backend | Full-stack |
| **Language** | TypeScript | TypeScript | TypeScript | Python | Python |
| **Learning Curve** | Low | Medium | Medium | Low | High |
| **Best For** | APIs | SPAs | SSR apps | APIs | Complex apps |
| **Routing** | Manual | React Router | File-based | Blueprints | URL patterns |
| **Database** | External ORM | N/A | External ORM | SQLAlchemy | Built-in ORM |
| **Admin Panel** | No | No | No | No | Built-in |

---

## References

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [React Folder Structure](https://www.robinwieruch.de/react-folder-structure/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)
