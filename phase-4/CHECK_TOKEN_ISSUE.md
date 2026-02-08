# Debug 401 Unauthorized Issue

## Problem
Backend keeps returning 401 even after login

## Check This in Browser Console (F12)

### Step 1: Check if token exists
```javascript
localStorage.getItem('access_token')
```

Should show something like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Step 2: Check if token is being sent
Open Network tab, filter by "tasks", check the request headers.

Should see:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Manual test with curl

First, login to get a token:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"abc@xyz.com","password":"Test@1234"}'
```

Copy the `access_token` from response.

Then test tasks endpoint:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/tasks
```

---

## Possible Issues

### Issue 1: Token not being sent
**Check:** Browser console → Network tab → tasks request → Headers

**Fix:** Frontend API client issue
- Check `frontend/src/lib/api.ts` line 50-52
- Token should be added to Authorization header

### Issue 2: Token format wrong
**Check:** Should be `Bearer <token>`, not just `<token>`

**Fix:** Line 52 in `api.ts`:
```typescript
headers["Authorization"] = `Bearer ${token}`;
```

### Issue 3: Token expired
**Check:** Login timestamp vs current time (tokens expire in 30 min)

**Fix:** Login again

### Issue 4: SECRET_KEY mismatch
**Check:** Backend `.env` file has SECRET_KEY

**Fix:** Ensure `.env` exists:
```env
SECRET_KEY=5d83eb8196a46b61b7062f24896b477e54a1aea254113b2488dde15aa56e08d5
```

### Issue 5: CORS preflight
**Check:** Backend logs show OPTIONS request before GET

**Fix:** Already handled in CORS middleware

---

## Quick Debug Steps

1. **Clear everything and start fresh:**
```javascript
// In browser console
localStorage.clear()
```

2. **Go to login page:**
```
http://localhost:3000/auth/login
```

3. **Login with:**
- Email: `abc@xyz.com`
- Password: `Test@1234`

(Or register new account)

4. **Check console logs:**
```
=== Loading Tasks ===
Token exists: true
Token preview: eyJ...
API Request: GET http://localhost:8000/tasks
Headers: {Authorization: "Bearer eyJ..."}
```

5. **Check backend terminal:**
Should NOT show 401, should show:
```
INFO: 127.0.0.1:xxxxx - "GET /tasks HTTP/1.1" 200 OK
```

---

## Test Authentication Manually

### In Browser Console:
```javascript
// Get token
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// Test API call
fetch('http://localhost:8000/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(d => console.log('Success:', d))
.catch(e => console.error('Error:', e));
```

If this works but page doesn't, it's a React state issue.
If this fails with 401, it's a token issue.

---

## Common Fixes

### Fix 1: Token not in localStorage
```javascript
// After login, check:
localStorage.getItem('access_token')

// If null, login again
```

### Fix 2: Wrong token format
Check `frontend/src/lib/api.ts` line 52:
```typescript
if (token) {
  headers["Authorization"] = `Bearer ${token}`;  // Must have "Bearer "
}
```

### Fix 3: Backend SECRET_KEY missing
Check `backend/.env` or root `.env`:
```bash
cat .env | grep SECRET_KEY
```

Should show a long hex string.

---

## Ultimate Test

Run this in browser console after login:
```javascript
(async () => {
  const token = localStorage.getItem('access_token');
  console.log('1. Token exists:', !!token);
  console.log('2. Token preview:', token?.substring(0, 30));

  try {
    const response = await fetch('http://localhost:8000/tasks', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    console.log('3. Response status:', response.status);
    const data = await response.json();
    console.log('4. Response data:', data);
  } catch (error) {
    console.error('5. Error:', error);
  }
})();
```

Expected output:
```
1. Token exists: true
2. Token preview: eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...
3. Response status: 200
4. Response data: []
```

If status is 401, there's a problem with token validation.

---

## Last Resort: Check Token Structure

```javascript
// Decode JWT (without verification)
const token = localStorage.getItem('access_token');
const parts = token.split('.');
const payload = JSON.parse(atob(parts[1]));
console.log('Token payload:', payload);
```

Should show:
```javascript
{
  sub: "abc@xyz.com",
  exp: 1234567890
}
```

Check if `exp` (expiration) is in the future:
```javascript
const now = Math.floor(Date.now() / 1000);
const exp = payload.exp;
console.log('Token expired:', now > exp);
```

If expired, login again!

---

**Most Likely Issue:** Token expired or not being sent properly.

**Quick Fix:**
1. `localStorage.clear()`
2. Login again
3. Check if works
