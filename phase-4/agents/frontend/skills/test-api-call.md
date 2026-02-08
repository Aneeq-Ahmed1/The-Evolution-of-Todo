# Frontend Skill: Test API Call

## Skill Name
`test-api-call`

## Description
Test API endpoint calls from the frontend to verify connectivity and response format.

## Usage
```
/frontend:test-api-call <endpoint> [--method METHOD] [--with-auth] [--data JSON]
```

## Examples

```bash
# Test GET endpoint
/frontend:test-api-call /tasks

# Test POST with authentication
/frontend:test-api-call /tasks --method POST --with-auth --data '{"title":"Test"}'

# Test login endpoint
/frontend:test-api-call /auth/login --method POST --data '{"email":"test@test.com","password":"test123"}'
```

## Parameters

- `<endpoint>`: API endpoint path (e.g., /tasks, /auth/login)
- `--method`: HTTP method (GET, POST, PUT, DELETE, PATCH)
- `--with-auth`: Include JWT token from localStorage
- `--data`: JSON data for request body

## What It Does

1. Reads API base URL from environment
2. Gets JWT token if `--with-auth` flag used
3. Makes fetch request with proper headers
4. Displays request and response details
5. Shows any errors in user-friendly format

## Expected Output

### Successful Request
```
=== API Test Results ===
URL: http://localhost:8000/tasks
Method: GET
Headers: {
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJ..."
}

Status: 200 OK
Response: [
  {
    "id": 1,
    "title": "Test Task",
    "completed": false
  }
]

✓ API call successful!
```

### Failed Request
```
=== API Test Results ===
URL: http://localhost:8000/tasks
Method: GET

Status: 401 Unauthorized
Error: {
  "detail": "Could not validate credentials"
}

✗ API call failed!

Possible issues:
- Token expired or invalid
- User not authenticated
- Backend not running
```

## Test Scenarios

### 1. Test Backend Connection
```bash
/frontend:test-api-call / --method GET
```
Should return: `{"message": "Todo API is running!"}`

### 2. Test Authentication
```bash
# First login to get token
/frontend:test-api-call /auth/login --method POST --data '{"email":"user@test.com","password":"password123"}'

# Then test protected endpoint
/frontend:test-api-call /tasks --with-auth
```

### 3. Test Task Creation
```bash
/frontend:test-api-call /tasks --method POST --with-auth --data '{"title":"New Task","description":"Test description"}'
```

### 4. Test Task Update
```bash
/frontend:test-api-call /tasks/1 --method PUT --with-auth --data '{"title":"Updated Task","completed":true}'
```

## Debugging Information

The skill shows:
- Full request URL
- HTTP method
- Request headers
- Request body (if any)
- Response status code
- Response body
- Detailed error messages

## Common Issues & Solutions

### CORS Error
```
Error: No 'Access-Control-Allow-Origin' header

Solution:
- Check backend CORS configuration
- Ensure backend allows frontend origin
- Restart backend server
```

### Network Error
```
Error: Failed to fetch

Solution:
- Check backend is running on port 8000
- Verify NEXT_PUBLIC_API_BASE_URL in .env.local
- Test backend: curl http://localhost:8000/
```

### 401 Unauthorized
```
Error: Could not validate credentials

Solution:
- Login again to get fresh token
- Check token in localStorage: localStorage.getItem('access_token')
- Verify token format: should be "Bearer <token>"
```

### 404 Not Found
```
Error: Not Found

Solution:
- Check endpoint path is correct
- Verify endpoint exists in backend
- Check for typos in URL
```

### 400 Bad Request
```
Error: Validation error

Solution:
- Check request data format
- Ensure required fields are provided
- Verify data types match schema
```

## Token Management

### Check Token
```javascript
const token = localStorage.getItem('access_token');
console.log('Token exists:', !!token);
console.log('Token:', token?.substring(0, 20) + '...');
```

### Manual Token Test
```bash
# Copy token from localStorage
# Then test with curl:
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/tasks
```

## Response Format

### Success Response (200-299)
```json
{
  "data": [...],
  "status": 200
}
```

### Error Response (400-599)
```json
{
  "detail": "Error message",
  "status": 401
}
```

## Integration with Test Page

This skill powers the test page at `/test`:
- Button 1: Tests backend connection
- Button 2: Checks token in localStorage
- Button 3: Tests authenticated endpoint

Visit: http://localhost:3000/test

## Using in Code

The test logic can be replicated in your components:

```typescript
const testApiCall = async () => {
  const token = localStorage.getItem('access_token');

  try {
    const response = await fetch('http://localhost:8000/tasks', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Success:', data);
    } else {
      const error = await response.json();
      console.error('Error:', error);
    }
  } catch (err) {
    console.error('Network error:', err);
  }
};
```

## Performance Testing

Test API response times:
```bash
# Measure request timing
/frontend:test-api-call /tasks --benchmark

Output:
Request time: 45ms
Response time: 120ms
Total time: 165ms
```

## Bulk Testing

Test multiple endpoints:
```bash
/frontend:test-api-call --run-suite

Tests:
✓ GET / (12ms)
✓ POST /auth/login (234ms)
✓ GET /tasks (89ms)
✓ POST /tasks (156ms)

4/4 tests passed
```

## Related Skills

- `check-auth` - Verify authentication status
- `run-frontend` - Start dev server
- `test-frontend` - Test frontend build

## Quick Troubleshooting

1. **Backend not responding**
   - Run: `/backend:run-backend`

2. **No token found**
   - Login at: http://localhost:3000/auth/login

3. **CORS errors**
   - Check backend CORS settings
   - Restart both servers

4. **Request hangs**
   - Check network tab in DevTools
   - Verify backend isn't crashed
   - Check for infinite loops
