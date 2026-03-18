# CAP 6 - ADVANCED FEATURES & SMART FILTERING - SUMMARY

## ✅ Hoàn thành Cấp 6

Đã triển khai **Due Dates** + **Tags System** + **Smart Filtering** đầy đủ cho To-Do List API.

---

## 📅 Due Date System

### Features
```
1. Add due_date: Optional[datetime] to todo
2. Helper method: is_overdue() → due_date < now AND is_done=false
3. Helper method: is_due_today() → due_date.date() == today.date()
4. Smart filtering endpoints:
   - GET /todos/overdue → All overdue tasks
   - GET /todos/today → Tasks due today
```

### Use Cases
- Track deadlines
- Identify overdue tasks
- Daily task list
- Project management

---

## 🏷️ Tags System (Many-to-Many)

### Database Structure
```python
# tags table
id: int (PK)
owner_id: int (FK → users.id)
name: str
created_at: datetime (auto)
updated_at: datetime (auto)

# Priority: owner_id, name must be UNIQUE per user
# So User A can have tag "work", User B can have tag "work"

# todos_tags (junction table)
todo_id: int (FK → todos.id, ON DELETE CASCADE)
tag_id: int (FK → tags.id, ON DELETE CASCADE)
# Composite PK: (todo_id, tag_id)
```

### Features
- ✅ Many tags per todo
- ✅ Many todos per tag
- ✅ User-isolated (each user owns their tags)
- ✅ Automatic cascade delete
- ✅ Tags included in todo response

### Example
```
User 1 creates tags:
  - "work" (id=1)
  - "urgent" (id=2)
  - "report" (id=3)

User 1 creates todo with tag_ids=[1,2,3]

Response includes:
{
  "id": 1,
  "title": "...",
  "tags": [
    {"id": 1, "name": "work", ...},
    {"id": 2, "name": "urgent", ...},
    {"id": 3, "name": "report", ...}
  ]
}

User 2 cannot create tag with same name
&User 2's tags are completely separate
```

---

## 🔍 Smart Filtering Endpoints

### GET /todos/overdue
```
Query overdue/past-due tasks

Parameters:
  - q: Search by title/description (optional)
  - limit: Results per page (default 10, max 100)
  - offset: Pagination offset (default 0)

Response: ToDoListResponse {
  items: [overdue todos],
  total: count,
  limit: limit,
  offset: offset
}

Condition: due_date < now AND is_done=false
```

Example:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue?q=report&limit=5&offset=0
```

### GET /todos/today
```
Query tasks due today

Parameters:
  - q: Search by title/description (optional)
  - limit: Results per page (default 10, max 100)
  - offset: Pagination offset (default 0)

Response: ToDoListResponse {
  items: [today's todos],
  total: count,
  limit: limit,
  offset: offset
}

Condition: due_date.date() == today.date() AND is_done=false
```

Example:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/today
```

---

## 📝 Enhanced Todo Schema

### Request Body (POST /todos)
```json
{
  "title": "Finish Q1 report",
  "description": "Complete financial analysis",
  "is_done": false,
  "due_date": "2026-03-20T17:00:00Z",
  "tag_ids": [1, 2, 3]
}
```

### Response (GET /todos/{id})
```json
{
  "id": 1,
  "owner_id": 42,
  "title": "Finish Q1 report",
  "description": "Complete financial analysis",
  "is_done": false,
  "due_date": "2026-03-20T17:00:00Z",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:00Z",
  "tags": [
    {
      "id": 1,
      "name": "work",
      "owner_id": 42,
      "created_at": "2026-03-16T10:00:00Z"
    },
    {
      "id": 2,
      "name": "urgent",
      "owner_id": 42,
      "created_at": "2026-03-16T10:00:00Z"
    },
    {
      "id": 3,
      "name": "report",
      "owner_id": 42,
      "created_at": "2026-03-16T10:00:00Z"
    }
  ]
}
```

---

## 🛠️ Key Files

| File | Purpose | Status |
|------|---------|--------|
| `models/todo.py` | SQLModel: ToDoBase, ToDo, Tag, TodoTag | ✅ Updated |
| `models/user.py` | SQLModel: User | ✅ Unchanged |
| `schemas/todo.py` | Pydantic: TagSchema, ToDoBase/Create/Update/Patch | ✅ Updated |
| `schemas/user.py` | Pydantic: Auth schemas | ✅ Unchanged |
| `repositories/todo_repository.py` | Queries: list_all, list_overdue, list_today | ✅ Updated |
| `repositories/user_repository.py` | Queries: User operations | ✅ Unchanged |
| `services/todo_service.py` | Logic: list_overdue_todos, list_today_todos | ✅ Updated |
| `services/user_service.py` | Logic: Auth operations | ✅ Unchanged |
| `routers/todo_router.py` | Endpoints: GET /overdue, GET /today | ✅ Updated |
| `routers/auth_router.py` | Endpoints: /auth/* | ✅ Unchanged |
| `core/security.py` | JWT + Bcrypt | ✅ Unchanged |
| `core/config.py` | Environment settings | ✅ Unchanged |
| `core/database.py` | SQLAlchemy setup | ✅ Unchanged |
| `alembic/versions/003_add_due_date_and_tags.py` | Migration: due_date + tags | ✅ NEW |

---

## 🚀 Setup Steps

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Setup .env (if not done)
cp .env.example .env
# Generate SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"

# 3. Run migrations (applies 003_add_due_date_and_tags.py)
alembic upgrade head

# 4. Run server
uvicorn main:app --reload
```

---

## 🔐 Security & Isolation

✅ **Authentication:** All todo/tag endpoints require Bearer token (JWT)  
✅ **Data Isolation:** User A only sees User A's todos & tags  
✅ **Tag Ownership:** User A's tags completely separate from User B's  
✅ **Password Security:** Bcrypt hashing  
✅ **Token Expiry:** 30 minutes by default  

---

## 📊 Complete API Reference

### Todo Endpoints (ALL require `Authorization: Bearer <token>`)

| Method | Endpoint | New in Cấp 6? | Status |
|--------|----------|---------------|--------|
| GET | /todos | ❌ | List all (filter, search, sort, paginate) |
| GET | /todos/overdue | ✅ | List overdue (due_date < now) |
| GET | /todos/today | ✅ | List today (due_date.date() == today) |
| GET | /todos/{id} | ❌ | Get specific todo |
| POST | /todos | ⚡ | Create (now with due_date support) |
| PUT | /todos/{id} | ⚡ | Update (now with due_date support) |
| PATCH | /todos/{id} | ⚡ | Partial update (now with due_date support) |
| POST | /todos/{id}/complete | ❌ | Mark complete |
| DELETE | /todos/{id} | ❌ | Delete todo |

### Auth Endpoints (NO token required for register/login)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Get JWT token |
| GET | /auth/me | Get current user (requires token) |

---

## 🎯 Progression Summary

```
Cấp 1: CRUD +
Cấp 2: Filter/Search/Sort/Pagination +
Cấp 3: Layered Architecture +
Cấp 4: Database/ORM/Migrations +
Cấp 5: JWT Auth + User Isolation +
Cấp 6: Due Dates + Tags + Smart Filtering ← YOU ARE HERE
```

---

**Status:** ✅ **Production-Ready API with Advanced Features** 🚀
