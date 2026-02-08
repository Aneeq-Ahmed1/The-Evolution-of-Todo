# Quickstart Guide: AI-Native Agent Platform

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL 12+ (or compatible database)
- API keys for your chosen LLM provider (Google Gemini, OpenAI, etc.)

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
git clone <repository-url>
cd <repository-directory>
cd phase_3_Aichatbot
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment Variables
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

#### Initialize Database
```bash
# Run database migrations
python -m alembic upgrade head

# Or if using SQLModel directly
python -c "from src.db.init_db import init_db; init_db()"
```

#### Start Backend Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment Variables
Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENABLED=true
```

#### Start Frontend Server
```bash
npm run dev
```

## API Endpoints

### Chat API
- `POST /api/chat` - Main chat endpoint for interacting with the agent
- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `POST /api/conversations` - Create new conversation

### MCP Server (if implemented separately)
- `POST /mcp/tools/invoke` - Invoke MCP tools
- `GET /mcp/tools/list` - List available tools

## Usage Examples

### Interacting with the Agent
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

### Switching LLM Providers
To switch between providers, update the `LLM_PROVIDER` environment variable:
- `gemini` - Google Gemini
- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models

## Development Commands

### Running Tests
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

### Code Quality Checks
```bash
# Backend linting
cd backend
flake8 src/
black --check src/

# Frontend linting
cd frontend
npm run lint
```

## Troubleshooting

### Common Issues

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

### Checking System Status
```bash
# Health check endpoint
curl http://localhost:8000/health

# Provider connectivity check
curl http://localhost:8000/api/health/provider
```

## Environment Variables Reference

### Backend Environment Variables
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

### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for backend API
- `NEXT_PUBLIC_CHAT_ENABLED` - Enable/disable chat interface (true/false)
- `NEXT_PUBLIC_DEBUG_MODE` - Enable debug features (true/false)

## Provider Configuration Details

### Google Gemini
- Requires `GEMINI_API_KEY` in environment
- Supports Gemini Pro and Gemini Flash models
- Automatic model selection based on query complexity

### OpenAI
- Requires `OPENAI_API_KEY` in environment
- Supports GPT-3.5 Turbo and GPT-4 models
- Function calling capabilities for tool integration

### Anthropic
- Requires `ANTHROPIC_API_KEY` in environment
- Supports Claude 2 and Claude 3 models
- Strong performance on complex reasoning tasks