# Debugging "Failed to fetch" Error

## Problem
Frontend shows: `TypeError: Failed to fetch` when loading tasks

## Backend Status
✅ Backend IS running on port 8000

## Root Causes

### 1. CORS Issue (Most Common)
Browser blocking requests due to CORS policy

### 2. Wrong API URL
Frontend trying to connect to wrong URL

### 3. Network/Firewall
Localhost blocked or firewall interfering

### 4. Browser Cache
Stale service workers or cached files

---

## Solution Steps

### Step 1: Verify Environment Variable

Check `frontend/.env.local`:
```bash
cd frontend
cat .env.local
```

Should show:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

If missing or wrong, create/fix it:
```bash
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

### Step 2: Restart Frontend (IMPORTANT!)

```bash
# In frontend terminal
Ctrl+C  # Stop current server

# Clear Next.js cache
rm -rf .next

# Restart
npm run dev
```

### Step 3: Clear Browser Cache

1. Close ALL browser tabs with localhost:3000
2. Press `Ctrl+Shift+Del`
3. Check "Cached images and files"
4. Click "Clear data"
5. Close browser completely
6. Reopen browser
7. Go to `http://localhost:3000`

### Step 4: Test Backend Directly

Open new browser tab:
```
http://localhost:8000/
```

Should show:
```json
{"message":"Todo API is running!"}
```

If this works, backend is fine.

### Step 5: Check Browser Console

1. Open browser console (F12)
2. Go to Network tab
3. Try loading tasks
4. Look for the request to `localhost:8000/tasks`

**What to check:**
- Is request appearing?
- What's the status? (Failed, CORS error, 404, etc.)
- Check request headers
- Check response

### Step 6: Test from Test Page

Go to: `http://localhost:3000/test`

Click buttons:
1. "Test Backend Connection" - Should work
2. "Check Token" - Should show token
3. "Test Tasks Endpoint" - Should work if logged in

---

## Quick Fix Script

Run this:

```bash
# Stop everything
# Press Ctrl+C in both terminals

# Backend
cd backend
python -m src.main &

# Frontend - clear and restart
cd frontend
rm -rf .next
npm run dev
```

Then:
1. Close browser
2. Clear cache (Ctrl+Shift+Del)
3. Reopen: http://localhost:3000
4. Login again

---

## Alternative: Try Different Port

Sometimes localhost:8000 has issues. Try:

**Backend on 8001:**
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

**Update frontend/.env.local:**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

**Restart frontend:**
```bash
cd frontend
rm -rf .next
npm run dev
```

---

## Check CORS in Backend

Open `backend/src/main.py` and verify:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This should be present
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Nuclear Option: Fresh Start

If nothing works:

```bash
# Kill all Node and Python processes
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# Wait 5 seconds

# Start backend
cd backend
python -m src.main

# In new terminal, start frontend fresh
cd frontend
rm -rf .next node_modules/.cache
npm run dev

# Close browser completely
# Clear all browsing data
# Reopen: http://localhost:3000
```

---

## Still Not Working?

Try accessing from IP address instead of localhost:

1. Find your IP:
```bash
ipconfig
```

2. Update `frontend/.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://192.168.x.x:8000
```

3. Restart frontend

4. Access at: `http://192.168.x.x:3000`

---

## Enable Detailed Logging

Add this to `frontend/src/lib/api.ts` line 58:

```typescript
console.log('Full fetch config:', {
  url: `${API_BASE_URL}${endpoint}`,
  options: options,
  headers: headers
});

try {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  console.log('Fetch successful, response:', response);
} catch (error) {
  console.error('Fetch failed with error:', error);
  console.error('Error name:', error.name);
  console.error('Error message:', error.message);
  throw error;
}
```

This will show exact error in console.

---

## Common Error Messages

### "Failed to fetch"
- Network problem
- Backend not reachable
- CORS blocking

### "CORS policy"
- CORS not configured
- Wrong origin in CORS

### "net::ERR_CONNECTION_REFUSED"
- Backend not running
- Wrong port

### "Network request failed"
- Firewall blocking
- Antivirus interference

---

## Last Resort: Use Proxy

Add to `frontend/next.config.js`:

```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
};
```

Change API calls to use `/api/` instead of full URL.

---

**Most Likely Fix:**
1. Restart frontend with cache clear
2. Clear browser cache
3. Try again

Run these commands NOW:
```bash
cd frontend
rm -rf .next
npm run dev
```

Then clear browser cache and reload!
