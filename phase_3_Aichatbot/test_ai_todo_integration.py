"""
End-to-End Test for AI Todo Assistant Integration
This script tests the complete flow from user input to database operations
"""
import asyncio
import httpx
import json
from uuid import uuid4

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    # You'll need to provide a valid JWT token for testing
    # "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}

async def test_ai_todo_integration():
    """
    Test the complete AI Todo assistant integration
    """
    print("Starting AI Todo Assistant Integration Test...")
    
    # Create a new conversation
    print("\n1. Creating a new conversation...")
    async with httpx.AsyncClient() as client:
        # For this test, we'll need a valid JWT token
        # This assumes you have a way to authenticate for testing
        try:
            # First, let's try to create a conversation without auth to see if it works
            response = await client.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": "Hi, I want to test the todo functionality",
                    "conversation_id": None
                },
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                conversation_id = result.get("conversation_id")
                print(f"✓ Conversation created successfully with ID: {conversation_id}")
            else:
                print(f"✗ Failed to create conversation: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Error creating conversation: {str(e)}")
            return False
    
    # Test adding a task
    print("\n2. Testing task creation...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": "Add a task: Buy groceries",
                    "conversation_id": conversation_id
                },
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Task creation response: {result['response']}")
            else:
                print(f"✗ Failed to add task: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error adding task: {str(e)}")
        return False
    
    # Test listing tasks
    print("\n3. Testing task listing...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": "Show me my tasks",
                    "conversation_id": conversation_id
                },
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Task listing response: {result['response']}")
            else:
                print(f"✗ Failed to list tasks: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error listing tasks: {str(e)}")
        return False
    
    # Test completing a task
    print("\n4. Testing task completion...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": "Mark the grocery task as complete",
                    "conversation_id": conversation_id
                },
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Task completion response: {result['response']}")
            else:
                print(f"✗ Failed to complete task: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error completing task: {str(e)}")
        return False
    
    # Test adding another task
    print("\n5. Testing another task creation...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": "Add a new task: Walk the dog",
                    "conversation_id": conversation_id
                },
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Second task creation response: {result['response']}")
            else:
                print(f"✗ Failed to add second task: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error adding second task: {str(e)}")
        return False
    
    print("\n✓ All tests completed successfully!")
    print(f"✓ Conversation ID: {conversation_id}")
    return True

async def test_direct_mcp_tools():
    """
    Test the MCP tools directly to ensure they work with the database
    """
    print("\nTesting MCP tools directly...")
    
    # Test create_task MCP tool
    print("\n1. Testing create_task MCP tool...")
    try:
        async with httpx.AsyncClient() as client:
            # This would require a valid JWT token to be passed in headers
            # For testing purposes, we'll need to simulate this differently
            print("Note: Direct MCP tool testing requires authentication headers with valid JWT")
            print("Skipping direct MCP tool test for now...")
    except Exception as e:
        print(f"✗ Error in direct MCP tool test: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("Running AI Todo Assistant Integration Tests...")
    
    # Run the integration test
    success = asyncio.run(test_ai_todo_integration())
    
    if success:
        print("\n🎉 All integration tests passed!")
        print("The AI assistant should now be able to handle todo actions properly.")
    else:
        print("\n❌ Some tests failed.")
        print("Please check the implementation and try again.")
    
    # Optionally run direct MCP tool tests
    # asyncio.run(test_direct_mcp_tools())