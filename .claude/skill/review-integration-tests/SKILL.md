---
name: review-integration-tests
description: Reviews integration test completeness for Todo app Phase I API endpoints and database interactions. Use when validating end-to-end workflows, API contract compliance, or multi-component interactions.
owner: QA Agent
---

# Review Integration Tests

## Purpose
Ensures integration tests validate complete workflows in Todo app Phase I, including API endpoints, database operations, and authentication flows. Verifies tests cover happy paths, error scenarios, and data consistency across components.

## When to Use
- After implementing new API endpoints for todo CRUD operations
- When adding authentication middleware or user management features
- Before merging features that involve database transactions
- During Phase I completion checklist validation
- When integration test suite execution time exceeds 30 seconds

## Inputs
- `test_directory`: Path to integration test files (e.g., `tests/integration/`)
- `api_spec_file`: OpenAPI/Swagger specification file path
- `database_schema`: Database schema file or migration directory
- `auth_config`: Authentication configuration (JWT, OAuth, etc.)
- `test_environment`: Environment configuration (test database URL, mock services)

## Step-by-Step Process

### 1. Inventory Integration Tests
- Scan integration test directory for test files
- Parse test names and group by feature area (todos, users, auth)
- Extract API endpoint calls from test code
- Count tests per endpoint and HTTP method

### 2. Validate API Coverage
- Load API specification from `api_spec_file`
- Map each endpoint to corresponding integration tests
- Identify untested endpoints and HTTP methods
- Check for tests covering all required request/response scenarios:
  - Valid requests with expected responses
  - Invalid requests with proper error codes
  - Authentication failures (401, 403)
  - Validation errors (400, 422)

### 3. Verify Database Interactions
- Identify database operations in tests (INSERT, UPDATE, DELETE, SELECT)
- Validate transaction boundaries and rollback scenarios
- Check for database state cleanup after each test
- Ensure tests verify data consistency:
  - Foreign key constraints honored
  - Cascade deletes work correctly
  - Unique constraints enforced

### 4. Check Authentication Flow
For Phase I authentication, verify tests cover:
- User registration with valid credentials
- Login with correct/incorrect passwords
- Token generation and validation
- Protected endpoint access with/without valid token
- Token expiration handling

### 5. Analyze Test Data Management
- Verify tests use isolated test data (no shared fixtures causing flaky tests)
- Check for proper setup/teardown of test database
- Ensure tests don't rely on execution order
- Validate no hardcoded production data in tests

### 6. Evaluate Performance Boundaries
- Measure total integration test execution time
- Identify slow tests (>5 seconds individual execution)
- Check for unnecessary database queries (N+1 problems)
- Recommend optimization for tests exceeding time budgets

### 7. Generate Review Report
- Summarize coverage by feature area
- List gaps in endpoint coverage
- Report data consistency issues found
- Provide actionable recommendations with priority

## Output

### Success Case
```json
{
  "status": "PASSED",
  "total_integration_tests": 23,
  "api_coverage": {
    "endpoints_tested": 12,
    "endpoints_total": 12,
    "coverage_percentage": 100.0,
    "untested_endpoints": []
  },
  "database_validation": {
    "transaction_safety": "PASSED",
    "constraint_checks": "PASSED",
    "cleanup_verified": "PASSED"
  },
  "authentication_coverage": {
    "registration": "PASSED",
    "login": "PASSED",
    "token_validation": "PASSED",
    "protected_routes": "PASSED"
  },
  "performance": {
    "total_execution_time": "18.7s",
    "slowest_test": {
      "name": "test_bulk_todo_creation",
      "duration": "3.2s"
    },
    "within_budget": true
  },
  "test_isolation": "PASSED",
  "recommendations": []
}
```

