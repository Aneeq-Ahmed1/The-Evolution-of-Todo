# API Contracts: Frontend Completion (Next.js)

## Todo Service API Contracts

### Todo Entity
```
{
  "id": "string",
  "title": "string",
  "completed": "boolean",
  "createdAt": "ISO 8601 date string",
  "updatedAt": "ISO 8601 date string (optional)"
}
```

### Endpoints

#### GET /api/todos
**Description**: Retrieve all todos for the current user
**Authentication**: Not required (mock implementation)
**Response**:
- Success: 200 OK
  ```
  {
    "data": [Todo],
    "count": "number"
  }
  ```
- Error: 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```

#### POST /api/todos
**Description**: Create a new todo
**Authentication**: Not required (mock implementation)
**Request Body**:
```
{
  "title": "string (required)"
}
```
**Response**:
- Success: 201 Created
  ```
  {
    "data": Todo
  }
  ```
- Error: 400 Bad Request (validation error) or 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```

#### PUT /api/todos/{id}
**Description**: Update a todo
**Authentication**: Not required (mock implementation)
**Request Body**:
```
{
  "title": "string (optional)",
  "completed": "boolean (optional)"
}
```
**Response**:
- Success: 200 OK
  ```
  {
    "data": Todo
  }
  ```
- Error: 404 Not Found or 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```

#### DELETE /api/todos/{id}
**Description**: Delete a todo
**Authentication**: Not required (mock implementation)
**Response**:
- Success: 204 No Content
- Error: 404 Not Found or 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```

## Authentication Service API Contracts

### User Entity
```
{
  "id": "string",
  "email": "string",
  "name": "string",
  "createdAt": "ISO 8601 date string"
}
```

### Endpoints

#### POST /api/auth/login
**Description**: Authenticate user and return session
**Request Body**:
```
{
  "email": "string",
  "password": "string"
}
```
**Response**:
- Success: 200 OK
  ```
  {
    "data": {
      "user": User,
      "token": "string"
    }
  }
  ```
- Error: 401 Unauthorized or 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```

#### POST /api/auth/signup
**Description**: Create new user account
**Request Body**:
```
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```
**Response**:
- Success: 201 Created
  ```
  {
    "data": {
      "user": User,
      "token": "string"
    }
  }
  ```
- Error: 400 Bad Request (validation) or 409 Conflict (email exists) or 500 Internal Server Error
  ```
  {
    "error": "string",
    "message": "string"
  }
  ```