---
id: 001
title: ai-agent-platform-plan
stage: plan
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-agent-platform
branch: 1-ai-agent-platform
user: user
command: /sp.plan
labels: [ai,agent,platform,architecture,design]
links:
  spec: specs/1-ai-agent-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-agent-platform/plan.md
  - specs/1-ai-agent-platform/research.md
  - specs/1-ai-agent-platform/data-model.md
  - specs/1-ai-agent-platform/quickstart.md
  - specs/1-ai-agent-platform/contracts/openapi.yaml
  - .specify/memory/agent-context.md
tests:
  - null
---

## Prompt

```text
Planning Authority:
This plan derives directly from the approved constitution and specification.
No architectural decisions may violate those governing documents.

Planning Objective:
Design a scalable, provider-agnostic AI-native agent system that routes model communication through an OpenAI-compatible interface while initially using Google Gemini as the inference provider.

The plan prioritizes:
- Architectural clarity
- Low cognitive load
- Debuggability
- Token efficiency
- Long-term extensibility


--------------------------------

SYSTEM ARCHITECTURE (High-Level)

The system will follow a layered architecture:

Frontend → API Layer → Agent Layer → Skills Layer → Provider Adapter → Model

Each layer must remain independently replaceable.

No layer may leak responsibilities into another.


--------------------------------

ARCHITECTURAL LAYERS

1️⃣ Frontend Layer
Purpose:
Provide a clean chatbot interface for interacting with the agent system.

Responsibilities:
- Capture user messages
- Send requests to backend
- Render structured responses
- Display errors gracefully

Rules:
- ZERO business logic
- ZERO provider awareness
- ZERO agent logic

Recommended:
Next.js or lightweight web UI.


--------------------------------

2️⃣ API / Gateway Layer

Purpose:
Act as the single entry point into the backend.

Responsibilities:
- Validate requests
- Attach metadata
- Forward messages to the orchestrator
- Standardize responses

Recommended Stack:
FastAPI (preferred for AI systems)

Why:
- Async ready
- Lightweight
- Easy schema validation
- Production-friendly


--------------------------------

3️⃣ Orchestrator Agent (CORE BRAIN)

⚠️ This is the most important component in the entire system.

Purpose:
Control decision flow across agents and skills.

Responsibilities:
- Interpret user intent
- Select appropriate agent
- Trigger required skills
- Enforce execution order

Flow MUST be:

User → Orchestrator → Agent → Skill → Provider → Response

Rules:
- No direct provider calls
- No embedded skill logic
- No shortcuts


--------------------------------

4️⃣ Agent Layer

Start SIMPLE.

Do NOT create multiple agents prematurely.

Phase Strategy:

Phase Start:
✅ Primary Conversational Agent

Later Expansion:
- Task Agent
- Support Agent
- Tool Agent

Agent Responsibilities:
- Reason
- Decide which skill to call
- Structure the response

Agents must remain thin.

Heavy logic belongs inside skills.


--------------------------------

5️⃣ Skills Layer (Your MCP Equivalent)

Think of skills as **deterministic capabilities**, not mini-agents.

Examples:

Core Skills:
- Intent Classification Skill
- Response Generation Skill
- Memory Skill (optional early phase)
- Error Handling Skill

Design Rules:
- Skills must be reusable
- Skills must be testable
- Skills must NOT depend on UI
- Skills must NOT call the frontend


--------------------------------

6️⃣ Provider Adapter Layer (VERY IMPORTANT)

This layer is what makes your system **future-proof**.

Purpose:
Translate OpenAI-style requests into Gemini format.

Architecture Pattern:
👉 Adapter Pattern

Create something like:

provider/
    base_provider.py
    gemini_adapter.py
    openai_adapter.py (future)

Rules:
- Agents NEVER talk directly to Gemini.
- Only the adapter can.

This prevents vendor lock-in.


--------------------------------

7️⃣ Configuration Layer

Use `.env` for ALL secrets.

Example variables:

OPENAI_BASE_URL=
OPENAI_API_KEY=
GEMINI_API_KEY=
MODEL_NAME=

Hardcoding keys = architecture violation.


--------------------------------

FOLDER STRUCTURE (Recommended)

Keep it extremely clean:

backend/
api/
agents/
skills/
provider/
orchestrator/
config/

frontend/

.env


Avoid deep nesting.
Complex folders kill velocity.


--------------------------------

EXECUTION FLOW

STRICT FLOW — DO NOT BREAK:

1️⃣ User sends message  
2️⃣ API receives request  
3️⃣ Orchestrator evaluates intent  
4️⃣ Agent selected  
5️⃣ Agent invokes skill  
6️⃣ Skill calls provider adapter  
7️⃣ Model responds  
8️⃣ Structured response returned  


--------------------------------

ERROR STRATEGY

Fail CLEARLY.
Never fail silently.

Required:

- Config errors → startup failure  
- Provider errors → readable message  
- Timeout → retry-safe response  


--------------------------------

OBSERVABILITY (Most beginners ignore this)

Minimum required:

- Request logging  
- Provider call logging  
- Error logging  

Do NOT over-engineer telemetry yet.


--------------------------------

SCALING STRATEGY (Future Safe)

Your design must allow:

✅ swapping Gemini → OpenAI  
✅ adding tools  
✅ multi-agent expansion  
✅ memory integration  
✅ MCP servers  

WITHOUT rewriting the core.


--------------------------------

ANTI-PATTERNS (DO NOT DO)

❌ Fat agents  
❌ Direct model calls  
❌ Hidden prompts everywhere  
❌ Hardcoded responses  
❌ Mixing UI with reasoning  
❌ Deep abstractions too early  


--------------------------------

SUCCESS CONDITIONS

This plan is successful when:

✅ The system runs through ONE orchestrator  
✅ Provider can be swapped with minimal change  
✅ Skills remain modular  
✅ Architecture is understandable in under 10 minutes  
✅ Claude Code can implement without guessing
```

