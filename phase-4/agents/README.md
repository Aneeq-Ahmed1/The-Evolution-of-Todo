# Reusable Agents - Todo Full-Stack Application

## Overview

This directory contains two specialized, reusable AI agents designed to assist with development of the Todo Full-Stack Web Application. Each agent has specific expertise, dedicated skills, and clear responsibilities.

---

## Agents

### 1. Backend Agent
**Location:** `agents/backend/agent.md`
**Expertise:** FastAPI, Python, SQLModel, Authentication, Database Management

**Capabilities:**
- API endpoint development
- Database schema design
- Authentication & JWT tokens
- Service layer implementation
- Testing & debugging
- Performance optimization

**Activation:** `@backend-agent <request>`

---

### 2. Frontend Agent
**Location:** `agents/frontend/agent.md`
**Expertise:** Next.js, React, TypeScript, Tailwind CSS, API Integration

**Capabilities:**
- Component development
- Page creation & routing
- State management
- API integration
- Authentication flows
- UI/UX implementation

**Activation:** `@frontend-agent <request>`

---

## Agent Structure

Each agent directory contains:

```
agents/
├── backend/
│   ├── agent.md              # Agent definition & guidelines
│   └── skills/               # Reusable backend skills
│       ├── test-backend.md
│       ├── create-endpoint.md
│       └── run-backend.md
│
└── frontend/
    ├── agent.md              # Agent definition & guidelines
    └── skills/               # Reusable frontend skills
        ├── run-frontend.md
        ├── create-component.md
        └── test-api-call.md
```

---

## Using Agents

### Method 1: Direct Activation
```
@backend-agent Create a new API endpoint for user comments
@frontend-agent Build a modal component for task editing
```

### Method 2: Skill Invocation
```
/backend:test-backend
/backend:create-endpoint user-stats GET --auth
/frontend:run-frontend
/frontend:create-component TaskModal --client --with-state
```

---

## Agent Coordination

When working on full-stack features, agents can coordinate:

### Example: Adding a New Feature

**Step 1: Backend Agent** creates the API
```
@backend-agent Create API endpoints for task comments:
- POST /tasks/{id}/comments (create comment)
- GET /tasks/{id}/comments (list comments)
- DELETE /comments/{id} (delete comment)
```

**Step 2: Frontend Agent** builds the UI
```
@frontend-agent Create components for task comments:
- CommentList component
- CommentForm component
- Add to TaskDetail page
```

**Step 3: Integration**
Both agents ensure:
- API contract matches frontend expectations
- Authentication works properly
- Error handling is consistent
- Types are synchronized

---

## Agent Skills

### Backend Skills

| Skill | Description | Usage |
|-------|-------------|-------|
| `test-backend` | Run comprehensive backend tests | `/backend:test-backend` |
| `create-endpoint` | Generate new API endpoint | `/backend:create-endpoint <name> <method>` |
| `create-model` | Create database model | `/backend:create-model <ModelName>` |
| `run-backend` | Start FastAPI server | `/backend:run-backend` |
| `test-endpoint` | Test specific endpoint | `/backend:test-endpoint <path>` |
| `check-auth` | Verify authentication | `/backend:check-auth` |
| `add-migration` | Create DB migration | `/backend:add-migration <description>` |

### Frontend Skills

| Skill | Description | Usage |
|-------|-------------|-------|
| `run-frontend` | Start Next.js dev server | `/frontend:run-frontend` |
| `create-component` | Generate React component | `/frontend:create-component <Name>` |
| `create-page` | Create Next.js page | `/frontend:create-page <route>` |
| `test-api-call` | Test API endpoint | `/frontend:test-api-call <endpoint>` |
| `check-auth` | Verify auth state | `/frontend:check-auth` |
| `build-frontend` | Production build | `/frontend:build-frontend` |
| `test-frontend` | Run frontend tests | `/frontend:test-frontend` |

---

## Communication Protocol

### Backend → Frontend
Backend agent provides:
- API endpoint documentation
- Request/response schemas
- Authentication requirements
- Error response formats
- Example curl commands

### Frontend → Backend
Frontend agent reports:
- Expected API behavior
- Issues with API responses
- Authentication problems
- CORS errors
- Performance concerns

