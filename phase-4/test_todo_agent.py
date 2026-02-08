"""
Simple test script for TodoAgent with display mapping.

This script tests the AI agent's ability to:
1. List tasks
2. Complete tasks using ordinal references
3. Edit tasks
4. Delete tasks
"""
import sys
import os

# Add the agents/backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents', 'backend'))

from src.agents.todo_agent import create_agent

def main():
    """Test the TodoAgent with various commands."""

    # Configuration
    API_BASE_URL = "http://localhost:8000"

    # Get auth token from user
    print("=" * 60)
    print("TodoAgent Test Script")
    print("=" * 60)
    print()
    print("Before testing, please:")
    print("1. Make sure backend is running (http://localhost:8000)")
    print("2. Login to the app and get your JWT token")
    print("3. You can get token from localStorage in browser console:")
    print("   localStorage.getItem('access_token')")
    print()

    auth_token = input("Enter your JWT token: ").strip()

    if not auth_token:
        print("Error: Token is required!")
        return

    # Create agent
    print("\nCreating TodoAgent...")
    agent = create_agent(API_BASE_URL, auth_token)

    # Test commands
    test_commands = [
        "list tasks",
        "task 1 is complete",
        "mark first task as complete",
        "edit task 2",
        "delete task 3",
        "show me task one",
        "complete the second task",
        "delete the 5th task",  # This should fail with helpful error
    ]

    print("\n" + "=" * 60)
    print("Testing TodoAgent Commands")
    print("=" * 60)

    for i, command in enumerate(test_commands, 1):
        print(f"\n[Test {i}] Command: \"{command}\"")
        print("-" * 60)

        result = agent.process_command(command)

        print(f"Success: {result['success']}")
        print(f"Intent: {result['intent']}")
        print(f"Display Index: {result.get('display_index')}")
        print(f"Message: {result['message']}")

        if result.get('data'):
            print(f"Data: {result['data']}")

        # Wait for user before next command
        if i < len(test_commands):
            input("\nPress Enter to continue to next test...")

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
