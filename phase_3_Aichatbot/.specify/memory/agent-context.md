# Phase 3 — Todo AI Chatbot Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-02

## Active Technologies

Python 3.11, TypeScript/JavaScript, FastAPI, Next.js, OpenAI SDK, Google Generative AI SDK, MCP SDK, PostgreSQL, SQLModel, pytest, Jest

## Project Structure

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

## Commands

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Run backend
uvicorn src.api.main:app --reload --port 8000

# Run frontend
npm run dev

# Run backend tests
cd backend
pytest tests/

# Run frontend tests
cd frontend
npm run test

## Code Style

# Python
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Prefer async/await for I/O operations
- Use FastAPI dependency injection for shared resources

# JavaScript/TypeScript
- Use functional components with hooks in React
- Follow Airbnb JavaScript style guide
- Use TypeScript for type safety where possible
- Implement proper error boundaries

## Recent Changes

Feature 1-ai-agent-platform: Added AI-native agent architecture with orchestrator pattern, provider-agnostic interface supporting multiple LLMs (initially Google Gemini), layered architecture with clear separation of concerns (Frontend → API → Agent → Skills → Provider), MCP tool integration for task operations, conversation persistence layer, and Next.js chat interface.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->