---
name: validate-unit-tests
description: Validates unit test quality, coverage, and compliance for Todo app Phase I components. Use when reviewing or creating unit tests for todo items, user authentication, or core business logic.
owner: QA Agent
---

# Validate Unit Tests

## Purpose
Ensures unit tests for the Todo app Phase I meet quality standards, achieve minimum coverage thresholds, and follow TDD principles. Validates test isolation, assertion quality, and edge case coverage for todo CRUD operations and user management.

## When to Use
- After implementing new features in Phase I (todo items, users, authentication)
- Before merging pull requests that add or modify business logic
- During code review when test files are added or changed
- When test coverage drops below 80% threshold
- Before progressing from Red to Green phase in TDD cycle

## Inputs
- `test_directory`: Path to test files (e.g., `tests/unit/`)
- `coverage_threshold`: Minimum coverage percentage (default: 80)
- `test_framework`: Testing framework used (e.g., pytest, jest, vitest)
- `source_files`: Paths to source files being tested

## Step-by-Step Process

### 1. Scan Test Files
- Locate all test files matching pattern `test_*.py`, `*.test.ts`, or framework-specific patterns
- Parse test file structure to identify test functions/methods
- Count total number of unit tests found

### 2. Validate Test Structure
- Verify each test follows Arrange-Act-Assert pattern
- Check test naming conventions (descriptive, includes scenario and expected outcome)
- Ensure tests are isolated (no shared state, proper setup/teardown)
- Confirm no database or external API calls (mocks/stubs required)

### 3. Analyze Test Coverage
- Execute coverage analysis tool (pytest-cov, c8, nyc)
- Generate coverage report for source files
- Identify uncovered lines and branches
- Calculate coverage percentages: line, branch, function

### 4. Verify Assertions
- Check each test contains at least one assertion
- Validate assertion specificity (no generic assertTrue on complex objects)
- Ensure error cases have assertions for exception type and message
- Confirm no commented-out assertions

### 5. Check Edge Cases
For Todo app Phase I, verify tests cover:
- **Todo Items**: Empty title, max length title, special characters, null values
- **User Authentication**: Invalid credentials, expired tokens, missing fields
- **CRUD Operations**: Create duplicate, read non-existent, update with invalid data, delete already deleted

### 6. Generate Validation Report
- List all passed validation rules
- Report violations with file path and line number
- Show coverage gaps with specific uncovered code blocks
- Provide prioritized recommendations

## Output

### Success Case
```json
{
  "status": "PASSED",
  "total_tests": 47,
  "coverage": {
    "line": 87.3,
    "branch": 82.1,
    "function": 91.5
  },
  "validation_results": {
    "structure": "PASSED",
    "isolation": "PASSED",
    "assertions": "PASSED",
    "edge_cases": "PASSED"
  },
  "test_execution_time": "2.3s",
  "recommendations": []
}
```

### Failure Case
```json
{
  "status": "FAILED",
  "total_tests": 47,
  "coverage": {
    "line": 73.2,
    "branch": 68.5,
    "function": 80.0
  },
  "validation_results": {
    "structure": "PASSED",
    "isolation": "FAILED",
    "assertions": "PASSED",
    "edge_cases": "FAILED"
  },
  "violations": [
    {
      "rule": "test_isolation",
      "file": "tests/unit/test_todo_service.py",
      "line": 45,
      "issue": "Test modifies global state without cleanup",
      "severity": "HIGH"
    },
    {
      "rule": "edge_case_coverage",
      "file": "tests/unit/test_auth.py",
      "missing": "Token expiration scenario not tested",
      "severity": "MEDIUM"
    }
  ],
  "coverage_gaps": [
    {
      "file": "src/services/todo_service.py",
      "uncovered_lines": [67, 68, 72-75],
      "reason": "Error handling branch not tested"
    }
  ],
  "recommendations": [
    "Add test for token expiration in test_auth.py",
    "Fix global state mutation in test_todo_service.py:45",
    "Increase coverage to 80% minimum (currently 73.2%)"
  ]
}
```

## Failure Handling

### Coverage Below Threshold
- **Action**: Generate detailed coverage report showing gaps
- **Output**: List specific uncovered lines with code snippets
- **Recommendation**: Suggest specific test cases to add based on uncovered branches

### Test Isolation Violation
- **Action**: Identify shared state or side effects
- **Output**: List affected tests and shared resources
- **Recommendation**: Provide refactoring guidance using fixtures/mocks
- **Blocking**: Mark as HIGH severity - must fix before merge

### Missing Edge Cases
- **Action**: Compare against Phase I edge case checklist
- **Output**: List missing scenarios from standard checklist
- **Recommendation**: Generate test skeleton for missing cases
- **Blocking**: Mark as MEDIUM severity - required for production

### Test Framework Not Found
- **Action**: Check for framework dependencies in package files
- **Output**: Error message with detected project type
- **Recommendation**: Provide installation command for appropriate framework
- **Blocking**: Cannot proceed - exit with error code 1

### No Tests Found
- **Action**: Verify test directory path and naming conventions
- **Output**: Expected patterns and searched locations
- **Recommendation**: Provide example test structure for Phase I
- **Blocking**: Exit with error code 2 - tests required for validation

## Deterministic Behavior
- Always runs tests in same order (alphabetical by file path)
- Coverage thresholds are fixed unless explicitly overridden
- Validation rules are version-controlled in `.qa/rules/unit-test-rules.json`
- Reports always use same JSON schema for parsing automation
- Exit codes: 0 (success), 1 (validation failed), 2 (no tests found)
