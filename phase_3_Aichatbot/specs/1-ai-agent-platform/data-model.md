# Data Model: AI-Native Agent Platform

## Core Entities

### Conversation
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

### Message
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

### AgentSession
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

### SkillExecutionLog
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

## State Transitions

### Conversation States
- `ACTIVE`: New messages can be added
- `PAUSED`: Temporarily inactive (user requested pause)
- `COMPLETED`: Final state, no further changes allowed
- `ARCHIVED`: Long-term storage, read-only access

### Message States
- `PENDING`: Sent but not yet processed
- `PROCESSING`: Currently being handled
- `PROCESSED`: Successfully handled
- `FAILED`: Processing failed, retry may be possible

## Validation Rules

### Conversation Validation
- Must have a valid user_id
- Title cannot exceed 200 characters
- Cannot have more than 10,000 messages
- Must be associated with an active user

### Message Validation
- Role must be one of the allowed enum values
- Content cannot be empty (except for tool responses)
- Must belong to an active conversation
- Timestamp must be current or past (not future)

### AgentSession Validation
- Cannot have overlapping sessions for the same user
- Expiration time must be in the future
- Current agent must be a valid registered agent type
- Context state size limited to 1MB

## Indexes

### Conversation Table
- Index on `user_id` for fast user lookup
- Index on `created_at` for chronological ordering
- Composite index on `(user_id, created_at)` for efficient pagination

### Message Table
- Index on `conversation_id` for conversation retrieval
- Index on `timestamp` for chronological ordering
- Composite index on `(conversation_id, timestamp)` for conversation history

### AgentSession Table
- Index on `user_id` for session lookup
- Index on `expires_at` for cleanup jobs
- Unique constraint on `user_id` to prevent multiple active sessions