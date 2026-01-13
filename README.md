# Claude Skills Lab

A collection of custom Claude Code skills designed to automate and enhance development workflows. This repository contains three specialized skills for API testing, project scaffolding, and professional content creation.

## 🚀 Skills Overview

### 1. API Testing Suite (`/api-testing-suite`)

Automates REST and GraphQL API testing with comprehensive validation, security testing, and detailed reporting capabilities.

**Key Features:**
- REST and GraphQL API testing with Python (requests/httpx)
- Authentication validation (JWT, OAuth 2.0, API keys)
- Security testing (authorization, input validation, rate limiting)
- Request/response schema validation
- Mock data generation
- Detailed test reports with pass/fail status
- Support for multiple environments (dev, staging, production)

**Use Cases:**
- Testing API endpoints for functionality and security
- Validating authentication and authorization flows
- Checking request/response formats
- Exploring API behavior and edge cases
- Generating comprehensive test reports

**Example Usage:**
```
User: "Test the API at https://api.example.com/users"
Claude: Uses api-testing-suite to send requests, validate responses,
        and generate a detailed test report
```

**Technologies:**
- Python (requests, httpx)
- JSON schema validation
- JWT/OAuth authentication
- Environment variable management

---

### 2. Project Scaffolder (`/project-scaffolder`)

Quickly scaffolds new projects with production-ready boilerplate code, folder structures, and configuration files.

**Key Features:**
- Next.js, React, Node.js/Express, Python/Flask/Django project templates
- TypeScript configuration with strict mode
- Tailwind CSS, CSS Modules, or Styled Components setup
- Database integration (Prisma + PostgreSQL, MongoDB)
- Authentication setup (NextAuth.js, JWT)
- Testing infrastructure (Vitest, Jest, pytest)
- ESLint/Prettier configuration
- Git initialization with proper .gitignore
- Docker configuration (optional)
- Comprehensive README generation

**Use Cases:**
- Starting new projects with best practices
- Setting up full-stack applications
- Creating consistent project structures
- Rapid prototyping with production-ready setup
- Team onboarding with standardized templates

**Example Usage:**
```
User: "Create a new Next.js project with TypeScript and Prisma"
Claude: Uses project-scaffolder to generate complete project structure
        with all configurations, dependencies, and documentation
```

**Supported Frameworks:**
- **Frontend:** React (Vite), Next.js 14
- **Backend:** Node.js/Express, Python/Flask, Django
- **Databases:** PostgreSQL (Prisma), MongoDB, SQLite
- **Authentication:** NextAuth.js, JWT, OAuth

---

### 3. LinkedIn Post Generator (`/linkedin-post-generator`)

Generates professional LinkedIn posts for research achievements, conference presentations, and academic milestones following proven engagement patterns.

**Key Features:**
- Professional academic post structure
- Research paper announcement templates
- Conference presentation formatting
- Achievement highlighting with metrics
- Hashtag optimization (10-15 relevant tags)
- Multiple post variations (short, standard, extended)
- VLCMatrix Lab style formatting
- Real-world impact emphasis
- Team acknowledgment sections

**Use Cases:**
- Announcing research paper publications
- Sharing conference presentations
- Highlighting lab achievements
- Celebrating team milestones
- Building academic presence on LinkedIn

**Example Usage:**
```
User: "Create a LinkedIn post for my paper on building damage assessment"
Claude: Uses linkedin-post-generator to create a professional post with:
        - Engaging headline
        - Research description
        - Key achievements with metrics
        - Impact statement
        - Relevant hashtags
```

**Post Structure:**
1. Bold headline with action verbs
2. Introduction with researcher and supervisor
3. Quoted research title
4. Conference/publication details
5. Research description (1-2 paragraphs)
6. Key achievements (with checkmarks ✅)
7. Impact statement
8. Team congratulations
9. 10-15 relevant hashtags

---

