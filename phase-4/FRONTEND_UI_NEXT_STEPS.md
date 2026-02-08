# Frontend UI - Advanced Features Implementation Guide

**Status:** Backend 100% Ready | Frontend UI Needs Update
**Estimated Time:** 2-3 hours

---

## ✅ Already Done:

1. API client updated with filter support (`lib/api.ts`)
2. TypeScript types complete with all fields (`types/task.ts`)
3. Backend fully supports advanced features

---

## 🔧 Step-by-Step Frontend Updates Needed:

### Step 1: Update TaskForm Component

**File:** `frontend/src/components/TaskForm.tsx`

**Add these state variables:**
```tsx
const [priority, setPriority] = useState(task?.priority || 'medium');
const [category, setCategory] = useState(task?.category || '');
const [tags, setTags] = useState(task?.tags || '');
const [dueDate, setDueDate] = useState(task?.due_date?.split('T')[0] || '');
const [dueTime, setDueTime] = useState(task?.due_time || '');
const [isRecurring, setIsRecurring] = useState(task?.is_recurring || false);
const [recurrencePattern, setRecurrencePattern] = useState(task?.recurrence_pattern || 'daily');
const [recurrenceInterval, setRecurrenceInterval] = useState(task?.recurrence_interval || 1);
```

**Add these fields after description field:**
```tsx
{/* Priority */}
<div>
  <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
    Priority
  </label>
  <select
    value={priority}
    onChange={(e) => setPriority(e.target.value)}
    className="w-full px-3 py-2.5 rounded text-sm"
    style={{ border: '1px solid #e0e4e9' }}
  >
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
  </select>
</div>

{/* Category */}
<div>
  <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
    Category
  </label>
  <input
    type="text"
    value={category}
    onChange={(e) => setCategory(e.target.value)}
    placeholder="e.g., work, personal, shopping"
    className="w-full px-3 py-2.5 rounded text-sm"
    style={{ border: '1px solid #e0e4e9' }}
  />
</div>

{/* Tags */}
<div>
  <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
    Tags <span className="text-xs" style={{ color: '#828a93' }}>(comma-separated)</span>
  </label>
  <input
    type="text"
    value={tags}
    onChange={(e) => setTags(e.target.value)}
    placeholder="e.g., urgent, meeting, important"
    className="w-full px-3 py-2.5 rounded text-sm"
    style={{ border: '1px solid #e0e4e9' }}
  />
</div>

{/* Due Date & Time */}
<div className="grid grid-cols-2 gap-3">
  <div>
    <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
      Due Date
    </label>
    <input
      type="date"
      value={dueDate}
      onChange={(e) => setDueDate(e.target.value)}
      className="w-full px-3 py-2.5 rounded text-sm"
      style={{ border: '1px solid #e0e4e9' }}
    />
  </div>
  <div>
    <label className="block text-sm font-medium mb-1.5" style={{ color: '#232a31' }}>
      Due Time
    </label>
    <input
      type="time"
      value={dueTime}
      onChange={(e) => setDueTime(e.target.value)}
      className="w-full px-3 py-2.5 rounded text-sm"
      style={{ border: '1px solid #e0e4e9' }}
    />
  </div>
</div>

{/* Recurring Task */}
<div>
  <label className="flex items-center gap-2">
    <input
      type="checkbox"
      checked={isRecurring}
      onChange={(e) => setIsRecurring(e.target.checked)}
      style={{ accentColor: '#7e1fff' }}
    />
    <span className="text-sm font-medium" style={{ color: '#232a31' }}>
      Recurring Task
    </span>
  </label>
</div>

{/* Recurrence Options - Only show if recurring */}
{isRecurring && (
  <div className="grid grid-cols-2 gap-3 p-3 rounded" style={{ backgroundColor: '#f5f8fa' }}>
    <div>
      <label className="block text-xs font-medium mb-1" style={{ color: '#232a31' }}>
        Repeat Every
      </label>
      <input
        type="number"
        min="1"
        value={recurrenceInterval}
        onChange={(e) => setRecurrenceInterval(Number(e.target.value))}
        className="w-full px-2 py-1.5 rounded text-sm"
        style={{ border: '1px solid #e0e4e9' }}
      />
    </div>
    <div>
      <label className="block text-xs font-medium mb-1" style={{ color: '#232a31' }}>
        Pattern
      </label>
      <select
        value={recurrencePattern}
        onChange={(e) => setRecurrencePattern(e.target.value)}
        className="w-full px-2 py-1.5 rounded text-sm"
        style={{ border: '1px solid #e0e4e9' }}
      >
        <option value="daily">Day(s)</option>
        <option value="weekly">Week(s)</option>
        <option value="monthly">Month(s)</option>
      </select>
    </div>
  </div>
)}
```