## Response snapshot

# Implementation Plan: AI-Native Agent Platform with Provider-Agnostic Interface

**Branch**: `1-ai-agent-platform` | **Date**: 2026-02-02 | **Spec**: [specs/1-ai-agent-platform/spec.md](specs/1-ai-agent-platform/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a scalable, provider-agnostic AI-native agent system that routes model communication through an OpenAI-compatible interface while initially using Google Gemini as the inference provider. The system will follow a layered architecture with clear separation of concerns: Frontend → API Layer → Agent Layer → Skills Layer → Provider Adapter → Model. The architecture prioritizes architectural clarity, low cognitive load, debuggability, token efficiency, and long-term extensibility.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend
**Primary Dependencies**: FastAPI (backend), Next.js (frontend), OpenAI SDK, Google Generative AI SDK, MCP SDK
**Storage**: PostgreSQL (via existing SQLModel setup from previous phases)
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web-based application (Linux/Mac/Windows server)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 second response times for typical queries, token-efficient communication
**Constraints**: Provider-agnostic design, stateless operation, security-first configuration
**Scale/Scope**: Individual/Team usage (up to 1000 concurrent users)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **AI-Native Design**: ✓ Confirmed - System designed around agents and skills, not hardcoded logic
2. **Spec-Driven Development**: ✓ Confirmed - Following Spec → Plan → Tasks → Implement flow
3. **Deterministic Orchestration**: ✓ Confirmed - All requests routed through central Orchestrator Agent
4. **Single Source of Truth**: ✓ Confirmed - Backend APIs and database remain authoritative for task data
5. **Statelessness**: ✓ Confirmed - Backend and MCP tools will not hold in-memory state between requests
6. **Reusability and Traceability**: ✓ Confirmed - Agents and skills designed to be reusable with logging

All constitution requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-agent-platform/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── conversation.py         # Conversation entities
│   ├── services/
│   │   ├── agent_orchestrator.py   # Main orchestrator logic
│   │   ├── conversation_service.py # Conversation persistence
│   │   └── provider_adapter.py     # Provider abstraction layer
│   ├── api/
│   │   ├── chat_api.py            # Main chat endpoint
│   │   └── mcp_server.py          # MCP tool server
│   ├── agents/
│   │   ├── base_agent.py          # Base agent class
│   │   ├── orchestrator_agent.py  # Main orchestrator
│   │   ├── chat_agent.py          # Conversational agent
│   │   └── task_agent.py          # Task-specific agent
│   └── skills/
│       ├── base_skill.py          # Base skill class
│       ├── intent_analysis.py     # Intent classification
│       ├── task_management.py     # Task operations
│       ├── context_memory.py      # Conversation state
│       ├── response_formatting.py # Response formatting
│       └── error_handling.py      # Error handling
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface/         # Main chat UI component
│   ├── pages/
│   │   └── chat.jsx              # Chat page
│   └── services/
│       └── api.js                # API client
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Web application structure selected with separate backend and frontend directories to maintain clear separation of concerns between AI logic and user interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations found] | [Constitution requirements satisfied] |

