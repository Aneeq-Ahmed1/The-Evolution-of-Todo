#!/usr/bin/env python3
"""
Debug script to test the todo agent's intent parsing functionality.
"""

import re
from sqlmodel import Session, SQLModel, create_engine, select
from backend.src.models.chat_task import ChatTask
from backend.src.agents.todo_agent import TodoAgent

# Create a mock session for testing
engine = create_engine("sqlite:///debug_test.db")
SQLModel.metadata.create_all(engine)

# Create a test session
with Session(engine) as session:
    # Add some test tasks for demo_user
    task1 = ChatTask(user_id="demo_user", title="a task to buy groceries", completed=False)
    task2 = ChatTask(user_id="demo_user", title="new task for purchase books", completed=False)
    session.add(task1)
    session.add(task2)
    session.commit()

    # Create the agent
    agent = TodoAgent(session)

    # Test the intent parsing
    test_messages = [
        "task 1 is done",
        "task 2 delete",
        "complete task 1",
        "delete task 2"
    ]

    for message in test_messages:
        print(f"\nTesting message: '{message}'")
        intent, params = agent._parse_intent(message, "demo_user")
        print(f"  Intent: {intent}")
        print(f"  Params: {params}")

        if intent == "complete_task":
            result = agent._handle_complete_task(params)
            print(f"  Complete result: {result}")
        elif intent == "delete_task":
            result = agent._handle_delete_task(params)
            print(f"  Delete result: {result}")
        elif intent == "ask_for_clarification":
            print(f"  Clarification needed: {params.get('message', 'No message')}")
        elif intent == "unknown":
            print(f"  Unknown intent")