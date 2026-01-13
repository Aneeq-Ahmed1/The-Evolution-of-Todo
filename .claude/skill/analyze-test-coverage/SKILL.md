---
name: analyze-test-coverage
description: Analyzes and reports comprehensive test coverage metrics for Todo app Phase I codebase. Use when measuring code coverage, identifying gaps, or enforcing quality gates before deployment.
owner: QA Agent
---

# Analyze Test Coverage

## Purpose
Provides detailed analysis of test coverage across Todo app Phase I codebase, including line, branch, and function coverage. Identifies critical gaps, generates actionable reports, and enforces minimum coverage thresholds for production readiness.

## When to Use
- Before merging pull requests to main branch
- During Phase I completion verification
- When coverage metrics are needed for quality dashboards
- After adding new features to measure coverage impact
- Before deployment to staging or production environments
- When investigating failing quality gates

## Inputs
- `source_directory`: Path to source code (e.g., `src/`)
- `test_directory`: Path to all tests (e.g., `tests/`)
- `coverage_tool`: Tool to use (pytest-cov, jest, c8, nyc)
- `minimum_thresholds`: Coverage requirements object
  ```json
  {
    "line": 80,
    "branch": 75,
    "function": 85,
    "statement": 80
  }
  ```
- `exclude_patterns`: Files/directories to exclude (e.g., `["**/*.config.js", "migrations/"]`)
- `critical_files`: High-priority files requiring 100% coverage (e.g., `["auth.py", "user_service.py"]`)
- `output_format`: Report format (json, html, lcov, text, cobertura)

## Step-by-Step Process

### 1. Environment Setup
- Verify coverage tool is installed and configured
- Check test environment is properly initialized
- Validate source and test directories exist
- Load coverage configuration from `.coveragerc` or `jest.config.js`

### 2. Execute Test Suite with Coverage
- Run all tests (unit + integration) with coverage tracking enabled
- Capture coverage data for each source file
- Record execution time and test results
- Generate raw coverage report in specified format

### 3. Parse Coverage Data
- Extract coverage metrics per file:
  - Line coverage: percentage of executable lines hit
  - Branch coverage: percentage of conditional branches taken
  - Function coverage: percentage of functions called
  - Statement coverage: percentage of statements executed
- Calculate aggregate metrics across entire codebase
- Identify files with zero coverage

### 4. Identify Coverage Gaps
- List uncovered lines with code snippets
- Highlight uncovered branches with conditions
- Flag untested functions with signatures
- Categorize gaps by severity:
  - CRITICAL: Security/auth code, data validation, error handling
  - HIGH: Core business logic (todo CRUD, user management)
  - MEDIUM: Utility functions, helpers
  - LOW: Logging, configuration loaders

### 5. Validate Against Thresholds
- Compare actual coverage vs. minimum thresholds per metric
- Check critical files have 100% coverage
- Verify no regression from previous coverage baseline
- Calculate coverage delta if baseline exists

### 6. Generate Detailed Report
- Create summary with overall metrics
- List top 10 files needing coverage improvement
- Provide specific recommendations for gap closure
- Generate visualizations if HTML format requested

### 7. Archive Coverage Data
- Save coverage report to `.coverage/` directory with timestamp
- Store baseline metrics for future comparison
- Update coverage badge metadata for README
- Export metrics for CI/CD pipeline

## Output

### Success Case
```json
{
  "status": "PASSED",
  "timestamp": "2025-12-30T14:30:00Z",
  "coverage_summary": {
    "line": 87.3,
    "branch": 82.1,
    "function": 91.5,
    "statement": 88.2
  },
  "thresholds_met": {
    "line": true,
    "branch": true,
    "function": true,
    "statement": true
  },
  "total_files_analyzed": 24,
  "files_with_full_coverage": 18,
  "files_below_threshold": [],
  "critical_files_coverage": {
    "src/auth/jwt_handler.py": 100.0,
    "src/services/user_service.py": 100.0,
    "src/models/user.py": 100.0
  },
  "coverage_delta": {
    "line": "+2.3",
    "branch": "+1.8",
    "function": "+0.5"
  },
  "report_paths": {
    "html": ".coverage/coverage-2025-12-30-143000/index.html",
    "json": ".coverage/coverage-2025-12-30-143000/coverage.json",
    "lcov": ".coverage/coverage-2025-12-30-143000/lcov.info"
  },
  "test_execution_time": "22.4s",
  "recommendations": []
}
```

