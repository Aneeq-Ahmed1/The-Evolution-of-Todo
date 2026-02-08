# Frontend Skill: Run Frontend

## Skill Name
`run-frontend`

## Description
Start the Next.js development server with hot-reload and optimal configuration.

## Usage
```
/frontend:run-frontend [--port PORT] [--turbo]
```

## Default Behavior
```bash
cd frontend
npm run dev
```

## Options

- `--port PORT`: Custom port (default: 3000)
- `--turbo`: Enable Turbopack for faster builds
- `--host HOST`: Bind to specific host (default: localhost)

## What It Does

1. Changes to frontend directory
2. Loads environment variables from `.env.local`
3. Starts Next.js development server
4. Enables hot module replacement (HMR)
5. Provides access to application at http://localhost:3000

## Expected Output

```
▲ Next.js 15.0.0
- Local:        http://localhost:3000
- Network:      http://192.168.1.x:3000

✓ Ready in 2.3s
```

## Development Features

- ✅ Hot Module Replacement (HMR)
- ✅ Fast Refresh for React components
- ✅ TypeScript type checking
- ✅ CSS hot reloading
- ✅ API route handling
- ✅ Error overlay in browser

## Health Check

After starting, the skill will verify:
- Server is responding at http://localhost:3000/
- No build errors in terminal
- TypeScript compilation successful

## Available Routes

Once running:
- **Landing:** http://localhost:3000/
- **Login:** http://localhost:3000/auth/login
- **Register:** http://localhost:3000/auth/register
- **Tasks:** http://localhost:3000/dashboard/tasks
- **Test:** http://localhost:3000/test

## Hot Reload

Automatically reloads when you edit:
- React components (.tsx, .jsx)
- TypeScript files (.ts)
- CSS/Tailwind files
- Page files
- Layout files

Changes appear instantly without full page reload.

## Environment Variables

Reads from `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

### Port Already in Use
```
Error: Port 3000 is already in use

Solution: Kill process or use different port
/frontend:run-frontend --port 3001
```

### Module Not Found
```
Error: Cannot find module 'react'

Solution: Install dependencies
cd frontend && npm install
```

### TypeScript Errors
```
Error: Type 'string' is not assignable to type 'number'

Solution: Fix TypeScript errors in code
Check terminal output for file locations
```

### Build Failed
```
Error: Failed to compile

Solution: Check terminal for specific errors
Fix syntax errors or import issues
```

## Development Mode Features

- Fast Refresh enabled
- Detailed error messages
- Source maps for debugging
- React DevTools compatible
- Console warnings visible

## Browser Console

Open with F12 to see:
- API request logs
- Component errors
- State changes
- Network activity

## Performance Tips

- Use `--turbo` for faster builds
- Close unused browser tabs
- Clear browser cache if needed
- Restart server if memory high

## Pre-Start Checklist

Before running:
1. ✓ Backend is running on port 8000
2. ✓ `.env.local` file exists
3. ✓ `node_modules` installed
4. ✓ No TypeScript errors

## Post-Start Verification

Skill automatically tests:
```bash
✓ Server responding: http://localhost:3000/
✓ No compilation errors
✓ Environment variables loaded
✓ Backend connection available
```

## Stopping Server

- Press `Ctrl+C` in terminal
- Or close the terminal window
- Or use skill: `/frontend:stop-frontend`

## Related Skills

- `test-frontend` - Check for errors before running
- `build-frontend` - Build for production
- `test-api-call` - Test backend connection

## Quick Start Sequence

```bash
# 1. Install dependencies (first time)
cd frontend && npm install

# 2. Start backend first
cd ../backend && python -m src.main

# 3. Start frontend
/frontend:run-frontend

# 4. Open browser
http://localhost:3000
```

## Common Workflows

### Development Loop
1. Start server with `run-frontend`
2. Edit files in code editor
3. Save file
4. See changes instantly in browser
5. Check console for errors
6. Repeat

### Testing Changes
1. Make code changes
2. Check browser updates
3. Open DevTools (F12)
4. Check console for errors
5. Test user interactions
6. Verify API calls work

## Memory Management

If server becomes slow:
- Restart with Ctrl+C then `run-frontend`
- Clear browser cache
- Close unused tabs
- Check for memory leaks in code

## Production Build

For production:
```bash
/frontend:build-frontend
npm start
```

This creates optimized build without HMR.
