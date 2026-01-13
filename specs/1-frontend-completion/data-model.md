# Data Model: Frontend Completion (Next.js)

## Entity: Todo Item
**Description**: Represents a single todo with properties like title, completion status, and creation date. Provides the core data model for the application.

**Fields**:
- `id`: string | unique identifier for the todo item
- `title`: string | the text content of the todo
- `completed`: boolean | completion status (true if completed, false if pending)
- `createdAt`: Date | timestamp when the todo was created
- `updatedAt`: Date | timestamp when the todo was last modified (optional)

**Validation Rules**:
- `title` must not be empty or whitespace only
- `id` must be unique within the user's todo list
- `completed` defaults to false when creating new items

**State Transitions**:
- Pending → Completed: When user marks the todo as complete
- Completed → Pending: When user unmarks the todo as complete

## Entity: Todo List
**Description**: Collection of todo items with operations for adding, completing, and deleting items. Manages the state and presentation of multiple todo items.

**Fields**:
- `items`: TodoItem[] | array of todo items
- `filter`: string | current filter state (all, active, completed)
- `isLoading`: boolean | loading state indicator
- `error`: string | error message if any issues occur

**Operations**:
- `add(item: TodoItem)`: void | adds a new todo to the list
- `remove(id: string)`: void | removes a todo by ID
- `update(id: string, updates: Partial<TodoItem>)`: void | updates todo properties
- `toggleComplete(id: string)`: void | toggles completion status

## Entity: UI State
**Description**: Represents different application states including loading, error, and empty states. Controls the visual presentation based on application status.

**Fields**:
- `isLoading`: boolean | indicates if data is being loaded
- `error`: string | error message for error state
- `isEmpty`: boolean | indicates if todo list is empty
- `isAuthenticated`: boolean | authentication state (for future auth integration)

**State Transitions**:
- Idle → Loading: When API call is initiated
- Loading → Success: When API call completes successfully
- Loading → Error: When API call fails
- Any state → Empty: When todo list becomes empty

## Entity: Authentication Credentials (for Login/Signup)
**Description**: Represents user credentials for authentication flows.

**Fields**:
- `email`: string | user's email address
- `password`: string | user's password
- `name`: string | user's full name (for signup only)

**Validation Rules**:
- `email` must be a valid email format
- `password` must meet minimum length requirements (8 characters)
- `name` must not be empty for signup

## Entity: Form State
**Description**: Represents the state of various forms in the application.

**Fields**:
- `isSubmitting`: boolean | indicates if form is being submitted
- `errors`: Record<string, string> | field-specific error messages
- `success`: boolean | indicates successful form submission