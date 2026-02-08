# Backend Skill: Run Backend

## Skill Name
`run-backend`

## Description
Start the FastAPI development server with proper configuration and monitoring.

## Usage
```
/backend:run-backend [--port PORT] [--reload] [--log-level LEVEL]
```

## Default Behavior
```bash
cd backend
python -m src.main
```

## Options

- `--port PORT`: Custom port (default: 8000)
- `--reload`: Enable auto-reload on file changes (default: enabled)
- `--log-level LEVEL`: Set logging level (debug, info, warning, error)
- `--host HOST`: Bind to specific host (default: 0.0.0.0)

## What It Does

1. Changes to backend directory
2. Loads environment variables from `.env`
3. Initializes database tables
4. Starts uvicorn server
5. Enables CORS for frontend
6. Provides API documentation at /docs

## Expected Output

```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Health Check

After starting, the skill will verify:
- Server is responding at http://localhost:8000/
- Database tables are created
- API documentation is accessible at /docs

## Server Endpoints

Once running:
- **API Root:** http://localhost:8000/
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Spec:** http://localhost:8000/openapi.json

## Auto-Reload

With `--reload` flag (enabled by default):
- Monitors Python files for changes
- Automatically restarts server
- Preserves database state
- Shows which files triggered reload

## Environment Variables

Reads from `.env`:
```env
DATABASE_URL=sqlite:///./todo.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

## Troubleshooting

### Port Already in Use
```
Error: Address already in use

Solution: Kill process or use different port
/backend:run-backend --port 8001
```

### Database Connection Error
```
Error: DATABASE_URL not set

Solution: Create .env file with DATABASE_URL
```

### Import Errors
```
Error: No module named 'src'

Solution: Ensure you're in backend directory
cd backend && python -m src.main
```

## Development Mode

In development (default):
- ✅ Auto-reload enabled
- ✅ Detailed error traces
- ✅ SQL query logging
- ✅ CORS enabled for all origins
- ✅ API documentation accessible

## Production Mode

For production use:
```bash
/backend:run-backend --no-reload --log-level warning --workers 4
```

Changes:
- ❌ Auto-reload disabled
- ❌ Reduced logging
- ✅ Multiple workers
- ✅ CORS restricted to frontend domain

## Monitoring

While running, monitor:
- Request logs in terminal
- SQL queries (if echo=True)
- Error traces
- Performance metrics

## Stopping Server

- Press `Ctrl+C` in terminal
- Or use skill: `/backend:stop-backend`

## Post-Start Verification

Skill automatically tests:
```bash
✓ Server responding: http://localhost:8000/
✓ API docs available: http://localhost:8000/docs
✓ Health check: {"message": "Todo API is running!"}
```

## Related Skills

- `test-backend` - Test before running
- `test-endpoint` - Test specific endpoints
- `check-auth` - Verify authentication

## Logs Location

Development logs: Terminal output
Production logs: `logs/backend.log` (if configured)

## Performance Tips

- Use `--workers 4` for better concurrency
- Enable database connection pooling
- Use async endpoints for I/O operations
- Monitor memory usage with tools

## Quick Start Sequence

```bash
# 1. Test backend first
/backend:test-backend

# 2. Run server
/backend:run-backend

# 3. Verify in browser
http://localhost:8000/docs
```
