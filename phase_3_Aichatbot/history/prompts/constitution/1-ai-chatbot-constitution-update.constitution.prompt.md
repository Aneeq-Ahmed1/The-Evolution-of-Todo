---
id: 1
title: "AI Chatbot Constitution Update"
stage: "constitution"
date_iso: "2026-01-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "ai-chatbot", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# AI Chatbot Constitution Update

## Prompt Text

```
Project: Phase 3 — Todo AI Chatbot (AI-Native, Agent & MCP Driven System)

Purpose:
Evolve the existing Phase 2 Todo full-stack application into an AI-native chatbot system that manages tasks through natural language using agents, skills, and MCP tools, without breaking existing architecture.

Core Principles:
- AI-Native Design: The system must be designed around agents and skills, not hardcoded logic.
- Spec-Driven Development: All work must follow the flow Spec → Plan → Tasks → Implement.
- Deterministic Orchestration: All user requests must be routed through a central Orchestrator Agent.
- Single Source of Truth: Backend APIs and database remain authoritative for all task data.
- Statelessness: Backend and MCP tools must not hold in-memory state between requests.
- Reusability: Agents and skills must be reusable in future phases with minimal refactoring.
- Traceability: Every AI decision must be observable via logs and structured metadata.
- Reliability: Errors must be handled gracefully with predictable responses.

Key Standards:
- All user messages must first be processed by the Orchestrator Agent.
- The Orchestrator must determine user intent before selecting any agent.
- No agent may execute logic directly; all actions must invoke an approved skill.
- MCP tools must be the only interface between AI agents and task operations.
- MCP tools must be stateless and persist data exclusively via the database.
- All agent interactions must follow this flow:
  User → Orchestrator Agent → Specialized Agent → Skill → MCP Tool → Response
- Conversation context must be persisted in the database and reconstructed per request.
- Frontend must never contain business logic; it only displays responses.

Mandatory Agents:
- Orchestrator Agent: Central router and intent coordinator.
- Chat Agent: Handles general conversational responses.
- Task/Todo Agent: Handles task-related intents (CRUD).
- Support Agent: Handles explanations, debugging, and system guidance.

Mandatory Skills:
- Intent Analysis Skill: Classifies user intent.
- Task Management Skill: Maps intents to MCP task tools.
- Context Memory Skill: Rebuilds conversation state from database.
- Response Formatting Skill: Produces clean, structured responses.
- Error Handling Skill: Standardized error and fallback responses.

MCP Tooling Rules:
- MCP server must be implemented using the Official MCP SDK.
- MCP tools must include:
  add_task, list_tasks, update_task, complete_task, delete_task
- MCP tools must not contain AI logic.
- All tool inputs and outputs must be explicit and schema-defined.

Constraints:
- No manual coding outside Claude Code generated output.
- No changes to Phase 1 or Phase 2 architecture unless strictly required.
- No direct database access from frontend.
- No hardcoded AI responses in agents.
- No committing build artifacts (node_modules, .next, dist, etc.).
- Git commits must clearly describe intent and scope.

Success Criteria:
- Fully functional AI chatbot integrated with existing frontend and backend.
- Correct agent routing and skill invocation for all user queries.
- MCP tools correctly manage tasks via the database.
- Stateless chat behavior with persistent conversation history.
- System is ready for Phase 4 without major refactoring.

Evaluation Focus:
- Correct use of Spec-Driven Development.
- Clean separation of agents, skills, and MCP tools.
- Deterministic orchestration and stateless design.
- Clarity, stability, and extensibility of the architecture.
```

## Response Text

Updated the project constitution at `.specify/memory/constitution.md` to reflect the Phase 3 Todo AI Chatbot requirements. The new constitution includes:

- Six core principles: AI-Native Design, Spec-Driven Development, Deterministic Orchestration, Single Source of Truth, Statelessness, and Reusability and Traceability
- Additional constraints for architecture requirements, agent and skill standards, and mandatory components
- Development workflow requirements for agent flow, mandatory agents, and mandatory skills
- Governance section outlining compliance and amendment procedures

The constitution now properly governs the AI-native system with its agent-based architecture, MCP tools, and stateless design requirements.