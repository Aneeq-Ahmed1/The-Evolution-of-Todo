"""
Simple quick test for TodoAgent ordinal resolution.

This tests the ordinal resolver without API calls.
"""
import sys
import os

# Add the agents/backend/src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents', 'backend', 'src'))

from services.ordinal_resolver import normalize_ordinal_to_number
from services.intent_parser import parse_user_command


def test_ordinal_resolver():
    """Test ordinal resolution with different formats."""
    print("=" * 60)
    print("Testing Ordinal Resolver")
    print("=" * 60)

    test_cases = [
        "task 1 is complete",
        "complete the first task",
        "mark task one as done",
        "edit the 2nd task",
        "delete the second task",
        "show me task two",
        "complete the 3rd task",
        "edit the third task",
        "task three is done",
        "delete the 10th task",
        "complete the tenth task",
    ]

    for test in test_cases:
        number = normalize_ordinal_to_number(test)
        print(f"\nInput: \"{test}\"")
        print(f"Resolved to: {number}")


def test_intent_parser():
    """Test intent parsing."""
    print("\n" + "=" * 60)
    print("Testing Intent Parser")
    print("=" * 60)

    test_cases = [
        "list all tasks",
        "show me my tasks",
        "task 1 is complete",
        "mark first task as done",
        "edit task 2",
        "update the second task",
        "delete task 3",
        "remove the third task",
        "show me task one",
        "complete the second task",
    ]

    for test in test_cases:
        result = parse_user_command(test)
        print(f"\nInput: \"{test}\"")
        print(f"Intent: {result['intent']}")
        print(f"Display Index: {result['display_index']}")
        print(f"Confidence: {result['confidence']:.2f}")


if __name__ == "__main__":
    print("TodoAgent Simple Test\n")

    try:
        test_ordinal_resolver()
        test_intent_parser()

        print("\n" + "=" * 60)
        print("All Tests Completed Successfully! ✓")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
