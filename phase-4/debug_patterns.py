import re

# Test the patterns from the todo agent
complete_patterns = [
    (r"(complete|done|finish)\s+task\s+(\d+)", 2),  # Handle "complete task 1" pattern - task number in group 2
    (r"(complete|done|finish)\s+#(\d+)", 2),       # Handle "complete #1" pattern - task number in group 2
    (r"task\s+(\d+)\s+is\s+(done|completed|finished)", 1),  # Handle "task 1 is done" pattern - task number in group 1
    (r"task\s+(\d+)\s+(done|completed|finished)", 1),       # Handle "task 1 done" pattern - task number in group 1
    (r"task\s+#?(\d+)\s+(done|completed|finished)", 1),     # Handle "task #1 done" or "task 1 done" pattern - task number in group 1
    (r"(done|complete|finished|completed)\s+(.*)", 2),      # Handle "done task_name" pattern - task name in group 2
    (r"mark\s+(.*)\s+(done|complete|finished)", 1),         # Handle "mark task_name done" pattern - task name in group 1
]

delete_patterns = [
    (r"(delete|remove|cancel|get\s+rid\s+of)\s+(.*)", 2),  # Handle "delete task_name" - task name in group 2
    (r"(delete|remove|cancel|get\s+rid\s+of)\s+task\s+(\d+)", 2),  # Handle "delete task 1" - task number in group 2
    (r"(delete|remove|cancel|get\s+rid\s+of)\s+#(\d+)", 2),  # Handle "delete #1" - task number in group 2
    (r"task\s+(\d+)\s+(delete|remove|cancel)", 1),  # Handle "task 1 delete" - task number in group 1
]

test_messages = [
    "task 1 is done",
    "task 1 done",
    "complete task 1",
    "delete task 2",
    "task 2 delete",
    "task 1 is completed",
    "task 4 delete"
]

print("Testing complete patterns:")
for message in test_messages:
    print(f"\nTesting: '{message}'")
    message_lower = message.lower().strip()

    # Test complete patterns
    for pattern, target_group in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_identifier = match.group(target_group)
            print(f"  Complete pattern matched: {pattern}")
            print(f"  Task identifier: '{task_identifier}' (group {target_group})")

    # Test delete patterns
    for pattern, target_group in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_identifier = match.group(target_group)
            print(f"  Delete pattern matched: {pattern}")
            print(f"  Task identifier: '{task_identifier}' (group {target_group})")