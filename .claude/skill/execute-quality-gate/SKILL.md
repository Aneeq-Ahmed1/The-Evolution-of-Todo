---
name: execute-quality-gate
description: Orchestrates comprehensive quality gate checks for Todo app Phase I before deployment. Use when validating production readiness, pre-merge verification, or release candidate approval.
owner: QA Agent
---

# Execute Quality Gate

## Purpose
Coordinates execution of all quality validation checks for Todo app Phase I, enforcing pass/fail criteria before code can be merged or deployed. Aggregates results from unit tests, integration tests, coverage analysis, API contract verification, security scans, and performance benchmarks into a single quality decision.

## When to Use
- Before merging pull requests to main branch
- Before deploying to staging environment
- Before creating release candidates for production
- After completing Phase I feature implementation
- When manually triggering quality verification in CI/CD pipeline
- During pre-deployment quality audits

## Inputs
- `target_branch`: Branch to validate (default: current branch)
- `quality_profile`: Profile defining gate criteria (e.g., `phase-1-strict`, `phase-1-permissive`)
- `skip_checks`: Optional list of checks to skip (for emergency bypasses)
- `environment`: Target deployment environment (development, staging, production)
- `baseline_ref`: Git reference for baseline comparison (e.g., `main`, `v1.0.0`)
- `fail_fast`: Stop on first failure (true) or run all checks (false)

## Step-by-Step Process

### 1. Load Quality Profile
- Read quality gate configuration from `.qa/profiles/{quality_profile}.json`
- Parse pass criteria for each validation type
- Load environment-specific overrides (production requires stricter gates)
- Validate profile configuration is complete and valid

### 2. Pre-Flight Checks
- Verify git working directory is clean (no uncommitted changes)
- Confirm target branch is up-to-date with remote
- Check all required dependencies are installed
- Validate test environment is properly configured
- Ensure previous artifacts are cleaned (.coverage, test-results, etc.)

### 3. Execute Validation Checks (in order)

#### 3a. Code Quality Checks
- **Linting**: Run ESLint/Pylint/Flake8 with zero tolerance for errors
- **Formatting**: Verify Prettier/Black compliance
- **Type Checking**: Run TypeScript/mypy with strict mode
- **Complexity**: Measure cyclomatic complexity (max 10 per function)
- **Dead Code**: Detect unused imports, variables, functions

#### 3b. Unit Test Validation
- Invoke `validate-unit-tests` skill
- Criteria:
  - All tests pass (0 failures)
  - Line coverage ≥ 80%
  - Branch coverage ≥ 75%
  - Function coverage ≥ 85%
  - No test isolation violations
  - Execution time < 30 seconds

#### 3c. Integration Test Review
- Invoke `review-integration-tests` skill
- Criteria:
  - All tests pass (0 failures)
  - 100% API endpoint coverage
  - 100% authentication flow coverage
  - Database cleanup verified
  - No test data leakage
  - Execution time < 60 seconds

#### 3d. Test Coverage Analysis
- Invoke `analyze-test-coverage` skill
- Criteria:
  - Overall line coverage ≥ 80%
  - Critical files coverage = 100% (auth, user service)
  - No coverage regression vs. baseline
  - Coverage delta ≥ 0 (no decrease allowed)

#### 3e. API Contract Verification
- Invoke `verify-api-contracts` skill
- Criteria:
  - 100% specification compliance
  - All endpoints implemented
  - Request/response schemas match spec
  - Authentication validated
  - Error formats consistent

#### 3f. Security Scans
- **Dependency Vulnerabilities**: Run npm audit / pip-audit
  - Zero HIGH or CRITICAL vulnerabilities
  - Document any MEDIUM vulnerabilities with mitigation plan
- **Static Analysis**: Run Bandit/Semgrep for security issues
  - Zero security hotspots in auth/user code
- **Secret Detection**: Scan for hardcoded credentials/tokens
  - Zero secrets in code or config files

#### 3g. Performance Benchmarks
- **API Response Times**: Test critical endpoints
  - GET /api/todos: < 100ms (p95)
  - POST /api/todos: < 150ms (p95)
  - POST /api/users/login: < 200ms (p95)
- **Database Query Performance**:
  - No N+1 queries detected
  - All queries < 50ms
  - Proper indexes on foreign keys