**Update submit function:**
```tsx
const response = await apiClient.tasks.create({
  title,
  description,
  priority,
  category,
  tags,
  due_date: dueDate ? new Date(dueDate).toISOString() : undefined,
  due_time: dueTime,
  is_recurring: isRecurring,
  recurrence_pattern: isRecurring ? recurrencePattern : undefined,
  recurrence_interval: isRecurring ? recurrenceInterval : undefined,
});
```

---

### Step 2: Update Dashboard with Search & Filters

**File:** `frontend/src/app/dashboard/tasks/page.tsx`

**Add state:**
```tsx
const [searchTerm, setSearchTerm] = useState('');
const [priorityFilter, setPriorityFilter] = useState<'all' | 'low' | 'medium' | 'high'>('all');
const [categoryFilter, setCategoryFilter] = useState('all');
const [sortBy, setSortBy] = useState<'created_at' | 'due_date' | 'priority' | 'title'>('created_at');
const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
```

**Update loadTasks:**
```tsx
const tasksData = await apiClient.tasks.getAll({
  search: searchTerm,
  priority: priorityFilter,
  category: categoryFilter,
  completed: filter === 'all' ? undefined : filter === 'completed',
  sortBy,
  sortOrder
}).then(res => res.data);
```

**Add search bar before filter buttons:**
```tsx
{/* Search Bar */}
<div className="mb-4">
  <input
    type="text"
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    placeholder="Search tasks..."
    className="w-full px-3 py-2 rounded text-sm"
    style={{ border: '1px solid #e0e4e9' }}
  />
</div>

{/* Advanced Filters */}
<div className="flex gap-2 mb-4 flex-wrap">
  <select
    value={priorityFilter}
    onChange={(e) => setPriorityFilter(e.target.value as any)}
    className="px-3 py-1.5 rounded text-xs"
    style={{ border: '1px solid #e0e4e9' }}
  >
    <option value="all">All Priorities</option>
    <option value="high">High</option>
    <option value="medium">Medium</option>
    <option value="low">Low</option>
  </select>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value as any)}
    className="px-3 py-1.5 rounded text-xs"
    style={{ border: '1px solid #e0e4e9' }}
  >
    <option value="created_at">Created Date</option>
    <option value="due_date">Due Date</option>
    <option value="priority">Priority</option>
    <option value="title">Title</option>
  </select>

  <button
    onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
    className="px-3 py-1.5 rounded text-xs"
    style={{ border: '1px solid #e0e4e9' }}
  >
    {sortOrder === 'asc' ? '↑ Asc' : '↓ Desc'}
  </button>

  <button
    onClick={() => loadTasks()}
    className="px-3 py-1.5 rounded text-xs font-medium"
    style={{ backgroundColor: '#7e1fff', color: '#ffffff' }}
  >
    Apply Filters
  </button>
</div>
```

---

### Step 3: Update TaskList to Show Advanced Fields

**File:** `frontend/src/components/TaskList.tsx`

**Add priority badge function:**
```tsx
const getPriorityColor = (priority: string) => {
  switch(priority) {
    case 'high': return { bg: '#fee', color: '#c00', text: 'HIGH' };
    case 'medium': return { bg: '#fef3e0', color: '#f59e0b', text: 'MED' };
    case 'low': return { bg: '#efe', color: '#0a0', text: 'LOW' };
    default: return { bg: '#f0f3f5', color: '#6e7780', text: 'MED' };
  }
};
```

