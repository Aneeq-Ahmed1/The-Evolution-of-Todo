# Claude Code Instructions for Todo Evolution - Phase II

**Project:** Todo Full-Stack Web Application
**Phase:** II - Multi-User Web Application
**Tech Stack:** Next.js 15 + FastAPI + Neon PostgreSQL
**Design:** Yahoo.com-inspired minimal professional UI

---

## Project Overview

The Todo Evolution project has evolved from a Phase I console application to a **Phase II full-stack web application** with:

- ✅ Multi-user support with authentication
- ✅ Cloud PostgreSQL database (Neon)
- ✅ RESTful API (FastAPI)
- ✅ Modern web UI (Next.js + Tailwind)
- ✅ Admin panel for user management
- ✅ Yahoo-inspired clean design

---

## Monorepo Structure

```
phase-02/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   ├── auth/        # Authentication
│   │   └── database/    # DB connection
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages (App Router)
│   │   ├── components/ # React components
│   │   ├── lib/        # Utilities
│   │   └── services/   # API clients
│   └── package.json
├── specs/              # Spec-Kit Plus specs
│   ├── spec.md        # Project specification
│   ├── plan.md        # Implementation plan
│   ├── tasks.md       # Task breakdown
│   └── implementation.md
├── .env                # Environment config
└── CLAUDE.md          # This file
```

---

## Specification References

All specifications are in `/specs` directory:

- **@specs/spec.md** - Complete project specification
- **@specs/plan.md** - Implementation strategy and phases
- **@specs/tasks.md** - Detailed task breakdown
- **@specs/implementation.md** - Implementation summary

---

## How to Use Specs

### When Adding Features
```
1. Read relevant spec: @specs/spec.md
2. Check implementation plan: @specs/plan.md
3. Review task breakdown: @specs/tasks.md
4. Implement following existing patterns
5. Update specs if requirements change
```

### When Fixing Bugs
```
1. Check acceptance criteria in @specs/spec.md
2. Review related implementation in @specs/implementation.md
3. Fix issue following project architecture
4. Test against acceptance criteria
```

---

## Development Workflow

### Running the Application

**Backend (Terminal 1):**
```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:3000/admin

---

## Architecture Patterns

### Backend Patterns

**Layered Architecture:**
```
API Layer (routes)
  ↓
Service Layer (business logic)
  ↓
Database Layer (SQLModel ORM)
  ↓
PostgreSQL (Neon)
```

**File Organization:**
- `/api/*` - Route handlers only
- `/services/*` - Business logic and validation
- `/models/*` - Database models (SQLModel)
- `/schemas/*` - Request/response schemas (Pydantic)
- `/auth/*` - Authentication middleware
- `/utils/*` - Helper functions

**Authentication Flow:**
1. User provides credentials
2. Backend validates against database
3. Generate JWT token with user email
4. Frontend stores token in localStorage
5. All API requests include "Authorization: Bearer {token}"
6. Backend verifies token and extracts user
7. Queries filtered by user_id

### Frontend Patterns

**Next.js App Router:**
- `/app/*` - File-based routing
- Client components: `'use client'` directive
- Server components: Default (when possible)

**State Management:**
- Local state with useState for forms
- No global state library (not needed)
- API calls trigger re-renders

**API Communication:**
- Centralized API client: `lib/api.ts`
- Automatic JWT injection
- Error handling built-in
- TypeScript types for safety

---

## Design System (Yahoo Theme)

### Color Palette
```css
Primary:    #7e1fff  /* Purple - buttons, links, logo */
Background: #f5f8fa  /* Light gray-blue - page background */
Text Dark:  #232a31  /* Headings */
Text Med:   #6e7780  /* Body text */
Text Light: #828a93  /* Subtle text */
Border:     #e0e4e9  /* Borders, dividers */
Button BG:  #f0f3f5  /* Secondary buttons */
White:      #ffffff  /* Cards, nav */
```

### Component Standards
```css
Navigation Height:  57px
Button Min Height:  44px (accessibility)
Border Radius:      8px (standard)
Card Padding:       16px (p-4)
Section Padding:    24px-40px (py-6 to py-10)
```

### Typography
```css
Font Family: Inter (Google Fonts)
Headings:    text-2xl to text-4xl, font-semibold
Body:        text-sm to text-base
Line Height: 1.5 standard
```

---

## Environment Variables

### Required in `.env`
```bash
# Database
DATABASE_URL=postgresql://...neon.tech/neondb

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin
ADMIN_EMAIL=admin@taskflow.com
ADMIN_PASSWORD=Admin@12345

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Admin Panel Usage