#### 3h. Build Verification
- **Compilation**: Ensure build completes without errors
- **Bundle Size**: Check bundle size ≤ baseline + 5%
- **Production Build**: Verify production build succeeds
- **Docker Image**: Build and scan container image (if applicable)

### 4. Aggregate Results
- Collect pass/fail status from each validation check
- Calculate overall quality score (percentage of passed checks)
- Identify blocking failures vs. warnings
- Generate consolidated report with all findings

### 5. Generate Quality Gate Decision
- **PASS**: All critical checks passed, merge/deploy allowed
- **FAIL**: One or more critical checks failed, merge/deploy blocked
- **WARNING**: All critical checks passed but warnings present, manual review required

### 6. Archive Results
- Save detailed report to `.qa/reports/quality-gate-{timestamp}.json`
- Export summary to CI/CD system (GitHub Actions, GitLab CI)
- Update quality metrics dashboard
- Send notifications (Slack, email) based on result

## Output

### Success Case
```json
{
  "status": "PASSED",
  "quality_score": 100.0,
  "gate_decision": "APPROVED_FOR_MERGE",
  "timestamp": "2025-12-30T15:45:00Z",
  "target_branch": "feature/todo-crud",
  "quality_profile": "phase-1-strict",
  "environment": "production",
  "execution_time": "142.8s",
  "checks_executed": 8,
  "checks_passed": 8,
  "checks_failed": 0,
  "checks_warned": 0,
  "validation_results": {
    "code_quality": {
      "status": "PASSED",
      "linting": "0 errors",
      "formatting": "compliant",
      "type_checking": "0 errors",
      "complexity": "max 7 (threshold 10)"
    },
    "unit_tests": {
      "status": "PASSED",
      "coverage": {
        "line": 87.3,
        "branch": 82.1,
        "function": 91.5
      }
    },
    "integration_tests": {
      "status": "PASSED",
      "api_coverage": "100%",
      "auth_coverage": "100%"
    },
    "test_coverage": {
      "status": "PASSED",
      "overall": 87.3,
      "critical_files": "100%",
      "delta": "+2.3"
    },
    "api_contracts": {
      "status": "PASSED",
      "compliance": "100%"
    },
    "security": {
      "status": "PASSED",
      "vulnerabilities": "0 HIGH/CRITICAL",
      "secrets": "0 detected"
    },
    "performance": {
      "status": "PASSED",
      "api_p95": "98ms",
      "db_queries": "all < 50ms"
    },
    "build": {
      "status": "PASSED",
      "bundle_size": "428KB (baseline 425KB)"
    }
  },
  "report_path": ".qa/reports/quality-gate-20251230-154500.json",
  "recommendations": []
}
```

### Failure Case
```json
{
  "status": "FAILED",
  "quality_score": 75.0,
  "gate_decision": "BLOCKED",
  "timestamp": "2025-12-30T15:45:00Z",
  "target_branch": "feature/todo-crud",
  "quality_profile": "phase-1-strict",
  "environment": "production",
  "execution_time": "89.2s",
  "checks_executed": 8,
  "checks_passed": 6,
  "checks_failed": 2,
  "checks_warned": 0,
  "validation_results": {
    "code_quality": {
      "status": "PASSED",
      "linting": "0 errors",
      "formatting": "compliant"
    },
    "unit_tests": {
      "status": "FAILED",
      "coverage": {
        "line": 72.8,
        "branch": 68.3,
        "function": 80.2
      },
      "reason": "Line coverage below 80% threshold"
    },
    "integration_tests": {
      "status": "PASSED",
      "api_coverage": "100%"
    },
    "test_coverage": {
      "status": "FAILED",
      "overall": 72.8,
      "critical_files": "87.3% (requires 100%)",
      "delta": "-3.7",
      "reason": "Coverage regression detected"
    },
    "api_contracts": {
      "status": "PASSED",
      "compliance": "100%"
    },
    "security": {
      "status": "PASSED",
      "vulnerabilities": "0 HIGH/CRITICAL"
    },
    "performance": {
      "status": "PASSED",
      "api_p95": "102ms"
    },
    "build": {
      "status": "PASSED",
      "bundle_size": "431KB"
    }
  },
  "blocking_issues": [
    {
      "check": "unit_tests",
      "severity": "CRITICAL",
      "issue": "Line coverage 72.8% below required 80%",
      "gap": "7.2%",
      "recommendation": "Add tests to increase coverage by 7.2 percentage points"
    },
    {
      "check": "test_coverage",
      "severity": "CRITICAL",
      "issue": "Critical file src/services/user_service.py has 87.3% coverage (requires 100%)",
      "recommendation": "Add tests for uncovered lines in user_service.py"
    },
    {
      "check": "test_coverage",
      "severity": "HIGH",
      "issue": "Coverage regression: -3.7% from baseline",
      "recommendation": "Restore coverage to previous level or justify regression"
    }
  ],
  "report_path": ".qa/reports/quality-gate-20251230-154500.json",
  "recommendations": [
    "CRITICAL: Increase line coverage from 72.8% to 80% minimum",
    "CRITICAL: Achieve 100% coverage for critical file user_service.py",
    "HIGH: Investigate and fix coverage regression (-3.7%)",
    "Run 'analyze-test-coverage --show-gaps' for detailed gap analysis"
  ]
}
```

