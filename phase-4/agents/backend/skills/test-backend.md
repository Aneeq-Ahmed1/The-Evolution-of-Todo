# Backend Skill: Test Backend

## Skill Name
`test-backend`

## Description
Run comprehensive backend tests to verify all functionality is working correctly.

## Usage
```
/backend:test-backend
```

## What It Does

1. Tests model imports (User, Task)
2. Tests database connection and table creation
3. Tests password hashing and verification
4. Tests user service (create, authenticate)
5. Tests JWT token generation
6. Tests API route imports
7. Provides detailed test results

## Output

```
============================================================
BACKEND TESTING SCRIPT
============================================================

[1/6] Testing model imports...
[OK] Models imported successfully

[2/6] Testing database connection...
[OK] Database connection successful

[3/6] Testing password utilities...
[OK] Password hashing works correctly

[4/6] Testing user service...
[OK] User service works correctly

[5/6] Testing JWT authentication...
[OK] JWT token creation works

[6/6] Testing API routes...
[OK] API routes imported successfully

============================================================
ALL TESTS PASSED [OK]
============================================================

Your backend is ready to run!
Start it with: cd backend && python -m src.main
```

## When to Use

- Before starting the backend server
- After making changes to models or services
- Before committing code
- When debugging issues
- After pulling new changes

## Implementation

Runs: `python test_backend.py`

This executes a comprehensive test suite that validates:
- Python imports work correctly
- Database connectivity
- Business logic functions
- Authentication mechanisms
- API structure

## Success Criteria

All 6 tests must pass:
- [OK] Models imported
- [OK] Database connected
- [OK] Password utilities working
- [OK] User service functional
- [OK] JWT tokens generated
- [OK] API routes loadable

## Failure Handling

If any test fails, the skill will:
1. Show which test failed
2. Display the error message
3. Exit with error code
4. Suggest fixes based on error type

## Related Skills

- `run-backend` - Start the backend server
- `test-endpoint` - Test specific API endpoint
- `check-auth` - Verify authentication
