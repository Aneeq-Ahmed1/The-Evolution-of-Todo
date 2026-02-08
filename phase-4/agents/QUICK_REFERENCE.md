# Agents Quick Reference Guide

## 🚀 Quick Start

### Activate Agents
```bash
@backend-agent <your request>
@frontend-agent <your request>
```

### Use Skills
```bash
/backend:<skill-name>
/frontend:<skill-name>
```

---

## 📋 Common Commands

### Backend Agent Commands

```bash
# Test backend
/backend:test-backend

# Start server
/backend:run-backend

# Create endpoint
/backend:create-endpoint task-stats GET --auth

# Test endpoint
/backend:test-endpoint /tasks

# Check authentication
/backend:check-auth
```

### Frontend Agent Commands

```bash
# Start dev server
/frontend:run-frontend

# Create component
/frontend:create-component TaskCard --client --with-state

# Create page
/frontend:create-page settings

# Test API call
/frontend:test-api-call /tasks --with-auth

# Build for production
/frontend:build-frontend
```

---

## 🎯 Common Tasks

### 1. Start Development

**Backend:**
```bash
cd backend
/backend:test-backend       # Test first
/backend:run-backend        # Start server
```

**Frontend:**
```bash
cd frontend
/frontend:run-frontend      # Start dev server
```

### 2. Create New Feature

**Backend API:**
```bash
@backend-agent Create endpoint for user profile:
- GET /users/me (get current user)
- PUT /users/me (update profile)
- With authentication
```

**Frontend UI:**
```bash
@frontend-agent Create user profile page:
- Create ProfilePage component
- Add form for editing
- Show user data
- Handle updates
```

### 3. Debug Issue

**Backend:**
```bash
@backend-agent Debug: Tasks endpoint returning 500 error
```

**Frontend:**
```bash
@frontend-agent Debug: Tasks not loading on page
```

### 4. Add Component

```bash
/frontend:create-component Modal --client
/frontend:create-component Button
/frontend:create-component Card --with-props
```

### 5. Test API

```bash
# Test without auth
/frontend:test-api-call / --method GET

# Test with auth
/frontend:test-api-call /tasks --with-auth

# Test POST
/frontend:test-api-call /tasks --method POST --with-auth --data '{"title":"Test"}'
```

---

## 💡 Use Cases

### Use Case 1: Add Search Feature

```bash
# Step 1: Backend
@backend-agent Add search to tasks:
- Endpoint: GET /tasks/search?q=query
- Search in title and description
- Return user-specific results

# Step 2: Frontend
@frontend-agent Add search UI:
- SearchBar component
- Display results
- Handle empty state
```

### Use Case 2: Add Sorting

```bash
# Backend
@backend-agent Add sorting to tasks endpoint:
- Support ?sort_by=created_at|title|completed
- Support ?order=asc|desc

# Frontend
@frontend-agent Add sort dropdown:
- SortDropdown component
- Update API calls
- Persist preference
```

### Use Case 3: Add Filtering

```bash
# Backend
@backend-agent Add filtering:
- ?status=completed|incomplete|all
- ?date_from=YYYY-MM-DD
- ?date_to=YYYY-MM-DD

# Frontend
@frontend-agent Add filter UI:
- FilterPanel component
- Multi-select options
- Apply filters button
```

---

## 🔧 Troubleshooting Commands

### Check Backend Health
```bash
curl http://localhost:8000/
/backend:test-backend
```

### Check Frontend Health
```bash
/frontend:run-frontend
# Open: http://localhost:3000
```

### Check Authentication
```bash
# Backend
/backend:check-auth

# Frontend
/frontend:check-auth
/frontend:test-api-call /tasks --with-auth
```

### Test API Connectivity
```bash
# From frontend
/frontend:test-api-call / --method GET

# From terminal
curl http://localhost:8000/
```

---

## 📊 Agent Comparison

| Task | Backend Agent | Frontend Agent |
|------|---------------|----------------|
| Create API | ✅ | ❌ |
| Create UI | ❌ | ✅ |
| Database | ✅ | ❌ |
| Components | ❌ | ✅ |
| Auth Logic | ✅ | Token storage |
| Testing | Backend | Frontend |
| Styling | ❌ | ✅ |

---

## 🎓 Examples

### Example 1: Complete Feature

```bash
# 1. Backend creates API
@backend-agent Create comments API:
- POST /tasks/{id}/comments
- GET /tasks/{id}/comments
- DELETE /comments/{id}
- All authenticated

# 2. Frontend creates UI
@frontend-agent Create comments UI:
- CommentList component
- CommentForm component
- Add to TaskDetail page
```

### Example 2: Bug Fix

```bash
# Frontend reports issue
@frontend-agent Tasks not loading, getting 401 error

# Backend investigates
@backend-agent Check JWT validation in tasks endpoint
```

### Example 3: Optimization

```bash
# Backend
@backend-agent Optimize tasks query:
- Add indexes
- Reduce joins
- Cache results

# Frontend
@frontend-agent Optimize task list:
- Implement virtualization
- Add pagination
- Lazy load images
```

---

## 🚨 Emergency Commands

### Backend Crashed
```bash
cd backend
python test_backend.py    # Check what's broken
python -m src.main         # Restart
```

### Frontend Not Loading
```bash
cd frontend
npm install                # Reinstall deps
rm -rf .next              # Clear cache
npm run dev               # Restart
```

### Database Issues
```bash
@backend-agent Reset database:
- Drop all tables
- Recreate schema
- Run migrations
```

### Authentication Broken
```bash
# Clear frontend
localStorage.clear()

# Test backend
/backend:check-auth

# Re-login
# Go to: /auth/login
```

---

## 📱 Mobile Commands

### Check Responsive Design
```bash
@frontend-agent Check mobile responsiveness:
- Test on different screen sizes
- Adjust breakpoints
- Fix layout issues
```

### Test on Device
```bash
# Start with network access
/frontend:run-frontend --host 0.0.0.0

# Access from phone:
http://YOUR_IP:3000
```

---

## 🔐 Security Commands

### Backend Security
```bash
@backend-agent Security review:
- Check input validation
- Test SQL injection
- Verify authentication
- Check rate limiting
```

### Frontend Security
```bash
@frontend-agent Security check:
- XSS prevention
- Token storage
- Secure API calls
- Input sanitization
```

---

## 📈 Performance Commands

### Backend Performance
```bash
@backend-agent Optimize performance:
- Profile slow queries
- Add caching
- Optimize indexes
- Reduce N+1 queries
```

### Frontend Performance
```bash
@frontend-agent Performance audit:
- Lighthouse score
- Bundle size
- Load time
- Render performance
```

---

## 💾 Backup Commands

### Backup Database
```bash
@backend-agent Backup database to file
```

### Export Data
```bash
@backend-agent Export all tasks to JSON
```

---

## 🔄 Update Commands

### Update Dependencies
```bash
# Backend
cd backend
pip list --outdated

# Frontend
cd frontend
npm outdated
```

### Apply Migrations
```bash
@backend-agent Apply pending migrations
```

---

## 📝 Documentation Commands

### Generate API Docs
```bash
# Access Swagger UI
http://localhost:8000/docs
```

### Generate Component Docs
```bash
@frontend-agent Document all components
```

---

**Quick Tip:** Use `@backend-agent` for server-side work and `@frontend-agent` for UI work. They can work together!

**Last Updated:** 2025-12-29
