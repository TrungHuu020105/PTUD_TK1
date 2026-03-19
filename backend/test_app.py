"""
Test suite for To-Do List API - Cấp 7 Testing Complete

Tests using pytest + FastAPI TestClient
Covers: Auth, Todo CRUD, Validation, Error cases, Cấp 6 features
"""

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from main import app
from core.database import get_session
from models.todo import ToDo
from models.user import User


# === DB SETUP ===
@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory SQLite database for tests"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """FastAPI TestClient with test database"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# === FIXTURES: TEST DATA ===
@pytest.fixture
def test_user_data():
    """Reusable user registration data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
    }


@pytest.fixture
def test_user_2_data():
    """Second user for isolation tests"""
    return {
        "email": "user2@example.com",
        "password": "Password456!",
    }


@pytest.fixture
def auth_headers(client: TestClient, test_user_data):
    """Register user and return Authorization headers"""
    # Register
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = client.post("/api/v1/auth/login", json=test_user_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_user_2(client: TestClient, test_user_2_data):
    """Second user headers for isolation tests"""
    client.post("/api/v1/auth/register", json=test_user_2_data)
    response = client.post("/api/v1/auth/login", json=test_user_2_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================================
# TESTS: AUTH ENDPOINTS
# ============================================

class TestAuth:
    """Auth endpoint tests (register, login, me)"""

    def test_register_success(self, client: TestClient, test_user_data):
        """POST /auth/register - Success"""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_register_duplicate_email(self, client: TestClient, test_user_data):
        """POST /auth/register - Duplicate email fails"""
        # Register first user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try register with same email
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 400

    def test_register_invalid_email(self, client: TestClient):
        """POST /auth/register - Invalid email format"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert response.status_code == 422  # Validation error

    def test_login_success(self, client: TestClient, test_user_data):
        """POST /auth/login - Success returns token"""
        # Register
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        response = client.post("/api/v1/auth/login", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user_data):
        """POST /auth/login - Wrong password fails"""
        # Register
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": "WrongPassword123!",
            },
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """POST /auth/login - Nonexistent user fails"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        assert response.status_code == 401

    def test_get_current_user(self, client: TestClient, auth_headers, test_user_data):
        """GET /auth/me - Returns current user"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["is_active"] is True

    def test_get_current_user_no_auth(self, client: TestClient):
        """GET /auth/me - No token fails"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """GET /auth/me - Invalid token fails"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_123"},
        )
        assert response.status_code == 401


# ============================================
# TESTS: TODO ENDPOINTS - CREATE
# ============================================

class TestTodoCreate:
    """Todo creation tests"""

    def test_create_todo_success(self, client: TestClient, auth_headers):
        """POST /todos - Create todo successfully"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Complete project",
                "description": "Finish the Q1 project",
                "is_done": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["description"] == "Finish the Q1 project"
        assert data["is_done"] is False
        assert "id" in data
        assert "owner_id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert "tags" in data

    def test_create_todo_with_due_date(self, client: TestClient, auth_headers):
        """POST /todos - Create todo with due_date (Cấp 6)"""
        future_date = datetime.now(timezone.utc) + timedelta(days=5)
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Future task",
                "due_date": future_date.isoformat(),
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "due_date" in data
        assert data["due_date"] is not None

    def test_create_todo_title_too_short(self, client: TestClient, auth_headers):
        """POST /todos - Title too short (validation fail)"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "ab"},  # < 3 chars
        )
        assert response.status_code == 422

    def test_create_todo_title_too_long(self, client: TestClient, auth_headers):
        """POST /todos - Title too long (validation fail)"""
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "a" * 101},  # > 100 chars
        )
        assert response.status_code == 422

    def test_create_todo_no_auth(self, client: TestClient):
        """POST /todos - No auth header fails"""
        response = client.post(
            "/api/v1/todos",
            json={"title": "Task without auth"},
        )
        assert response.status_code == 401


# ============================================
# TESTS: TODO ENDPOINTS - READ
# ============================================