## Research Findings: AI-Native Agent Platform

### Decision: Provider Adapter Layer Implementation
**Rationale**: To achieve provider-agnostic design, we need a translation layer that converts OpenAI-compatible requests to provider-specific formats. Google Gemini was selected as the initial provider due to its strong capabilities and availability of SDKs.

**Alternatives considered**:
- Direct OpenAI API calls: Would create vendor lock-in
- Multiple direct provider integrations: Would create complex branching logic
- Third-party abstraction libraries: Limited flexibility and potential maintenance issues

### Decision: Agent Architecture Pattern
**Rationale**: The orchestrator-first pattern ensures all user requests go through a central decision-maker, enabling consistent intent analysis and proper routing to specialized agents.

**Alternatives considered**:
- Direct routing to agents: Would bypass intent analysis and create inconsistent experiences
- Multiple entry points: Would complicate the architecture and violate the single-entry-point principle
- Rule-based routing: Would lack the flexibility of AI-driven routing

### Decision: MCP Tool Integration
**Rationale**: Using the Model Context Protocol (MCP) tools provides a standardized way to expose backend capabilities to AI agents, maintaining clear separation between AI logic and business logic.

**Alternatives considered**:
- Custom function calling: Would create proprietary integration patterns
- Direct API calls from agents: Would violate the skills layer separation
- Hardcoded capabilities: Would reduce flexibility and reusability

### Decision: Frontend Technology
**Rationale**: Next.js provides the best balance of server-side rendering capabilities, developer experience, and integration possibilities with AI chat interfaces.

**Alternatives considered**:
- Vanilla JavaScript: Would require more boilerplate and lack framework benefits
- React with Create React App: Would miss Next.js optimizations for production
- Alternative frameworks (Vue, Angular): Would add unnecessary complexity for this use case

### Decision: Backend Framework
**Rationale**: FastAPI offers excellent async support, automatic API documentation, and strong typing capabilities that align well with AI system requirements.

**Alternatives considered**:
- Flask: Would lack async support and modern features
- Django: Would be overly complex for this use case
- Node.js/Express: Would not leverage Python's strong AI/ML ecosystem

## Data Model: AI-Native Agent Platform

### Core Entities

#### Conversation
**Description**: Represents a single conversation thread between user and agent

**Fields**:
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to user)
- `title`: String (conversation title, auto-generated)
- `created_at`: DateTime (timestamp)
- `updated_at`: DateTime (last activity timestamp)
- `metadata`: JSON (conversation properties, tags, etc.)

**Relationships**:
- One-to-many with Message
- Belongs to User

#### Message
**Description**: Represents a single message in a conversation