## Failure Handling

### Critical Check Failed
- **Action**: Immediately halt remaining checks if fail_fast=true
- **Output**: Detailed failure report with specific violations
- **Recommendation**: Provide actionable steps to resolve each blocking issue
- **Blocking**: CRITICAL - prevents merge/deploy
- **Recovery**: Fix issues and re-run quality gate, all checks must pass

### Multiple Checks Failed
- **Action**: Continue executing all checks to provide complete picture
- **Output**: Prioritized list of failures by severity
- **Recommendation**: Order fixes by dependency (e.g., fix tests before coverage)
- **Blocking**: CRITICAL - must resolve all failures
- **Recovery**: Address each failure systematically, re-run gate after fixes

### Coverage Regression
- **Action**: Compare current coverage with baseline commit
- **Output**: File-by-file coverage delta showing losses
- **Recommendation**: Identify commits that reduced coverage, restore or justify
- **Blocking**: HIGH severity for production, MEDIUM for staging
- **Recovery**: Add tests to restore coverage or update baseline with approval

### Security Vulnerabilities Found
- **Action**: List all vulnerabilities with CVE IDs and severity
- **Output**: Dependency tree showing vulnerable packages
- **Recommendation**: Upgrade dependencies or apply security patches
- **Blocking**: CRITICAL for HIGH/CRITICAL CVEs, MEDIUM for others
- **Recovery**: Update vulnerable dependencies, re-run security scan

### Performance Degradation
- **Action**: Compare current benchmarks with baseline
- **Output**: Response time delta per endpoint
- **Recommendation**: Profile slow endpoints, optimize queries/code
- **Blocking**: HIGH if p95 > 2x baseline, MEDIUM otherwise
- **Recovery**: Optimize performance, re-run benchmarks until within threshold

### Build Failure
- **Action**: Capture build logs and error messages
- **Output**: Compilation errors with file/line references
- **Recommendation**: Fix syntax/type errors, resolve dependencies
- **Blocking**: CRITICAL - cannot deploy broken build
- **Recovery**: Fix build errors, verify production build succeeds

### Environment Configuration Error
- **Action**: Validate all required environment variables and services
- **Output**: List of missing/invalid configuration
- **Recommendation**: Provide setup instructions for test environment
- **Blocking**: CRITICAL - cannot run tests without proper setup
- **Recovery**: Configure environment per `.env.test.example`, re-run gate

### Gate Profile Not Found
- **Action**: List available quality profiles
- **Output**: Profile names and their criteria
- **Recommendation**: Use default profile or create custom profile
- **Blocking**: CRITICAL - cannot proceed without criteria
- **Recovery**: Specify valid profile name or use default "phase-1-strict"

## Deterministic Behavior
- Checks always executed in same order (code quality → tests → security → performance → build)
- Quality profiles version-controlled in `.qa/profiles/` directory
- Baseline reference resolved to specific git commit SHA (not branch name)
- All timestamps in ISO 8601 UTC format
- Quality score calculation: (passed_checks / total_checks) * 100
- Exit codes: 0 (all passed), 1 (checks failed), 2 (setup error), 3 (profile invalid)
- Timeout per check: unit tests (60s), integration (120s), security (300s), performance (180s)
- Retry logic: network-dependent checks retry 3x with exponential backoff
- Report artifact always saved even on failure for post-mortem analysis
- CI/CD integration: exports QUALITY_GATE_STATUS, QUALITY_SCORE, BLOCKING_ISSUES_COUNT
