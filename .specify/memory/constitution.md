
<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Modified principles: N/A (new constitution)
- Added sections: All sections (new constitution)
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending review
- Follow-up TODOs: None
-->

# AI-Powered Todo Chatbot Constitution

## Core Principles

### Scalability
Stateless backend architecture with horizontal scaling support; All services must be designed for auto-scaling; Load balancing and distributed processing capabilities required.

### Reliability
Fault-tolerant systems with graceful error handling; Circuit breakers and retry mechanisms implemented; Service health monitoring and automatic failover required.

### Modularity
Clear separation of concerns between frontend, backend, MCP, database, Kafka, and Dapr components; Each service must have well-defined interfaces and minimal coupling; Independent deployment capabilities for each module.

### Reproducibility
All deployments must be documented and containerized; Infrastructure as Code (IaC) approach required; Complete deployment pipelines with consistent environments across local, staging, and production.

### Security
Secrets management with secure storage and access; Authentication and authorization enforced at all service boundaries; Domain allowlist for all external communications; Data encryption at rest and in transit.

### Spec-Driven Development
No coding without approved specification, plan, and tasks; All features must follow the specify → plan → tasks workflow; Requirements traceability from specification to implementation.

## Standards and Constraints

Technology stack: OpenAI ChatKit for frontend, FastAPI with Python for backend, MCP SDK for integration, SQLModel with Neon Postgres for database, Dapr for service communication, Kafka for event streaming, Helm and Kubernetes for deployment.

Version Control: Git with structured branch strategy (feature branches, main/master protection rules, pull request reviews required); All commits must reference relevant tasks and specifications.

Documentation: Inline Task-ID references in code; Comprehensive README files; Specification documents in specs/ folder; Architecture Decision Records for significant choices.

Testing: Unit testing for all components; Integration testing for service interactions; Test coverage metrics maintained; Automated testing in CI/CD pipeline.

CI/CD: Automated deployment pipeline using GitHub Actions; Build, test, and deployment stages; Automated security scanning; Quality gates before production deployment.

## Development Workflow

Phased Implementation: Follow Phase I-V development approach; Each phase must be completed before advancing to the next; Regular milestone reviews and approvals required.

Stateless Architecture: Backend services must maintain no persistent state; All data persistence handled through database layer; Session management via external stores.

Event-Driven Architecture: Services communicate via Kafka and Dapr; Asynchronous processing for non-critical operations; Event sourcing patterns where appropriate; Message durability and ordering guarantees.

Deployment Strategy: Local deployment via Minikube for development; Cloud deployment via AKS/GKE/Redpanda for production; Consistent deployment patterns across environments.

Performance Requirements: Max frontend latency of 200ms; Response time SLA definitions; Resource utilization monitoring; Performance testing as part of CI/CD.

## Governance

This constitution supersedes all other development practices and guidelines; All development activities must comply with these principles; Amendments require formal documentation, team approval, and migration planning.

All pull requests and code reviews must verify constitution compliance; Architectural decisions must align with stated principles; Complexity must be justified against these core principles; Use this constitution as the primary guidance for development decisions.

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25
=======
# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### [PRINCIPLE_6_NAME]


[PRINCIPLE__DESCRIPTION]

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
ab5ed3a (Initial commit from Specify template)