**Fields**:
- `id`: UUID (primary key)
- `conversation_id`: UUID (foreign key to conversation)
- `role`: Enum ('user', 'assistant', 'system', 'tool')
- `content`: Text (message content)
- `timestamp`: DateTime
- `tool_calls`: JSON (if role is 'assistant' and tools were called)
- `tool_response`: JSON (if role is 'tool' and contains tool result)

**Relationships**:
- Belongs to Conversation
- Belongs to User (via conversation)

#### AgentSession
**Description**: Tracks active agent sessions for state management

**Fields**:
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to user)
- `current_agent`: String (currently active agent type)
- `context_state`: JSON (serialized context for continuity)
- `created_at`: DateTime
- `expires_at`: DateTime

**Relationships**:
- Belongs to User

#### SkillExecutionLog
**Description**: Logs all skill executions for debugging and analytics

**Fields**:
- `id`: UUID (primary key)
- `conversation_id`: UUID (foreign key to conversation)
- `skill_name`: String (name of executed skill)
- `input_params`: JSON (parameters passed to skill)
- `output_result`: JSON (result returned by skill)
- `execution_time`: Float (time taken in seconds)
- `timestamp`: DateTime

**Relationships**:
- Belongs to Conversation

### State Transitions

#### Conversation States
- `ACTIVE`: New messages can be added
- `PAUSED`: Temporarily inactive (user requested pause)
- `COMPLETED`: Final state, no further changes allowed
- `ARCHIVED`: Long-term storage, read-only access

#### Message States
- `PENDING`: Sent but not yet processed
- `PROCESSING`: Currently being handled
- `PROCESSED`: Successfully handled
- `FAILED`: Processing failed, retry may be possible

### Validation Rules

#### Conversation Validation
- Must have a valid user_id
- Title cannot exceed 200 characters
- Cannot have more than 10,000 messages
- Must be associated with an active user

#### Message Validation
- Role must be one of the allowed enum values
- Content cannot be empty (except for tool responses)
- Must belong to an active conversation
- Timestamp must be current or past (not future)

#### AgentSession Validation
- Cannot have overlapping sessions for the same user
- Expiration time must be in the future
- Current agent must be a valid registered agent type
- Context state size limited to 1MB

### Indexes

#### Conversation Table
- Index on `user_id` for fast user lookup
- Index on `created_at` for chronological ordering
- Composite index on `(user_id, created_at)` for efficient pagination

#### Message Table
- Index on `conversation_id` for conversation retrieval
- Index on `timestamp` for chronological ordering
- Composite index on `(conversation_id, timestamp)` for conversation history

#### AgentSession Table
- Index on `user_id` for session lookup
- Index on `expires_at` for cleanup jobs
- Unique constraint on `user_id` to prevent multiple active sessions

## Quickstart Guide: AI-Native Agent Platform

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL 12+ (or compatible database)
- API keys for your chosen LLM provider (Google Gemini, OpenAI, etc.)

### Setup Instructions

#### 1. Clone and Initialize the Repository

```bash
git clone <repository-url>
cd <repository-directory>
cd phase_3_Aichatbot
```

#### 2. Backend Setup

##### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

##### Configure Environment Variables
Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-super-secret-key-here

# LLM Provider Configuration
LLM_PROVIDER=gemini  # or 'openai', 'anthropic', etc.
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key  # if using OpenAI
ANTHROPIC_API_KEY=your-anthropic-api-key  # if using Anthropic

# Application Configuration
DEBUG=false
LOG_LEVEL=info
```

##### Initialize Database
```bash
# Run database migrations
python -m alembic upgrade head

# Or if using SQLModel directly
python -c "from src.db.init_db import init_db; init_db()"
```

##### Start Backend Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

#### 3. Frontend Setup

##### Install Node Dependencies
```bash
cd frontend
npm install
```

##### Configure Environment Variables
Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENABLED=true
```