**Display in task item:**
```tsx
{/* Priority Badge */}
<span className="px-2 py-0.5 rounded text-xs font-medium" style={{
  backgroundColor: getPriorityColor(task.priority).bg,
  color: getPriorityColor(task.priority).color
}}>
  {getPriorityColor(task.priority).text}
</span>

{/* Category */}
{task.category && (
  <span className="px-2 py-0.5 rounded text-xs" style={{
    backgroundColor: '#f0f3f5',
    color: '#6e7780'
  }}>
    {task.category}
  </span>
)}

{/* Tags */}
{task.tags && task.tags.split(',').map(tag => (
  <span key={tag} className="px-2 py-0.5 rounded text-xs" style={{
    backgroundColor: '#f0f3f5',
    color: '#7e1fff'
  }}>
    #{tag.trim()}
  </span>
))}

{/* Due Date */}
{task.due_date && (
  <span className="text-xs" style={{ color: '#6e7780' }}>
    📅 {new Date(task.due_date).toLocaleDateString()}
    {task.due_time && ` at ${task.due_time}`}
  </span>
)}

{/* Recurring Icon */}
{task.is_recurring && (
  <span className="text-xs" style={{ color: '#7e1fff' }}>
    🔁 {task.recurrence_pattern}
  </span>
)}
```

---

### Step 4: Add Notification Service (Optional)

**File:** `frontend/src/lib/notifications.ts` (New)

```tsx
export const requestNotificationPermission = async () => {
  if ('Notification' in window) {
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }
  return false;
};

export const showTaskNotification = (task: Task) => {
  if (Notification.permission === 'granted') {
    new Notification('Task Due Soon!', {
      body: `${task.title} is due ${task.due_time ? 'at ' + task.due_time : 'today'}`,
      icon: '/icon.png',
      tag: `task-${task.id}`
    });
  }
};

export const checkUpcomingTasks = async () => {
  const tasks = await apiClient.tasks.getAll({
    // Get tasks due in next 24 hours
    // (needs backend endpoint or client-side filtering)
  });

  tasks.data.forEach(task => {
    if (task.due_date && !task.completed) {
      const dueDate = new Date(task.due_date);
      const now = new Date();
      const hoursUntilDue = (dueDate.getTime() - now.getTime()) / (1000 * 60 * 60);

      if (hoursUntilDue > 0 && hoursUntilDue <= 24) {
        showTaskNotification(task);
      }
    }
  });
};
```

---

## 🎨 Quick Visual Reference:

### TaskForm will look like:
```
┌─ Create New Task ─────────────────┐
│ Title: [_____________________]    │
│ Description: [_______________]    │
│ Priority: [Medium ▼]              │
│ Category: [work]                  │
│ Tags: [urgent, meeting]           │
│ Due Date: [2025-01-15]            │
│ Due Time: [10:00]                 │
│ □ Recurring Task                  │
│   ┌─ Recurrence ───────┐          │
│   │ Every: [1] [Week ▼]│          │
│   └─────────────────────┘          │
│ [Cancel] [Save Task]              │
└───────────────────────────────────┘
```

### Dashboard with filters:
```
┌─ My Tasks ────────────────────────┐
│ [Search: ____________] [Apply]    │
│ [All Priorities ▼] [Created ▼] ↓  │
│                                    │
│ All (5) | Pending (3) | Done (2)  │
│                                    │
│ ┌─ Task 1 ──────────────┐         │
│ │ [✓] Meeting         HIGH│        │
│ │ work  #urgent            │       │
│ │ 📅 Jan 15 🔁 weekly     │       │
│ └─────────────────────────┘        │
└────────────────────────────────────┘
```

---

## ⚡ Quick Implementation (Minimal Viable):

If short on time, implement these MINIMUM features:

**Priority 1:**
- Add priority dropdown to TaskForm
- Show priority badge in TaskList
- Add search bar

**Priority 2:**
- Add category field
- Add due date picker
- Filter by priority

**Can Skip:**
- Tags (nice to have)
- Recurring tasks (complex)
- Notifications (extra)

---

## 🧪 Testing Checklist:

After frontend updates:
- [ ] Create task with priority=high
- [ ] Search for task by title
- [ ] Filter by priority
- [ ] Create task with due date
- [ ] Create recurring daily task
- [ ] Mark recurring task complete (should create next instance)
- [ ] View task with category and tags
- [ ] Sort tasks by due date

---

**Current Token Usage:** 255k/1M
**Recommendation:** Continue in new session for frontend UI updates

