import sys
import os

# Add project root to sys.path to fix import errors during tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Import your FastAPI app and models
from run import app
from backend.database import Base, get_db
from backend.models import Category, Task, TaskStatus, TaskPriority

# Use a separate test database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}


def test_create_category(client):
    response = client.post(
        "/api/categories/",
        json={"name": "Work", "color": "#FF0000"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Work"
    assert data["color"] == "#FF0000"
    assert "id" in data
    assert "created_at" in data


def test_create_task(client, db):
    # First create a category
    category = Category(name="Work", color="#FF0000")
    db.add(category)
    db.commit()
    db.refresh(category)

    # Create a task with the category id
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "priority": "medium",
            "category_id": category.id,
            "due_date": datetime.now(timezone.utc).isoformat()
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == TaskStatus.PENDING.value  # Enum value (string)
    assert data["priority"] == TaskPriority.MEDIUM.value
    assert data["category_id"] == category.id


def test_read_tasks(client, db):
    # Create tasks
    task1 = Task(title="Task 1", status=TaskStatus.PENDING.value)
    task2 = Task(title="Task 2", status=TaskStatus.COMPLETED.value)
    db.add(task1)
    db.add(task2)
    db.commit()

    response = client.get("/api/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_update_task(client, db):
    # Create a task
    task = Task(title="Original Task", status=TaskStatus.PENDING.value)
    db.add(task)
    db.commit()
    db.refresh(task)

    # Update the task
    response = client.put(
        f"/api/tasks/{task.id}",
        json={
            "title": "Updated Task",
            "status": "completed"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == TaskStatus.COMPLETED.value


def test_delete_task(client, db):
    # Create a task
    task = Task(title="Task to Delete", status=TaskStatus.PENDING.value)
    db.add(task)
    db.commit()
    db.refresh(task)

    # Delete the task
    response = client.delete(f"/api/tasks/{task.id}")
    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(f"/api/tasks/{task.id}")
    assert response.status_code == 404


def test_read_category(client, db):
    # Create a category
    category = Category(name="Personal", color="#00FF00")
    db.add(category)
    db.commit()
    db.refresh(category)
    
    # Get the category
    response = client.get(f"/api/categories/{category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Personal"
    assert data["color"] == "#00FF00"
    assert data["id"] == category.id


def test_update_category(client, db):
    # Create a category
    category = Category(name="Shopping", color="#0000FF")
    db.add(category)
    db.commit()
    db.refresh(category)
    
    # Update the category
    response = client.put(
        f"/api/categories/{category.id}",
        json={
            "name": "Groceries",
            "color": "#00FFFF"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Groceries"
    assert data["color"] == "#00FFFF"
    
    # Verify the update in the database
    updated_response = client.get(f"/api/categories/{category.id}")
    updated_data = updated_response.json()
    assert updated_data["name"] == "Groceries"


def test_delete_category(client, db):
    # Create a category
    category = Category(name="Temporary", color="#FF00FF")
    db.add(category)
    db.commit()
    db.refresh(category)
    
    # Delete the category
    response = client.delete(f"/api/categories/{category.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Category deleted successfully"
    
    # Verify category is deleted
    get_response = client.get(f"/api/categories/{category.id}")
    assert get_response.status_code == 404


def test_filter_tasks_by_status(client, db):
    # Create tasks with different statuses
    task1 = Task(title="Pending Task", status=TaskStatus.PENDING.value)
    task2 = Task(title="In Progress Task", status=TaskStatus.IN_PROGRESS.value)
    task3 = Task(title="Completed Task", status=TaskStatus.COMPLETED.value)
    task4 = Task(title="Another Pending Task", status=TaskStatus.PENDING.value)
    
    db.add(task1)
    db.add(task2)
    db.add(task3)
    db.add(task4)
    db.commit()
    
    # Filter by PENDING status
    response = client.get("/api/tasks/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Pending Task" in titles
    assert "Another Pending Task" in titles
    assert "Completed Task" not in titles
    
    # Filter by COMPLETED status
    response = client.get("/api/tasks/?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Completed Task"



# test_health_check: Verifies the API health endpoint returns a 200 status code and confirms database connectivity with the expected JSON response.
# test_create_category: Tests the API can successfully create a new category with name and color attributes, returning proper data with ID and timestamp.
# test_create_task: Validates task creation with various attributes including title, description, status, priority, category association, and due date.
# test_read_tasks: Ensures the API correctly returns a list of all tasks in the database with proper data structure.
# test_update_task: Confirms the ability to modify existing task properties like title and status through the PUT endpoint.
# test_delete_task: Verifies that tasks can be properly deleted and subsequent retrieval attempts return a 404 error.
# test_read_category: Tests that a specific category can be retrieved by ID with all its attributes correctly populated.
# test_update_category: Validates that category properties can be updated and the changes are properly persisted in the database.
# test_delete_category: Ensures categories can be deleted and confirms deletion with a 404 response on subsequent retrieval attempts.
# test_filter_tasks_by_status: Tests the API's ability to filter tasks by their status (pending, in-progress, completed) using query parameters.