class TestTodoRead:
    """Todo retrieval tests"""

    def test_list_todos(self, client: TestClient, auth_headers):
        """GET /todos - List all todos"""
        # Create 3 todos
        for i in range(3):
            client.post(
                "/api/v1/todos",
                headers=auth_headers,
                json={"title": f"Task {i}"},
            )
        
        # List todos
        response = client.get("/api/v1/todos", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3
        assert "limit" in data
        assert "offset" in data

    def test_list_todos_pagination(self, client: TestClient, auth_headers):
        """GET /todos - Pagination works"""
        # Create 5 todos
        for i in range(5):
            client.post(
                "/api/v1/todos",
                headers=auth_headers,
                json={"title": f"Task {i}"},
            )
        
        # List with limit=2
        response = client.get(
            "/api/v1/todos?limit=2&offset=0",
            headers=auth_headers,
        )
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["limit"] == 2
        assert data["offset"] == 0

    def test_list_todos_filter_is_done(self, client: TestClient, auth_headers):
        """GET /todos - Filter by is_done"""
        # Create 2 todos
        client.post("/api/v1/todos", headers=auth_headers, json={"title": "Task 1"})
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task 2", "is_done": True},
        )
        todo_id = response.json()["id"]
        
        # Mark one as done
        client.patch(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={"is_done": True},
        )
        
        # Filter for completed
        response = client.get(
            "/api/v1/todos?is_done=true",
            headers=auth_headers,
        )
        data = response.json()
        assert len(data["items"]) >= 1

    def test_list_todos_search(self, client: TestClient, auth_headers):
        """GET /todos - Search by keyword"""
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Important project", "description": "Urgent work"},
        )
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Random task"},
        )
        
        # Search for "Important"
        response = client.get(
            "/api/v1/todos?q=Important",
            headers=auth_headers,
        )
        data = response.json()
        assert data["total"] >= 1
        assert "Important" in data["items"][0]["title"]

    def test_get_todo_by_id(self, client: TestClient, auth_headers):
        """GET /todos/{id} - Get specific todo"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "My task"},
        )
        todo_id = create_response.json()["id"]
        
        # Get
        response = client.get(f"/api/v1/todos/{todo_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "My task"

    def test_get_todo_404(self, client: TestClient, auth_headers):
        """GET /todos/{id} - Nonexistent todo returns 404"""
        response = client.get("/api/v1/todos/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_get_todo_no_auth(self, client: TestClient):
        """GET /todos/{id} - No auth fails"""
        response = client.get("/api/v1/todos/1")
        assert response.status_code == 401

    def test_get_other_user_todo_404(self, client: TestClient, auth_headers, auth_headers_user_2):
        """GET /todos/{id} - User cannot access other user's todo (returns 404 for privacy)"""
        # User 1 creates todo
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "User 1 task"},
        )
        todo_id = create_response.json()["id"]
        
        # User 2 tries to get it
        response = client.get(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers_user_2,
        )
        assert response.status_code == 404


# ============================================
# TESTS: TODO ENDPOINTS - UPDATE
# ============================================

class TestTodoUpdate:
    """Todo update/patch/complete tests"""

    def test_update_todo_full(self, client: TestClient, auth_headers):
        """PUT /todos/{id} - Full update"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Original task"},
        )
        todo_id = create_response.json()["id"]
        
        # Update
        response = client.put(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={
                "title": "Updated task",
                "description": "New description",
                "is_done": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated task"
        assert data["description"] == "New description"
        assert data["is_done"] is True

    def test_update_todo_with_due_date(self, client: TestClient, auth_headers):
        """PUT /todos/{id} - Update with due_date"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task"},
        )
        todo_id = create_response.json()["id"]
        
        # Update
        future_date = datetime.now(timezone.utc) + timedelta(days=7)
        response = client.put(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={
                "title": "Task with deadline",
                "is_done": False,
                "due_date": future_date.isoformat(),
            },
        )
        assert response.status_code == 200

    def test_patch_todo_partial(self, client: TestClient, auth_headers):
        """PATCH /todos/{id} - Partial update"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task", "description": "Original"},
        )
        todo_id = create_response.json()["id"]
        
        # Patch only title
        response = client.patch(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={"title": "Modified title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Modified title"
        assert data["description"] == "Original"  # Unchanged

    def test_patch_todo_mark_complete(self, client: TestClient, auth_headers):
        """PATCH /todos/{id} - Mark as complete"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task"},
        )
        todo_id = create_response.json()["id"]
        
        # Patch to mark done
        response = client.patch(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={"is_done": True},
        )
        assert response.status_code == 200
        assert response.json()["is_done"] is True

    def test_complete_todo_endpoint(self, client: TestClient, auth_headers):
        """POST /todos/{id}/complete - Mark complete via endpoint"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task"},
        )
        todo_id = create_response.json()["id"]
        
        # Complete
        response = client.post(
            f"/api/v1/todos/{todo_id}/complete",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["is_done"] is True

    def test_update_todo_404(self, client: TestClient, auth_headers):
        """PUT /todos/{id} - Update nonexistent todo"""
        response = client.put(
            "/api/v1/todos/9999",
            headers=auth_headers,
            json={"title": "New title", "is_done": False},
        )
        assert response.status_code == 404

    def test_patch_todo_validation_fail(self, client: TestClient, auth_headers):
        """PATCH /todos/{id} - Invalid data fails"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task"},
        )
        todo_id = create_response.json()["id"]
        
        # Patch with invalid title (too short)
        response = client.patch(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers,
            json={"title": "ab"},  # Too short
        )
        assert response.status_code == 422


# ============================================
# TESTS: TODO ENDPOINTS - DELETE
# ============================================