### Access Admin Panel
1. Visit: http://localhost:3000/admin
2. Login: admin@taskflow.com / Admin@12345
3. View all users in table
4. Reset any user's password
5. Delete users if needed

### Password Reset Process
1. Find user in admin panel table
2. Click "Reset Password" button
3. Enter new password (min 6 characters)
4. Click "Save"
5. Inform user of new password
6. User can login immediately

---

## API Documentation

### Swagger UI
Visit http://localhost:8000/docs for interactive API documentation

### Authentication Header Format
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Common Error Responses
```json
// 401 Unauthorized
{"detail": "Could not validate credentials"}

// 404 Not Found
{"detail": "Task not found"}

// 400 Bad Request
{"detail": "Email already registered"}
```

---

## Best Practices

### Code Conventions

**Backend (Python):**
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Pydantic models for validation
- Async/await for database operations
- Comprehensive docstrings

**Frontend (TypeScript):**
- Use TypeScript for type safety
- React hooks for state management
- Async/await for API calls
- Error boundaries for error handling
- Responsive design (mobile-first)

### Security Practices
- ✅ Never commit `.env` files
- ✅ Never log passwords or tokens
- ✅ Always validate user input
- ✅ Always filter queries by user_id
- ✅ Use parameterized SQL queries (ORM)
- ✅ Hash passwords with bcrypt
- ✅ Set JWT expiration times

---

## Common Tasks

### Add New API Endpoint
1. Create route in `/backend/src/api/`
2. Create schema in `/backend/src/schemas/`
3. Add business logic in `/backend/src/services/`
4. Add JWT auth dependency if needed
5. Update `/backend/src/main.py` if new router
6. Test with curl or Swagger UI

### Add New Frontend Page
1. Create page in `/frontend/src/app/`
2. Use `'use client'` if interactive
3. Import API client from `lib/api.ts`
4. Apply Yahoo theme (colors, spacing)
5. Add to navigation if needed
6. Test responsiveness

### Update Database Schema
1. Modify model in `/backend/src/models/`
2. Restart backend (auto-creates tables)
3. For production: Use Alembic migrations
4. Update related schemas/services

---

## Troubleshooting

### Common Issues

**Issue: Backend won't start**
```bash
# Check Python dependencies
cd backend
pip install -r requirements.txt

# Check DATABASE_URL
echo $DATABASE_URL

# Check for port conflicts
netstat -ano | findstr :8000
```

**Issue: Frontend shows "Cannot connect to server"**
```bash
# Verify backend is running
curl http://localhost:8000/

# Check NEXT_PUBLIC_API_BASE_URL in .env.local
```

**Issue: "Could not validate credentials"**
```bash
# Check JWT token in browser localStorage
# Verify SECRET_KEY matches in backend .env
# Check token expiration (30 minutes)
```

**Issue: Database connection failed**
```bash
# Verify Neon DATABASE_URL is correct
# Check internet connection
# Verify PostgreSQL drivers installed (psycopg2-binary)
```

---

## Testing Guidelines

### Manual Testing Checklist
- [ ] User can register with new email
- [ ] Duplicate email shows error
- [ ] User can login with credentials
- [ ] Invalid login shows error
- [ ] Dashboard loads user's tasks
- [ ] User can create task
- [ ] User can edit task
- [ ] User can delete task
- [ ] User can toggle completion
- [ ] Filters work (All/Pending/Done)
- [ ] Admin can login
- [ ] Admin can view all users
- [ ] Admin can reset password
- [ ] User can login with reset password
- [ ] Logout works correctly

---

## Resources

### Project Documentation
- Specification: `@specs/spec.md`
- Implementation Plan: `@specs/plan.md`
- Task Breakdown: `@specs/tasks.md`
- Implementation Summary: `@specs/implementation.md`