### Failure Case
```json
{
  "status": "FAILED",
  "total_integration_tests": 23,
  "api_coverage": {
    "endpoints_tested": 10,
    "endpoints_total": 12,
    "coverage_percentage": 83.3,
    "untested_endpoints": [
      "DELETE /api/todos/:id (authentication required)",
      "PATCH /api/users/:id/profile"
    ]
  },
  "database_validation": {
    "transaction_safety": "PASSED",
    "constraint_checks": "FAILED",
    "cleanup_verified": "FAILED"
  },
  "authentication_coverage": {
    "registration": "PASSED",
    "login": "PASSED",
    "token_validation": "FAILED",
    "protected_routes": "PASSED"
  },
  "violations": [
    {
      "category": "api_coverage",
      "severity": "HIGH",
      "issue": "DELETE endpoint not tested for authorization",
      "file": "tests/integration/test_todos.py",
      "recommendation": "Add test verifying only todo owner can delete"
    },
    {
      "category": "database_cleanup",
      "severity": "HIGH",
      "issue": "Test data persists after test completion",
      "file": "tests/integration/test_user_registration.py",
      "line": 78,
      "recommendation": "Add teardown method to remove test users"
    },
    {
      "category": "token_validation",
      "severity": "MEDIUM",
      "issue": "Expired token test missing",
      "file": "tests/integration/test_auth.py",
      "recommendation": "Add test with expired JWT to verify 401 response"
    }
  ],
  "performance": {
    "total_execution_time": "34.2s",
    "slowest_test": {
      "name": "test_concurrent_todo_updates",
      "duration": "12.8s"
    },
    "within_budget": false,
    "slow_tests": [
      {
        "name": "test_concurrent_todo_updates",
        "duration": "12.8s",
        "issue": "Excessive database commits without batching"
      }
    ]
  },
  "recommendations": [
    "Add integration tests for DELETE /api/todos/:id with authorization checks",
    "Implement database cleanup in teardown for test_user_registration.py",
    "Add expired token validation test in test_auth.py",
    "Optimize test_concurrent_todo_updates using database transaction batching"
  ]
}
```

## Failure Handling

### Untested API Endpoints
- **Action**: Generate test template for missing endpoint
- **Output**: Skeleton test code with TODO comments for assertions
- **Recommendation**: Provide example test for similar endpoint as reference
- **Blocking**: HIGH severity if endpoint handles authentication or data modification

### Database State Leakage
- **Action**: Run test in isolation and inspect database after execution
- **Output**: List of orphaned records with table names and IDs
- **Recommendation**: Generate teardown code template for cleanup
- **Blocking**: HIGH severity - causes flaky tests and false positives

### Missing Authentication Tests
- **Action**: Cross-reference protected routes with auth test coverage
- **Output**: List of protected endpoints without auth failure tests
- **Recommendation**: Provide auth test template for Phase I JWT validation
- **Blocking**: HIGH severity - security requirement for Phase I

### Performance Budget Exceeded
- **Action**: Profile slow tests to identify bottlenecks
- **Output**: Execution time breakdown with database query counts
- **Recommendation**: Suggest using test database seeding vs. per-test inserts
- **Blocking**: MEDIUM severity - impacts developer productivity

### Test Dependency Detected
- **Action**: Run tests in random order and capture failures
- **Output**: List of tests failing when run in isolation
- **Recommendation**: Refactor to use independent fixtures
- **Blocking**: HIGH severity - violates test isolation principle

### API Spec Mismatch
- **Action**: Compare actual endpoint signatures with spec
- **Output**: Differences in request/response schemas
- **Recommendation**: Update tests or API implementation to match spec
- **Blocking**: HIGH severity - contract violation

## Deterministic Behavior
- Tests always executed in alphabetical order by filename
- Database seeded with identical fixture data on each run
- Environment variables loaded from `.env.test` (never `.env`)
- Test results cached with input hash to skip redundant validations
- Coverage thresholds: API endpoints 100%, auth flows 100%, error cases 95%
- Exit codes: 0 (passed), 1 (failed validations), 2 (environment setup error)
