# Frontend Guidelines - Todo Full-Stack App

**Framework:** Next.js 15 (App Router)
**Language:** TypeScript
**Styling:** Tailwind CSS + Custom CSS
**Design System:** Yahoo.com-inspired

---

## Tech Stack

- **Next.js:** 15.0.0 with App Router
- **React:** 19.0.0
- **TypeScript:** 5.6.2
- **Tailwind CSS:** 4.1.18
- **Font:** Inter (Google Fonts)

---

## Project Structure

```
frontend/src/
├── app/
│   ├── page.tsx              # Landing page
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles + Yahoo theme
│   ├── auth/
│   │   ├── login/page.tsx   # Login page
│   │   └── register/page.tsx # Register page
│   ├── dashboard/
│   │   ├── page.tsx         # Dashboard redirect
│   │   └── tasks/page.tsx   # Main task interface
│   └── admin/
│       └── page.tsx          # Admin panel
├── components/
│   ├── TaskList.tsx         # Task list component
│   └── TaskForm.tsx         # Task form component
├── lib/
│   ├── auth.ts              # Auth utilities
│   └── api.ts               # API client with JWT
├── services/
│   └── taskService.ts       # Task service layer
└── types/
    ├── task.ts              # Task TypeScript types
    └── auth.ts              # Auth types
```

---

## Design System

### Yahoo Color Palette (Use Exact Colors)

```typescript
// Use these exact hex codes
const colors = {
  primary: '#7e1fff',      // Purple - buttons, links, logo
  background: '#f5f8fa',   // Light gray-blue - page bg
  textDark: '#232a31',     // Headings
  textMedium: '#6e7780',   // Body text
  textLight: '#828a93',    // Subtle text
  border: '#e0e4e9',       // Borders, dividers
  buttonBg: '#f0f3f5',     // Secondary buttons
  white: '#ffffff',        // Cards, nav
  error: '#c00',           // Error messages
  success: '#0a0',         // Success messages
};
```

### Component Patterns

**Navigation Bar:**
```tsx
<nav style={{ height: '57px', borderColor: '#e0e4e9' }}>
  // Yahoo standard height
</nav>
```

**Buttons:**
```tsx
// Primary button
<button style={{
  backgroundColor: '#7e1fff',
  color: '#ffffff',
  minHeight: '44px'  // Accessibility
}}>
  Click Me
</button>

// Secondary button
<button style={{
  backgroundColor: '#f0f3f5',
  color: '#232a31'
}}>
  Cancel
</button>
```

**Cards:**
```tsx
<div className="bg-white rounded p-4" style={{
  border: '1px solid #e0e4e9'
}}>
  Content
</div>
```

**Input Fields:**
```tsx
<input
  className="w-full px-3 py-2.5 rounded text-sm"
  style={{
    border: '1px solid #e0e4e9',
    backgroundColor: '#ffffff',
    color: '#232a31'
  }}
/>
```

---

## Styling Guidelines

### Use Inline Styles for Yahoo Colors
```tsx
// Good - exact Yahoo colors
<h1 style={{ color: '#232a31' }}>Title</h1>

// Avoid - Tailwind approximations
<h1 className="text-gray-900">Title</h1>
```

### Spacing (Yahoo-style Compact)
```tsx
// Sections: py-6 to py-10 (compact)
<section className="py-8">

// Cards: p-4 to p-6
<div className="p-4">

// Navigation: h-14 or exact 57px
<nav style={{ height: '57px' }}>
```

### Typography
```tsx
// Headings: font-semibold (not bold)
<h1 className="text-2xl font-semibold">

// Body: text-sm to text-base
<p className="text-sm">
```

---

## Component Development

### Page Structure Pattern
```tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function PageName() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  // Loading state with Yahoo spinner
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center"
           style={{ backgroundColor: '#f5f8fa' }}>
        <div className="text-center">
          <div className="relative w-10 h-10 mx-auto mb-3">
            <div className="absolute inset-0 rounded-full border-2"
                 style={{ borderColor: '#e0e4e9' }}></div>
            <div className="absolute inset-0 rounded-full border-2 border-t-transparent animate-spin"
                 style={{ borderColor: '#7e1fff' }}></div>
          </div>
          <p className="text-sm" style={{ color: '#828a93' }}>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f5f8fa' }}>
      {/* Content */}
    </div>
  );
}
```

---

## API Communication

### Using API Client
```typescript
import { apiClient } from '@/lib/api';

// Get all tasks
const tasks = await apiClient.tasks.getAll();

// Create task
const newTask = await apiClient.tasks.create({
  title: 'My task',
  description: 'Optional description'
});

// Update task
await apiClient.tasks.update(taskId, {
  title: 'Updated title',
  completed: true
});

// Delete task
await apiClient.tasks.delete(taskId);
```

### Error Handling
```typescript
try {
  const result = await apiClient.tasks.getAll();
  setTasks(result.data);
} catch (error: any) {
  if (error.status === 401) {
    // Redirect to login
    router.push('/auth/login');
  } else {
    setError(error.message);
  }
}
```

---

## Authentication Patterns

### Check if User is Logged In
```typescript
import { isAuthenticated } from '@/lib/auth';

const loggedIn = isAuthenticated(); // Returns boolean
```

### Login User
```typescript
import { signIn } from '@/lib/auth';

const result = await signIn.email({
  email: 'user@example.com',
  password: 'password123',
  callbackURL: '/dashboard'
});

if (result?.error) {
  // Handle error
} else {
  // Redirect to dashboard
  router.push('/dashboard');
}
```

### Logout User
```typescript
import { signOut } from '@/lib/auth';

await signOut();
router.push('/');
```

---

## Form Patterns

### Standard Form
```tsx
const [formData, setFormData] = useState({ email: '', password: '' });
const [error, setError] = useState('');
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  setIsLoading(true);

  try {
    // API call
    setIsLoading(false);
  } catch (err) {
    setError('Error message');
    setIsLoading(false);
  }
};
```

### Error Display
```tsx
{error && (
  <div className="p-3 rounded" style={{
    backgroundColor: '#fee',
    border: '1px solid #fcc'
  }}>
    <p className="text-sm" style={{ color: '#c00' }}>{error}</p>
  </div>
)}
```

---

## Responsive Design

### Breakpoints (Tailwind)
```tsx
// Mobile first
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">

// Show/hide on mobile
<button className="hidden md:inline-flex">Desktop Only</button>
```

### Mobile-Friendly Buttons
```tsx
// Minimum 44px height for touch
<button style={{ minHeight: '44px' }}>
  Click Me
</button>
```

---

## Performance Optimization

### Best Practices
- Use `'use client'` only when necessary
- Lazy load images if added
- Minimize bundle size
- Use React.memo for expensive components
- Avoid unnecessary re-renders

---

## Testing Checklist

### Before Deployment
- [ ] All forms validate properly
- [ ] Error messages are clear
- [ ] Loading states show correctly
- [ ] Yahoo colors applied consistently
- [ ] Responsive on mobile/tablet/desktop
- [ ] All links work
- [ ] Authentication flow works
- [ ] API errors handled gracefully

---

**Frontend Version:** 2.0
**Last Updated:** December 31, 2025
**Status:** ✅ Complete