class TestTodoDelete:
    """Todo deletion tests"""

    def test_delete_todo_success(self, client: TestClient, auth_headers):
        """DELETE /todos/{id} - Delete successfully"""
        # Create
        create_response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Task to delete"},
        )
        todo_id = create_response.json()["id"]
        
        # Delete
        response = client.delete(f"/api/v1/todos/{todo_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify deleted
        get_response = client.get(f"/api/v1/todos/{todo_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_todo_404(self, client: TestClient, auth_headers):
        """DELETE /todos/{id} - Delete nonexistent todo"""
        response = client.delete("/api/v1/todos/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_todo_no_auth(self, client: TestClient):
        """DELETE /todos/{id} - No auth fails"""
        response = client.delete("/api/v1/todos/1")
        assert response.status_code == 401


# ============================================
# TESTS: CAP 6 FEATURES - SMART FILTERING
# ============================================

class TestCap6SmartFiltering:
    """Cấp 6: Due dates and smart filtering"""

    def test_get_overdue_todos(self, client: TestClient, auth_headers):
        """GET /todos/overdue - Get past-due todos"""
        # Create overdue todo
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Overdue task",
                "due_date": past_date.isoformat(),
                "is_done": False,
            },
        )
        
        # Create future todo (should not appear)
        future_date = datetime.now(timezone.utc) + timedelta(days=5)
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Future task",
                "due_date": future_date.isoformat(),
                "is_done": False,
            },
        )
        
        # Get overdue
        response = client.get("/api/v1/todos/overdue", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        # All should have due_date in past
        for todo in data["items"]:
            assert todo["is_done"] is False

    def test_get_today_todos(self, client: TestClient, auth_headers):
        """GET /todos/today - Get todos due today"""
        # Create today todo
        today = datetime.now(timezone.utc)
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Today task",
                "due_date": today.isoformat(),
                "is_done": False,
            },
        )
        
        # Create tomorrow todo (should not appear)
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Tomorrow task",
                "due_date": tomorrow.isoformat(),
                "is_done": False,
            },
        )
        
        # Get today
        response = client.get("/api/v1/todos/today", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # Should have at least the today task
        assert len(data["items"]) >= 1

    def test_overdue_pagination(self, client: TestClient, auth_headers):
        """GET /todos/overdue - Pagination works"""
        # Create multiple overdue todos
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        for i in range(5):
            client.post(
                "/api/v1/todos",
                headers=auth_headers,
                json={
                    "title": f"Overdue {i}",
                    "due_date": past_date.isoformat(),
                    "is_done": False,
                },
            )
        
        # Get with limit=2
        response = client.get(
            "/api/v1/todos/overdue?limit=2&offset=0",
            headers=auth_headers,
        )
        data = response.json()
        assert len(data["items"]) <= 2
        assert data["limit"] == 2

    def test_today_search(self, client: TestClient, auth_headers):
        """GET /todos/today - Search works"""
        today = datetime.now(timezone.utc)
        client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "Important meeting today",
                "due_date": today.isoformat(),
                "is_done": False,
            },
        )
        
        # Search for "Important"
        response = client.get(
            "/api/v1/todos/today?q=Important",
            headers=auth_headers,
        )
        assert response.status_code == 200


# ============================================
# TESTS: USER ISOLATION
# ============================================

class TestUserIsolation:
    """Verify user data isolation (Cấp 5)"""

    def test_user_sees_only_own_todos(self, client: TestClient, auth_headers, auth_headers_user_2):
        """Two users have separate todo lists"""
        # User 1 creates 2 todos
        client.post("/api/v1/todos", headers=auth_headers, json={"title": "User 1 Task 1"})
        client.post("/api/v1/todos", headers=auth_headers, json={"title": "User 1 Task 2"})
        
        # User 2 creates 1 todo
        client.post("/api/v1/todos", headers=auth_headers_user_2, json={"title": "User 2 Task 1"})
        
        # User 1 lists todos
        response = client.get("/api/v1/todos", headers=auth_headers)
        data = response.json()
        assert data["total"] == 2
        
        # User 2 lists todos
        response = client.get("/api/v1/todos", headers=auth_headers_user_2)
        data = response.json()
        assert data["total"] == 1

    def test_user_cannot_modify_other_user_todo(self, client: TestClient, auth_headers, auth_headers_user_2):
        """User 2 cannot update User 1's todo"""
        # User 1 creates todo
        response = client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "User 1 Task"},
        )
        todo_id = response.json()["id"]
        
        # User 2 tries to update it
        response = client.put(
            f"/api/v1/todos/{todo_id}",
            headers=auth_headers_user_2,
            json={"title": "Changed by User 2", "is_done": False},
        )
        assert response.status_code == 404  # Privacy: return 404 not 403


# ============================================
# TESTS: HEALTH CHECKS
# ============================================

class TestHealth:
    """API health checks"""

    def test_health_endpoint(self, client: TestClient):
        """GET /health - Health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_root_endpoint(self, client: TestClient):
        """GET / - Root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
