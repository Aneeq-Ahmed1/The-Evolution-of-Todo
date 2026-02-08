"""
Direct test of the tasks-with-display endpoint logic.
"""
import sys
sys.path.insert(0, 'backend/src')

# Mock imports to test the logic
class MockTask:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.description = ""
        self.completed = False
        self.priority = "medium"
        self.tags = None
        self.category = None
        self.due_date = None
        self.due_time = None
        self.is_recurring = False
        self.recurrence_pattern = None
        self.recurrence_interval = 1
        self.next_occurrence = None
        self.user_id = 1
        self.created_at = "2026-01-05T00:00:00"
        self.updated_at = "2026-01-05T00:00:00"

    def model_dump(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'tags': self.tags,
            'category': self.category,
            'due_date': self.due_date,
            'due_time': self.due_time,
            'is_recurring': self.is_recurring,
            'recurrence_pattern': self.recurrence_pattern,
            'recurrence_interval': self.recurrence_interval,
            'next_occurrence': self.next_occurrence,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Test the actual function
try:
    from services.mapping_service import mapping_service

    tasks = [
        MockTask(1, "Buy groceries"),
        MockTask(2, "Pay bills"),
        MockTask(3, "Call dentist")
    ]

    print("Testing get_task_with_display_index...")
    result = mapping_service.get_task_with_display_index(tasks, "test_user")
    print(f"✓ Success! Got {len(result)} tasks with display indices")

    for task in result:
        print(f"  - Task {task.display_index}: {task.title}")

    print("\nTesting generate_display_mapping...")
    mapping = mapping_service.generate_display_mapping(tasks, "test_user")
    print(f"✓ Success! Generated {len(mapping)} mappings")

    for m in mapping:
        print(f"  - display_index: {m['display_index']}, task_id: {m['task_id']}")

    print("\n✓ All tests passed!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
