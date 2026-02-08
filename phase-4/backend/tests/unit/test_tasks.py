"""
Unit tests for task endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import patch, MagicMock
from src.main import app
from src.models.user import User
from src.models.task import Task
from src.database import get_session


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    return session


def test_get_tasks_success(client, mock_session):
    """Test retrieving user's tasks successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task retrieval
        mock_task = Task(title="Test Task", user_id=1, id=1)
        with patch('src.services.task_service.get_user_tasks', return_value=[mock_task]):
            response = client.get(
                "/tasks",
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0]["title"] == "Test Task"


def test_get_tasks_user_not_found(client, mock_session):
    """Test retrieving tasks when user is not found."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user not found
        mock_session.exec.return_value.first.return_value = None

        response = client.get(
            "/tasks",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


def test_create_task_success(client, mock_session):
    """Test creating a new task successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task creation
        mock_created_task = Task(title="New Task", user_id=1, id=1)
        with patch('src.services.task_service.create_task', return_value=mock_created_task):
            response = client.post(
                "/tasks",
                json={"title": "New Task", "description": "Test description", "completed": False},
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert response.json()["title"] == "New Task"


def test_create_task_user_not_found(client, mock_session):
    """Test creating a task when user is not found."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user not found
        mock_session.exec.return_value.first.return_value = None

        response = client.post(
            "/tasks",
            json={"title": "New Task", "description": "Test description", "completed": False},
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


def test_get_task_by_id_success(client, mock_session):
    """Test retrieving a specific task by ID successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task retrieval
        mock_task = Task(title="Test Task", user_id=1, id=1)
        with patch('src.services.task_service.get_task_by_id', return_value=mock_task):
            response = client.get(
                "/tasks/1",
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert response.json()["title"] == "Test Task"


def test_get_task_by_id_not_found(client, mock_session):
    """Test retrieving a specific task that doesn't exist."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task not found
        with patch('src.services.task_service.get_task_by_id', return_value=None):
            response = client.get(
                "/tasks/999",
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 404
            assert "Task not found" in response.json()["detail"]


def test_update_task_success(client, mock_session):
    """Test updating a task successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task update
        updated_task = Task(title="Updated Task", user_id=1, id=1)
        with patch('src.services.task_service.update_task', return_value=updated_task):
            response = client.put(
                "/tasks/1",
                json={"title": "Updated Task"},
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert response.json()["title"] == "Updated Task"


def test_update_task_not_found(client, mock_session):
    """Test updating a task that doesn't exist."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task update returning None (not found)
        with patch('src.services.task_service.update_task', return_value=None):
            response = client.put(
                "/tasks/999",
                json={"title": "Updated Task"},
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 404
            assert "Task not found" in response.json()["detail"]


def test_delete_task_success(client, mock_session):
    """Test deleting a task successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task deletion
        with patch('src.services.task_service.delete_task', return_value=True):
            response = client.delete(
                "/tasks/1",
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"


def test_delete_task_not_found(client, mock_session):
    """Test deleting a task that doesn't exist."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task deletion returning False (not found)
        with patch('src.services.task_service.delete_task', return_value=False):
            response = client.delete(
                "/tasks/999",
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 404
            assert "Task not found" in response.json()["detail"]


def test_update_task_status_success(client, mock_session):
    """Test updating task completion status successfully."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task status update
        updated_task = Task(title="Test Task", user_id=1, id=1, completed=True)
        with patch('src.services.task_service.update_task_status', return_value=updated_task):
            response = client.patch(
                "/tasks/1",
                json={"completed": True},
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 200
            assert response.json()["completed"] is True
            assert response.json()["title"] == "Test Task"


def test_update_task_status_not_found(client, mock_session):
    """Test updating task status when task doesn't exist."""
    with patch('src.api.tasks.get_session', return_value=mock_session):
        # Mock user retrieval
        mock_user = User(email="test@example.com", hashed_password="hashed_password", id=1)
        mock_session.exec.return_value.first.return_value = mock_user

        # Mock task status update returning None (not found)
        with patch('src.services.task_service.update_task_status', return_value=None):
            response = client.patch(
                "/tasks/999",
                json={"completed": True},
                headers={"Authorization": "Bearer fake_token"}
            )

            assert response.status_code == 404
            assert "Task not found" in response.json()["detail"]