### Failure Case
```json
{
  "status": "FAILED",
  "timestamp": "2025-12-30T14:30:00Z",
  "coverage_summary": {
    "line": 72.8,
    "branch": 68.3,
    "function": 80.2,
    "statement": 74.1
  },
  "thresholds_met": {
    "line": false,
    "branch": false,
    "function": false,
    "statement": false
  },
  "total_files_analyzed": 24,
  "files_with_full_coverage": 12,
  "files_below_threshold": [
    {
      "file": "src/services/todo_service.py",
      "line_coverage": 65.2,
      "branch_coverage": 58.7,
      "missing_lines": [45, 46, 52-58, 72-75],
      "severity": "HIGH",
      "reason": "Core business logic for todo CRUD operations"
    },
    {
      "file": "src/middleware/auth_middleware.py",
      "line_coverage": 70.5,
      "branch_coverage": 62.3,
      "missing_lines": [23-28, 34],
      "severity": "CRITICAL",
      "reason": "Authentication and authorization logic"
    }
  ],
  "critical_files_coverage": {
    "src/auth/jwt_handler.py": 100.0,
    "src/services/user_service.py": 87.3,
    "src/models/user.py": 100.0
  },
  "coverage_gaps": [
    {
      "file": "src/services/todo_service.py",
      "function": "update_todo",
      "uncovered_branches": [
        {
          "line": 52,
          "condition": "if not todo.owner_id == user_id",
          "branch": "false branch not tested",
          "code_snippet": "if not todo.owner_id == user_id:\n    raise UnauthorizedError()"
        }
      ],
      "severity": "CRITICAL",
      "recommendation": "Add test for unauthorized todo update attempt"
    },
    {
      "file": "src/middleware/auth_middleware.py",
      "function": "verify_token",
      "uncovered_lines": [23, 24, 25],
      "code_snippet": "except jwt.ExpiredSignatureError:\n    return None\n",
      "severity": "CRITICAL",
      "recommendation": "Add test for expired JWT token handling"
    }
  ],
  "coverage_delta": {
    "line": "-3.7",
    "branch": "-2.1",
    "function": "+0.2"
  },
  "regression_detected": true,
  "recommendations": [
    "Add unit test for unauthorized todo update (todo_service.py:52)",
    "Add integration test for expired JWT token (auth_middleware.py:23-25)",
    "Increase overall line coverage from 72.8% to 80% minimum (7.2% gap)",
    "Increase branch coverage from 68.3% to 75% minimum (6.7% gap)",
    "Critical file src/services/user_service.py requires 100% coverage (currently 87.3%)"
  ]
}
```

## Failure Handling

### Coverage Below Threshold
- **Action**: Generate prioritized list of files to improve
- **Output**: Specific uncovered lines with code snippets and severity
- **Recommendation**: Provide test templates for uncovered code paths
- **Blocking**: HIGH severity - prevents merge to main branch
- **Recovery**: Run `analyze-test-coverage --show-gaps --priority=HIGH` to get focused action items

### Coverage Tool Not Found
- **Action**: Detect project type and recommend appropriate tool
- **Output**: Installation commands for detected language/framework
- **Recommendation**: Add coverage tool to `package.json` or `requirements.txt`
- **Blocking**: CRITICAL - cannot proceed without coverage tool
- **Recovery**: Install tool and re-run analysis

### Critical Files Below 100%
- **Action**: Highlight critical files (auth, security, data validation)
- **Output**: Detailed gap report for each critical file
- **Recommendation**: Write specific tests for uncovered critical code
- **Blocking**: CRITICAL - security/auth code must be fully tested
- **Recovery**: Add tests until critical files reach 100%, then re-run

### Coverage Regression Detected
- **Action**: Compare current coverage with baseline from previous run
- **Output**: Delta report showing which files lost coverage
- **Recommendation**: Identify commits that reduced coverage
- **Blocking**: MEDIUM severity - flag for review
- **Recovery**: Restore coverage to baseline level or justify regression

### Test Suite Failure
- **Action**: Report test failures preventing coverage analysis
- **Output**: List of failing tests with error messages
- **Recommendation**: Fix failing tests before measuring coverage
- **Blocking**: CRITICAL - coverage invalid if tests fail
- **Recovery**: Run `validate-unit-tests` to identify and fix test issues

### Invalid Coverage Data
- **Action**: Verify coverage report format and integrity
- **Output**: Validation errors in coverage data file
- **Recommendation**: Re-run tests with clean environment
- **Blocking**: CRITICAL - cannot trust invalid data
- **Recovery**: Delete `.coverage/` cache and re-run with fresh test execution

### Excluded Files Misconfiguration
- **Action**: Validate exclude patterns against actual file structure
- **Output**: List of excluded files and justification check
- **Recommendation**: Review exclusions to ensure no critical code is skipped
- **Blocking**: LOW severity - informational warning
- **Recovery**: Update exclude patterns in configuration file

## Deterministic Behavior
- Coverage always calculated with same test execution order
- Thresholds loaded from `.qa/coverage-thresholds.json` (version controlled)
- Baseline stored in `.coverage/baseline.json` (updated only on main branch)
- Reports timestamped with ISO 8601 format for consistent sorting
- Metric rounding: always 1 decimal place, round half up
- Exit codes: 0 (passed all thresholds), 1 (below threshold), 2 (tool error), 3 (regression detected)
- Coverage data cached with git commit SHA for reproducibility
- HTML report colors: green (≥90%), yellow (75-89%), red (<75%)