### Technology Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Neon Docs](https://neon.tech/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Design Reference
- Yahoo.com - Design inspiration
- Color palette extracted from Yahoo's design system

---

## Getting Help

### For Claude Code Users

**Spec Commands:**
- `/sp.specify` - Create new specifications
- `/sp.plan` - Generate implementation plan
- `/sp.tasks` - Generate task breakdown
- `/sp.implement` - Execute implementation

**Development:**
- Check `@specs/spec.md` for requirements
- Check `@specs/implementation.md` for how it was built
- Review code in `backend/src/` or `frontend/src/`
- Use `/sp.clarify` for specification questions

---

**Version:** 2.0 - Phase II Complete
**Last Updated:** December 31, 2025
**Status:** ✅ Production-Ready for Demo

---

## AI Task Display Mapping Feature

### Overview

The AI Task Display Mapping feature enables users to reference tasks by their displayed numbers (e.g., "task 1", "task 2") instead of internal task IDs.

### Supported Ordinal Formats

Users can reference tasks using any of these formats:
- **Numeric**: "task 1", "task 2", "task 3"
- **Ordinal words**: "first task", "second task", "third task"
- **Number words**: "task one", "task two", "task three"
- **Ordinal suffixes**: "1st task", "2nd task", "3rd task"

### Example Commands

```
# Complete tasks
"task 1 is complete"
"first task is done"
"mark task 2 as complete"

# Edit tasks
"edit task 3"
"update the second task"

# Delete tasks
"delete task 1"
"remove the first task"

# Get task info
"show me task 2"
"what is the third task"
```

### Key Implementation Files

**Backend (Python):**
- `agents/backend/src/services/ordinal_resolver.py` - Parses ordinal references
- `agents/backend/src/services/task_resolver.py` - Resolves display indices to task IDs
- `agents/backend/src/services/intent_parser.py` - Extracts intent from commands
- `agents/backend/src/agents/todo_agent.py` - Main AI agent logic
- `backend/src/api/mapping.py` - Display mapping API endpoints
- `backend/src/schemas/mapping.py` - Pydantic schemas

**Frontend (TypeScript):**
- `frontend/src/types/mapping.ts` - TypeScript types
- `frontend/src/services/displayMappingService.ts` - Runtime mapping management

### API Endpoints

**Display-Based Operations:**
- `GET /tasks-with-display` - Get tasks with display indices
- `GET /tasks/display/{display_index}` - Get specific task by display index
- `PUT /tasks/display/{display_index}` - Update task by display index
- `DELETE /tasks/display/{display_index}` - Delete task by display index
- `PATCH /tasks/display/{display_index}/completion` - Toggle completion by display index

**Mapping Operations:**
- `POST /mapping/refresh` - Refresh display mapping after task changes
- `POST /mapping/resolve` - Resolve display index to task ID

### Usage Pattern

1. **Load tasks with display indices:**
   ```typescript
   const response = await fetch('/tasks-with-display');
   const data = response.json();
   // data.tasks contains tasks with display_index field
   // data.display_mapping contains index → id mappings
   ```

2. **Refresh mapping after changes:**
   ```typescript
   import { refreshDisplayMapping } from '@/services/displayMappingService';
   refreshDisplayMapping(updatedTasks, userId);
   ```

3. **Process user commands:**
   ```python
   from agents.backend.src.agents.todo_agent import TodoAgent
   
   agent = TodoAgent("http://localhost:8000", auth_token=token)
   result = agent.process_command("task 1 is complete")
   ```

### Error Handling

The system provides helpful error messages:
- **Out of range**: "You only have 3 tasks. Did you mean task 1, 2, or 3?"
- **Empty list**: "You don't have any tasks yet. Create a task first!"
- **Invalid reference**: "Task numbers start from 1. You have 5 tasks."

### Development Notes

- Display indices are 1-based (task 1, task 2, task 3...)
- Internal task IDs remain unchanged
- Mapping is maintained in runtime memory (no database storage)
- Mapping refreshes automatically when task list changes
- All AI agent operations use display indices for user-friendly interaction

---

**Last Updated:** 2026-01-05
**Feature Status:** ✅ Implemented

