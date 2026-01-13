---
name: verify-api-contracts
description: Validates API contract compliance between specification and implementation for Todo app Phase I endpoints. Use when verifying OpenAPI specs, request/response schemas, or API versioning requirements.
owner: QA Agent
---

# Verify API Contracts

## Purpose
Ensures Todo app Phase I API implementation strictly adheres to defined contracts in OpenAPI specification. Validates request schemas, response formats, HTTP status codes, authentication requirements, and error responses match specification exactly.

## When to Use
- After implementing new API endpoints for Phase I
- Before merging API changes to main branch
- When updating OpenAPI specification
- During contract-first development validation
- Before publishing API documentation to consumers
- When API integration tests fail unexpectedly

## Inputs
- `spec_file`: Path to OpenAPI specification (e.g., `specs/api/openapi.yaml`)
- `base_url`: API server base URL (e.g., `http://localhost:3000/api`)
- `auth_token`: JWT token for authenticated endpoint testing
- `test_data_file`: JSON file with valid/invalid request examples
- `contract_test_suite`: Path to contract test files (e.g., `tests/contract/`)
- `validation_mode`: Strict (fail on any mismatch) or Permissive (warn on extra fields)

## Step-by-Step Process

### 1. Load API Specification
- Parse OpenAPI specification file (YAML or JSON)
- Extract all endpoint definitions with paths and methods
- Build schema registry for request/response models
- Identify authentication requirements per endpoint
- Validate spec itself is valid OpenAPI 3.x format

### 2. Start API Server
- Check if API server is running at `base_url`
- If not running and auto-start enabled, launch server in test mode
- Verify server health endpoint returns 200 OK
- Wait for server readiness (max 30 seconds)

### 3. Test Each Endpoint

For each endpoint in specification:

#### 3a. Validate Request Schema
- Send valid request matching spec schema
- Send invalid requests violating each constraint:
  - Missing required fields
  - Wrong data types
  - Out-of-range values
  - Extra fields (if strict mode)
- Verify server returns 400/422 for invalid requests with descriptive errors

#### 3b. Validate Response Schema
- Verify response body matches spec schema exactly
- Check all required fields are present
- Validate data types for each field
- Ensure no unexpected fields in strict mode
- Verify nested object structures match spec

