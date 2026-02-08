# Data Model: Todo AI Chatbot – Phase III (Basic Level)

## Entity: Task
**Fields:**
- id: Integer (Primary Key, Auto-increment)
- user_id: String (Foreign Key reference to user)
- title: String (Required, max 255 characters)
- description: Text (Optional, unlimited length)
- completed: Boolean (Default: false)
- created_at: Timestamp (Default: current timestamp)
- updated_at: Timestamp (Default: current timestamp, updates on modification)

**Validation Rules:**
- title is required and must be 1-255 characters
- user_id must exist and match authenticated user
- completed defaults to false
- timestamps automatically managed

**Relationships:**
- Belongs to one User (via user_id)

## Entity: Conversation
**Fields:**
- id: Integer (Primary Key, Auto-increment)
- user_id: String (Foreign Key reference to user)
- created_at: Timestamp (Default: current timestamp)
- updated_at: Timestamp (Default: current timestamp, updates on modification)

**Validation Rules:**
- user_id must exist and match authenticated user
- timestamps automatically managed

**Relationships:**
- Belongs to one User (via user_id)
- Has many Messages

## Entity: Message
**Fields:**
- id: Integer (Primary Key, Auto-increment)
- user_id: String (Foreign Key reference to user)
- conversation_id: Integer (Foreign Key reference to conversation)
- role: String (Required, values: "user" or "assistant")
- content: Text (Required, unlimited length)
- created_at: Timestamp (Default: current timestamp)

**Validation Rules:**
- user_id must exist and match authenticated user
- conversation_id must exist and belong to user
- role must be either "user" or "assistant"
- content is required
- timestamps automatically managed

**Relationships:**
- Belongs to one User (via user_id)
- Belongs to one Conversation (via conversation_id)

## State Transitions

### Task State Transitions
- Initial: completed = false
- Transition: completed = true (via complete_task operation)
- No reverse transition (completed tasks remain completed)

### Conversation State Transitions
- Initial: created when first message is sent
- Transition: updated_at changes when new messages are added
- No explicit end state (conversations persist indefinitely)

## Data Integrity Constraints
- All entities require valid user_id matching authenticated user
- Foreign key constraints between Conversation and Message
- Timestamps automatically managed by database
- No cascading deletes (preserve conversation history)