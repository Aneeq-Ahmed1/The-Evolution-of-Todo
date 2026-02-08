# Frontend Skill: Create Component

## Skill Name
`create-component`

## Description
Generate a new React component with TypeScript, proper structure, and Tailwind CSS styling.

## Usage
```
/frontend:create-component <ComponentName> [--client] [--with-state] [--with-props]
```

## Examples

```bash
# Create simple component
/frontend:create-component Button

# Create client component with state
/frontend:create-component TaskCard --client --with-state

# Create component with props interface
/frontend:create-component UserProfile --with-props
```

## Parameters

- `<ComponentName>`: PascalCase component name
- `--client`: Add 'use client' directive
- `--with-state`: Include useState example
- `--with-props`: Generate props interface

## What It Generates

### Basic Component
```typescript
// src/components/Button.tsx
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

export default function Button({ onClick, children, variant = 'primary' }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded ${
        variant === 'primary'
          ? 'bg-indigo-600 text-white hover:bg-indigo-700'
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }`}
    >
      {children}
    </button>
  );
}
```

### Client Component with State
```typescript
'use client';

import { useState } from 'react';

interface TaskCardProps {
  task: Task;
  onUpdate: (task: Task) => void;
}

export default function TaskCard({ task, onUpdate }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="bg-white shadow rounded-lg p-4">
      {/* Component content */}
    </div>
  );
}
```

## Generated Structure

```
frontend/src/components/
└── ComponentName.tsx           # ← New component
```

Or for complex components:
```
frontend/src/components/
└── ComponentName/
    ├── index.tsx              # Main component
    ├── ComponentName.tsx      # Component logic
    └── types.ts               # TypeScript types
```

## Automatic Features

- ✅ TypeScript props interface
- ✅ Tailwind CSS styling
- ✅ Proper file naming (PascalCase)
- ✅ Export statement
- ✅ JSDoc comments
- ✅ Accessibility attributes
- ✅ Responsive design classes

## Component Types

### 1. Presentational Component
- No state
- Pure UI rendering
- Takes props only
- Easy to test

### 2. Container Component
- Manages state
- Handles logic
- Fetches data
- Passes data to presentational components

### 3. Page Component
- Next.js route component
- Can be server or client
- Manages page-level state
- Includes SEO metadata

## Post-Creation Steps

1. Review generated code
2. Customize styling
3. Add business logic
4. Import and use in parent component
5. Test component behavior
6. Add to Storybook (if applicable)

## Example Output

```
✓ Created component: src/components/TaskCard.tsx
✓ Generated TypeScript interface: TaskCardProps
✓ Added Tailwind CSS styling
✓ Included 'use client' directive

Usage example:
import TaskCard from '@/components/TaskCard';

<TaskCard
  task={task}
  onUpdate={handleUpdate}
/>
```

## Best Practices

### Props Interface
```typescript
interface ComponentProps {
  // Required props
  id: string;
  title: string;

  // Optional props with defaults
  variant?: 'primary' | 'secondary';
  disabled?: boolean;

  // Callbacks
  onClick?: () => void;
  onSubmit?: (data: FormData) => void;

  // Children
  children?: React.ReactNode;
}
```

### State Management
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function Component() {
  const [data, setData] = useState<DataType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch data
  }, []);

  // Component logic
}
```

### Styling Patterns
```typescript
// Conditional classes
<div className={`base-classes ${isActive ? 'active-classes' : 'inactive-classes'}`}>

// Dynamic classes with helper
const buttonClasses = clsx(
  'px-4 py-2 rounded',
  variant === 'primary' && 'bg-indigo-600 text-white',
  variant === 'secondary' && 'bg-gray-200 text-gray-700',
  disabled && 'opacity-50 cursor-not-allowed'
);
```

## Common Patterns

### Form Input Component
```typescript
interface InputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
}

export default function Input({ label, value, onChange, error, required }: InputProps) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}
```

### Card Component
```typescript
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export default function Card({ title, children, footer }: CardProps) {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold">{title}</h3>
      </div>
      <div className="p-6">
        {children}
      </div>
      {footer && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          {footer}
        </div>
      )}
    </div>
  );
}
```

## Testing Components

```typescript
// Component usage
import Component from '@/components/Component';

<Component
  prop1="value"
  prop2={handler}
/>
```

## Related Skills

- `create-page` - Create Next.js page
- `test-frontend` - Test build
- `run-frontend` - See component in action