#### 3c. Validate HTTP Status Codes
- Confirm successful requests return specified status (200, 201, 204)
- Verify error scenarios return correct codes:
  - 400: Bad Request (validation errors)
  - 401: Unauthorized (missing/invalid token)
  - 403: Forbidden (insufficient permissions)
  - 404: Not Found (resource doesn't exist)
  - 409: Conflict (duplicate resource)
  - 422: Unprocessable Entity (semantic validation)
  - 500: Internal Server Error (server failures)

#### 3d. Validate Authentication
- Test protected endpoints without token → expect 401
- Test with invalid/expired token → expect 401
- Test with valid token but wrong permissions → expect 403
- Test with valid token → expect success

#### 3e. Validate Error Response Format
- Ensure errors follow standard format:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Title is required",
      "details": [
        {
          "field": "title",
          "issue": "missing_required_field"
        }
      ]
    }
  }
  ```

### 4. Validate Phase I Specific Contracts

#### Todo Endpoints
- `POST /api/todos`: Create with title, description, completed status
- `GET /api/todos`: List user's todos with pagination
- `GET /api/todos/:id`: Retrieve single todo, verify owner access
- `PUT /api/todos/:id`: Update todo, verify owner-only modification
- `DELETE /api/todos/:id`: Delete todo, verify owner-only deletion

#### User Endpoints
- `POST /api/users/register`: Create user with email/password validation
- `POST /api/users/login`: Return JWT token on valid credentials
- `GET /api/users/me`: Return current user profile with valid token

### 5. Check API Versioning
- Verify API version in URL path or headers
- Ensure deprecated endpoints return warnings
- Validate version negotiation if multiple versions supported

### 6. Generate Contract Validation Report
- Summarize compliance percentage
- List all contract violations with severity
- Report missing implementations
- Provide specification coverage metrics

## Output

### Success Case
```json
{
  "status": "PASSED",
  "compliance_percentage": 100.0,
  "endpoints_tested": 8,
  "total_test_cases": 47,
  "passed_validations": 47,
  "failed_validations": 0,
  "specification_coverage": {
    "endpoints": "8/8 (100%)",
    "request_schemas": "8/8 (100%)",
    "response_schemas": "12/12 (100%)",
    "error_scenarios": "15/15 (100%)"
  },
  "authentication_validation": "PASSED",
  "versioning_compliance": "PASSED",
  "execution_time": "8.3s",
  "contract_tests_passed": 47,
  "recommendations": []
}
```

### Failure Case
```json
{
  "status": "FAILED",
  "compliance_percentage": 83.7,
  "endpoints_tested": 8,
  "total_test_cases": 47,
  "passed_validations": 39,
  "failed_validations": 8,
  "violations": [
    {
      "endpoint": "POST /api/todos",
      "severity": "HIGH",
      "category": "response_schema",
      "issue": "Response missing 'createdAt' field required by spec",
      "expected": {
        "schema": {
          "id": "string",
          "title": "string",
          "completed": "boolean",
          "createdAt": "string (ISO 8601)"
        }
      },
      "actual": {
        "id": "abc123",
        "title": "Buy milk",
        "completed": false
      },
      "recommendation": "Add 'createdAt' timestamp to Todo model and serializer"
    },
    {
      "endpoint": "PUT /api/todos/:id",
      "severity": "CRITICAL",
      "category": "authorization",
      "issue": "Non-owner can modify todo (should return 403)",
      "test_case": "User B attempting to update User A's todo",
      "expected_status": 403,
      "actual_status": 200,
      "recommendation": "Add ownership check in update handler before modification"
    },
    {
      "endpoint": "POST /api/users/register",
      "severity": "MEDIUM",
      "category": "request_validation",
      "issue": "Server accepts invalid email format",
      "test_case": "Email: 'notanemail'",
      "expected_status": 422,
      "actual_status": 201,
      "recommendation": "Add email format validation in user registration schema"
    },
    {
      "endpoint": "GET /api/todos",
      "severity": "HIGH",
      "category": "response_schema",
      "issue": "Pagination metadata missing in list response",
      "expected": {
        "data": "array",
        "meta": {
          "total": "number",
          "page": "number",
          "pageSize": "number"
        }
      },
      "actual": {
        "data": "[...]"
      },
      "recommendation": "Wrap todos array in paginated response structure per spec"
    }
  ],
  "specification_coverage": {
    "endpoints": "8/8 (100%)",
    "request_schemas": "7/8 (87.5%)",
    "response_schemas": "9/12 (75%)",
    "error_scenarios": "14/15 (93.3%)"
  },
  "missing_implementations": [],
  "recommendations": [
    "Fix authorization check in PUT /api/todos/:id to prevent non-owner updates",
    "Add 'createdAt' field to POST /api/todos response schema",
    "Implement email validation in user registration endpoint",
    "Add pagination metadata to GET /api/todos response"
  ]
}
```

## Failure Handling

### Response Schema Mismatch
- **Action**: Compare actual response with spec schema field-by-field
- **Output**: JSON diff showing missing/extra/mistyped fields
- **Recommendation**: Update serializer or spec to achieve consistency
- **Blocking**: HIGH severity - breaks consumer expectations
- **Recovery**: Fix implementation to match spec, or update spec if intentional change

### Missing Authorization Check
- **Action**: Test protected endpoints with different user contexts
- **Output**: Access control matrix showing which users can access what
- **Recommendation**: Add middleware or decorator for ownership verification
- **Blocking**: CRITICAL severity - security vulnerability
- **Recovery**: Implement authorization logic before allowing merge

### Invalid Error Response Format
- **Action**: Capture actual error responses and compare with standard format
- **Output**: Examples of non-compliant error responses
- **Recommendation**: Create centralized error handler following spec
- **Blocking**: MEDIUM severity - poor API consumer experience
- **Recovery**: Implement error response middleware or wrapper

### API Server Not Running
- **Action**: Attempt to start server if auto-start enabled
- **Output**: Server startup logs and health check status
- **Recommendation**: Ensure server can start in test mode
- **Blocking**: CRITICAL - cannot validate without running server
- **Recovery**: Fix server startup issues, verify dependencies installed

### Specification Parse Error
- **Action**: Validate OpenAPI spec using validator tool
- **Output**: Spec validation errors with line numbers
- **Recommendation**: Fix spec syntax or schema definition errors
- **Blocking**: CRITICAL - invalid spec cannot be tested
- **Recovery**: Lint spec with `openapi-validator` or `swagger-cli validate`

### Missing Test Data
- **Action**: Generate sample test data from spec schemas
- **Output**: Auto-generated valid/invalid request examples
- **Recommendation**: Save generated data to test data file for reuse
- **Blocking**: MEDIUM severity - limits test coverage
- **Recovery**: Use schema-based data generation as fallback

### Endpoint Not Implemented
- **Action**: List endpoints in spec missing from running server
- **Output**: Table of specified vs. implemented endpoints
- **Recommendation**: Implement missing endpoints or remove from spec
- **Blocking**: HIGH severity if endpoint marked required in Phase I
- **Recovery**: Implement stub endpoint or mark as future phase

### Authentication Token Invalid
- **Action**: Attempt to generate fresh token using login endpoint
- **Output**: Token generation success or failure details
- **Recommendation**: Provide valid credentials or refresh token mechanism
- **Blocking**: HIGH severity - cannot test protected endpoints
- **Recovery**: Call `POST /api/users/login` to obtain valid token

## Deterministic Behavior
- Endpoints tested in alphabetical order (by path then method)
- Same test data used on each run (loaded from versioned test data file)
- Validation mode (strict/permissive) set via configuration, not runtime
- Contract test results stored with spec version hash for traceability
- Response time assertions: <200ms for simple CRUD, <500ms for complex queries
- Exit codes: 0 (full compliance), 1 (violations found), 2 (server error), 3 (spec invalid)
- Retry logic: 3 attempts with exponential backoff for network failures
- Timeout: 5 seconds per endpoint request, 30 seconds total server startup
