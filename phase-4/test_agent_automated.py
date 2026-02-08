"""
Automated test script for TodoAgent (no user input required).
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

    # Use the test token (fresh token)
    AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X2FnZW50QGV4YW1wbGUuY29tIiwiZXhwIjoxNzY3NjA5NTc2fQ.wA9uspcmp6XkGSZCRMEqs1clfobic18XEvh0i6iGR8k"

    print("=" * 60)
    print("TodoAgent Automated Test")
    print("=" * 60)
    print(f"\nAPI: {API_BASE_URL}")
    print("User: test_display@example.com")
    print()

    # Create agent
    print("Creating TodoAgent...")
    agent = create_agent(API_BASE_URL, AUTH_TOKEN)
    print("Agent created successfully!")

    # Test commands
    test_commands = [
        "list tasks",
        "task 1 is complete",
        "mark first task as complete",
        "show me task 2",
        "delete task 3",
        "complete the second task",
    ]

    print("\n" + "=" * 60)
    print("Testing TodoAgent Commands")
    print("=" * 60)

    for i, command in enumerate(test_commands, 1):
        print(f"\n[Test {i}] Command: \"{command}\"")
        print("-" * 60)

        try:
            result = agent.process_command(command)

            print(f"Success: {result['success']}")
            print(f"Intent: {result['intent']}")
            print(f"Display Index: {result.get('display_index')}")
            print(f"Message: {result['message'][:200]}")  # Limit message length

            if result.get('data'):
                if isinstance(result['data'], dict):
                    print(f"Data: {result['data'].get('title', result['data'])}")
                else:
                    print(f"Data: [data present]")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