---

## Best Practices

### When to Use Each Agent

**Use Backend Agent for:**
- Creating/modifying API endpoints
- Database schema changes
- Authentication logic
- Backend business logic
- Performance optimization
- Backend testing

**Use Frontend Agent for:**
- Creating UI components
- Adding new pages
- State management
- API integration
- Styling & responsiveness
- Frontend debugging

**Use Both Agents for:**
- New feature development
- API contract changes
- Authentication flows
- Full-stack bug fixes
- Integration testing
- Performance tuning

---

## Agent Workflows

### Workflow 1: New Feature
1. Define requirements
2. Backend agent creates API
3. Backend agent writes tests
4. Frontend agent creates UI
5. Frontend agent integrates API
6. Both test integration

### Workflow 2: Bug Fix
1. Identify bug location (backend/frontend/both)
2. Appropriate agent investigates
3. Agent proposes fix
4. Test fix thoroughly
5. Verify related functionality

### Workflow 3: Refactoring
1. Identify code to refactor
2. Agent creates refactoring plan
3. Implement changes incrementally
4. Test after each change
5. Update documentation

---

## Agent Memory

Each agent maintains context of:
- Project structure
- Tech stack
- Coding patterns
- Existing code
- Previous conversations
- Common issues & solutions

---

## Extending Agents

### Adding New Skills

1. Create skill file in `agents/<agent>/skills/<skill-name>.md`
2. Document skill purpose, usage, and examples
3. Update agent.md with new skill
4. Test skill thoroughly
5. Update this README

### Skill Template

```markdown
# Agent Skill: Skill Name

## Description
What the skill does

## Usage
How to invoke the skill

## Examples
Usage examples

## What It Does
Step-by-step process

## Output
Expected output format

## Related Skills
Links to related skills
```

---

## Troubleshooting

### Agent Not Responding
- Check agent activation syntax
- Verify agent file exists
- Try specific skill invocation

### Skill Not Working
- Check skill name spelling
- Verify parameters are correct
- Check prerequisites are met
- Review skill documentation

### Coordination Issues
- Ensure API contract is clear
- Verify both agents use same types
- Check authentication flow matches
- Test integration points

---

## Examples

### Example 1: Add Search Feature

**Backend Agent:**
```
@backend-agent Create search endpoint:
- GET /tasks/search?q=query
- Search in title and description
- Return matching tasks for current user
```

**Frontend Agent:**
```
@frontend-agent Add search feature:
- Create SearchBar component
- Add to tasks page
- Display results
- Show "no results" message
```

### Example 2: Fix Authentication Bug

**Frontend Agent:**
```
@frontend-agent Debug: Token not being sent to API
- Check localStorage
- Verify API client
- Test with curl
```

**Backend Agent:**
```
@backend-agent Verify: JWT middleware working
- Check token validation
- Test with sample token
- Review error messages
```

---

## Agent Capabilities Matrix

| Capability | Backend Agent | Frontend Agent |
|------------|---------------|----------------|
| API Development | ✅ Expert | ❌ N/A |
| Database Design | ✅ Expert | ❌ N/A |
| Authentication | ✅ Expert | ✅ Implementation |
| UI Components | ❌ N/A | ✅ Expert |
| State Management | ❌ N/A | ✅ Expert |
| API Integration | ✅ Provides | ✅ Consumes |
| Testing | ✅ Backend | ✅ Frontend |
| Styling | ❌ N/A | ✅ Expert |
| Performance | ✅ Backend | ✅ Frontend |
| Security | ✅ Expert | ✅ Implementation |

---

## Version History

- **v1.0.0** (2025-12-29): Initial release
  - Backend Agent created
  - Frontend Agent created
  - Core skills implemented
  - Documentation completed

---

## Contributing

To improve agents:
1. Test agent behavior
2. Document issues
3. Propose improvements
4. Add new skills
5. Update documentation

---

## Support

For agent-related questions:
1. Check agent documentation
2. Review skill files
3. Test with simple requests
4. Verify prerequisites

---

**Status:** Active and Ready
**Version:** 1.0.0
**Last Updated:** 2025-12-29