## 📁 Project Structure

```
claude-code-skills-lab-main/
├── .claude/
│   └── skills/
│       ├── api-testing-suite/
│       │   ├── SKILL.md                    # Skill documentation
│       │   ├── references/                 # API testing concepts
│       │   ├── scripts/                    # Python test scripts
│       │   └── assets/                     # Config examples
│       │
│       ├── project-scaffolder/
│       │   ├── SKILL.md                    # Skill documentation
│       │   ├── references/                 # Framework guides
│       │   └── templates/                  # Project templates
│       │
│       └── linkedin-post-generator/
│           ├── SKILL.md                    # Skill documentation
│           ├── references/                 # Example posts
│           └── templates/                  # Post templates
│
├── .gitignore
└── README.md
```

## 🛠️ How to Use These Skills

### Prerequisites

1. **Claude Code CLI** installed and configured
2. **Python 3.8+** (for api-testing-suite)
3. **Node.js 18+** (for project-scaffolder)
4. **Git** configured with your credentials

### Using Skills in Claude Code

Skills are automatically available when working in this directory. Claude Code will detect and use them when relevant to your request.

#### API Testing Suite
```bash
# Example command
"Test this API endpoint: https://dummyjson.com/products/1"
```

#### Project Scaffolder
```bash
# Example command
"Create a new Next.js project with TypeScript, Tailwind CSS, and Prisma"
```

#### LinkedIn Post Generator
```bash
# Example command
"Create a LinkedIn post for my research paper at path/to/paper.pdf"
```

## 📊 Skills Performance

| Skill | Files | Lines of Code | Reference Docs |
|-------|-------|---------------|----------------|
| API Testing Suite | 18 | ~2,500 | 7 guides |
| Project Scaffolder | 15 | ~3,000 | 5 guides |
| LinkedIn Post Generator | 8 | ~800 | 2 examples |

## 🎯 Benefits

### API Testing Suite
- ✅ Comprehensive API validation in minutes
- ✅ Security testing with OWASP guidelines
- ✅ Automated report generation
- ✅ Support for multiple authentication methods

### Project Scaffolder
- ✅ 10x faster project setup
- ✅ Production-ready configurations
- ✅ Best practices baked in
- ✅ Consistent team standards

### LinkedIn Post Generator
- ✅ Professional academic tone
- ✅ Proven engagement patterns
- ✅ Saves 30+ minutes per post
- ✅ Optimized for LinkedIn algorithm

## 🧪 Testing

Each skill includes test cases and examples:

```bash
# API Testing Suite
cd .claude/skills/api-testing-suite
python test_product_api.py

# Project Scaffolder - generates test project
# LinkedIn Post Generator - includes example posts
```

## 📝 Documentation

Detailed documentation for each skill is available in their respective `SKILL.md` files:

- [API Testing Suite Documentation](./.claude/skills/api-testing-suite/SKILL.md)
- [Project Scaffolder Documentation](./.claude/skills/project-scaffolder/SKILL.md)
- [LinkedIn Post Generator Documentation](./.claude/skills/linkedin-post-generator/SKILL.md)

## 🤝 Contributing

To add or modify skills:

1. Follow the skill structure in `.claude/skills/`
2. Create a `SKILL.md` with clear instructions
3. Add reference materials in `references/`
4. Include examples and templates
5. Test thoroughly before committing

## 📄 License

MIT License - Feel free to use and modify these skills for your projects.

## 👨‍💻 Author

**Muhammad Abdullah Malik**
- GitHub: [@Muhammad-Abdullah-Malik](https://github.com/Muhammad-Abdullah-Malik)
- Email: malikabdmalik468@gmail.com

## 🙏 Acknowledgments

These skills were developed to enhance productivity in:
- API development and testing workflows
- Project initialization and setup
- Academic and professional content creation

---

**Built with Claude Code** - Enhancing development workflows with AI-powered skills.