##### Start Frontend Server
```bash
npm run dev
```

### API Endpoints

#### Chat API
- `POST /api/chat` - Main chat endpoint for interacting with the agent
- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `POST /api/conversations` - Create new conversation

#### MCP Server (if implemented separately)
- `POST /mcp/tools/invoke` - Invoke MCP tools
- `GET /mcp/tools/list` - List available tools

### Usage Examples

#### Interacting with the Agent
Send a message to the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <user-token>" \
  -d '{
    "message": "Hello, can you help me create a todo?",
    "conversation_id": "optional-existing-conversation-id"
  }'
```

#### Switching LLM Providers
To switch between providers, update the `LLM_PROVIDER` environment variable:
- `gemini` - Google Gemini
- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models

### Development Commands

#### Running Tests
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

#### Code Quality Checks
```bash
# Backend linting
cd backend
flake8 src/
black --check src/

# Frontend linting
cd frontend
npm run lint
```

### Troubleshooting

#### Common Issues

1. **API Key Not Found**
   - Ensure your `.env` file contains the correct API keys
   - Verify the `LLM_PROVIDER` environment variable matches your provider

2. **Database Connection Issues**
   - Check that PostgreSQL is running
   - Verify your `DATABASE_URL` is correctly formatted
   - Ensure the database exists and user has appropriate permissions

3. **CORS Issues**
   - Check that your frontend URL is included in the backend CORS settings
   - Verify the `ALLOWED_ORIGINS` environment variable

4. **Provider-Specific Issues**
   - Some providers may have rate limits - check your provider's dashboard
   - Verify that your account has sufficient quota for the operations you're performing

#### Checking System Status
```bash
# Health check endpoint
curl http://localhost:8000/health

# Provider connectivity check
curl http://localhost:8000/api/health/provider
```

### Environment Variables Reference

#### Backend Environment Variables
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `LLM_PROVIDER` - Active LLM provider ('gemini', 'openai', 'anthropic')
- `GEMINI_API_KEY` - Google Gemini API key
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `DEBUG` - Enable debug mode (true/false)
- `LOG_LEVEL` - Logging level (debug, info, warning, error)
- `MAX_TOKENS` - Maximum tokens for responses
- `TEMPERATURE` - Temperature setting for LLM responses
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins

#### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for backend API
- `NEXT_PUBLIC_CHAT_ENABLED` - Enable/disable chat interface (true/false)
- `NEXT_PUBLIC_DEBUG_MODE` - Enable debug features (true/false)

### Provider Configuration Details

#### Google Gemini
- Requires `GEMINI_API_KEY` in environment
- Supports Gemini Pro and Gemini Flash models
- Automatic model selection based on query complexity

#### OpenAI
- Requires `OPENAI_API_KEY` in environment
- Supports GPT-3.5 Turbo and GPT-4 models
- Function calling capabilities for tool integration

#### Anthropic
- Requires `ANTHROPIC_API_KEY` in environment
- Supports Claude 2 and Claude 3 models
- Strong performance on complex reasoning tasks

## Architectural Decision Detected

📋 Architectural decision detected: Layered architecture with provider-agnostic design — Document reasoning and tradeoffs? Run `/sp.adr layered-architecture-decision`

## Outcome

- ✅ Impact: Created complete implementation plan with research, data models, quickstart guide, API contracts, and agent context for the AI agent platform
- 🧪 Tests: No tests created in planning phase
- 📁 Files: Created 6 files (plan.md, research.md, data-model.md, quickstart.md, openapi.yaml, agent-context.md)
- 🔁 Next prompts: Implementation tasks will be generated using /sp.tasks
- 🧠 Reflection: The layered architecture ensures provider-agnostic design while maintaining clear separation of concerns between frontend, API, agents, skills, and providers.

## Evaluation notes (flywheel)

- Failure modes observed: None identified in planning phase
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate implementation tasks with /sp.tasks