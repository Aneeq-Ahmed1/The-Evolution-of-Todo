# Data Model: Phase 1 and Phase 2 Separation

## Overview
This document defines the data models for both the Phase 1 console application and Phase 2 web application. Both applications use similar Task entities but with different persistence mechanisms.

## Phase 1 - Console App Data Model

### Task (src/todo/models.py)
- **id**: int (auto-generated unique identifier)
- **title**: str (1-200 characters, required)
- **description**: str (optional, up to 1000 characters)
- **completed**: bool (default: False)
- **created_at**: datetime (auto-generated timestamp)
- **updated_at**: datetime (auto-generated timestamp, updated on changes)

**Persistence**: In-memory storage with JSON export/import capability
- Tasks stored in memory during runtime
- Export to JSON file functionality
- Import from JSON file functionality
- No permanent database storage

## Phase 2 - Web App Data Model

### User (backend/models.py)
- **id**: UUID (auto-generated unique identifier)
- **email**: str (unique, required for authentication)
- **hashed_password**: str (encrypted password)
- **created_at**: datetime (auto-generated timestamp)
- **updated_at**: datetime (auto-generated timestamp, updated on changes)

### Task (backend/models.py)
- **id**: UUID (auto-generated unique identifier)
- **title**: str (1-200 characters, required)
- **description**: str (optional, up to 1000 characters)
- **completed**: bool (default: False)
- **user_id**: UUID (foreign key linking to User)
- **created_at**: datetime (auto-generated timestamp)
- **updated_at**: datetime (auto-generated timestamp, updated on changes)

**Persistence**: PostgreSQL database via Neon
- Persistent storage using SQLModel with SQLAlchemy
- Relationship between User and Task entities
- Foreign key constraint ensuring data integrity
- ACID compliance for transactional operations

## Data Relationships

### Phase 2 Only
- **User-Task Relationship**: One-to-Many
  - One User can have many Tasks
  - Each Task belongs to exactly one User
  - Cascade delete: When User is deleted, all associated Tasks are deleted

## Validation Rules

### Phase 1 Console App
- Task title: 1-200 characters
- Task description: max 1000 characters (optional)
- Task ID: auto-incrementing integer

### Phase 2 Web App
- User email: valid email format, unique across system
- Task title: 1-200 characters
- Task description: max 1000 characters (optional)
- Task user_id: must reference an existing User
- Password: minimum length and complexity requirements

## State Transitions

### Task State Transitions (Both Phases)
- **Created**: New task with completed=False
- **Updated**: Task details modified (title, description)
- **Completed**: completed=True when marked as done
- **Uncompleted**: completed=False when marked as pending
- **Deleted**: Task removed from system

### User State Transitions (Phase 2 Only)
- **Registered**: New user account created with hashed password
- **Authenticated**: User verified via JWT token
- **Deactivated**: User account disabled (soft delete)

## Data Access Patterns

### Phase 1 Console App
- In-memory operations for speed
- CRUD operations on Task entities
- JSON serialization for export/import
- No concurrent access concerns

### Phase 2 Web App
- Database operations through SQLModel/SQLAlchemy
- Concurrent access handling via database locks
- Transaction management for data consistency
- Connection pooling for performance
- JWT-based access control for user isolation