# Cấp 6 - Advanced Features (Due Dates + Tags + Smart Filtering)

## ✅ Hoàn thành Cấp 6 - Due Dates, Tags & Deadline Tracking

### Những gì đã làm

#### 1. **Due Date Field**
- ✅ Thêm `due_date: Optional[datetime]` vào mô hình Todo
- ✅ So sánh ngày giờ để xác định công việc quá hạn
- ✅ Lọc theo ngày hôm nay
- ✅ Index trên `due_date` để query nhanh

**Files:**
- `models/todo.py` - Added `due_date` field with helper methods
- `schemas/todo.py` - Updated ToDo schemas to include `due_date`
- `repositories/todo_repository.py` - New query methods for date filtering

**Helper Methods:**
```python
todo.is_overdue()      # Check if due_date < now AND is_done=false
todo.is_due_today()    # Check if due_date.date() == today.date()
```

#### 2. **Tags System (Many-to-Many)**
- ✅ Bảng `tags` với owner isolation (user riêng có user riêng tags)
- ✅ Junction table `todos_tags` cho quan hệ many-to-many
- ✅ Mỗi user chỉ có thể tạo tags của mình
- ✅ Tags được include trong Todo response

**Database Schema:**
```python
# tags table
id: int (PK)
owner_id: int (FK → users.id)
name: str (UNIQUE per owner)
created_at: datetime (auto)
updated_at: datetime (auto)

# todos_tags junction table
todo_id: int (PK + FK → todos.id)
tag_id: int (PK + FK → tags.id)
```

**Files:**
- `models/todo.py` - Tag model + TodoTag junction table + Relationship
- `schemas/todo.py` - TagSchema cho serialization

#### 3. **Smart Filtering Endpoints**

**GET /api/v1/todos/overdue** - Danh sách công việc quá hạn
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue?limit=10&offset=0
```
Response: ToDoListResponse (quá hạn = due_date < now && is_done=false)

**GET /api/v1/todos/today** - Danh sách công việc hôm nay
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/today?limit=10&offset=0
```
Response: ToDoListResponse (hôm nay = due_date.date() == today.date() && is_done=false)

**Query Params (cả 2 endpoint):**
- `q`: Search by title/description
- `limit`: Pagination limit (default 10, max 100)
- `offset`: Pagination offset (default 0)

**Files:**
- `routers/todo_router.py` - NEW endpoints
- `services/todo_service.py` - NEW service methods
- `repositories/todo_repository.py` - NEW query methods

#### 4. **Enhanced Todo Schema**

**Request (Create/Update):**
```json
{
  "title": "Finish project report",
  "description": "Q1 report due Friday",
  "is_done": false,
  "due_date": "2026-03-20T17:00:00Z",
  "tag_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "id": 1,
  "owner_id": 1,
  "title": "Finish project report",
  "description": "Q1 report due Friday",
  "is_done": false,
  "due_date": "2026-03-20T17:00:00Z",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:00Z",
  "tags": [
    {"id": 1, "name": "work", "owner_id": 1, "created_at": "..."},
    {"id": 2, "name": "urgent", "owner_id": 1, "created_at": "..."},
    {"id": 3, "name": "report", "owner_id": 1, "created_at": "..."}
  ]
}
```

**Files:**
- `schemas/todo.py` - TagSchema + updated ToDo
- `schemas/user.py` - Unchanged from Cấp 5

#### 5. **Database Migrations**
- ✅ Migration 003_add_due_date_and_tags.py
  - Adds `due_date` column
  - Creates `tags` table
  - Creates `todos_tags` junction table
  - Adds indexes for performance

**Files:**
- `alembic/versions/003_add_due_date_and_tags.py` - NEW

---

## 🚀 Setup & Run Cấp 6

### 1. Dependencies (no new packages)
Already installed from Cấp 5:
```bash
pip install -r requirements.txt
```

### 2. Update .env (optional)
No new environment variables needed. Existing `.env` from Cấp 5 works.

### 3. Run migrations
```bash
alembic upgrade head
```

This will create: `due_date` column + `tags` table + `todos_tags` table

### 4. Run server
```bash
uvicorn main:app --reload
```

---

## 🧪 Test Cấp 6

### Complete Test Flow

#### Step 1: Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

#### Step 2: Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
# Save access_token
export TOKEN="<access_token_value>"
```

#### Step 3: Create Todo with Due Date
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Finish report",
    "description": "Q1 analysis",
    "due_date": "2026-03-15T17:00:00Z",
    "is_done": false
  }'
# Save todo id
export TODO_ID=1
```

#### Step 4: Get Overdue Todos (if due_date in past)
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue
```
Response: Todos with due_date < now && is_done=false

#### Step 5: Get Today's Todos
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/today
```
Response: Todos with due_date matching today

#### Step 6: Update Todo
```bash
curl -X PUT http://localhost:8000/api/v1/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Finish report - UPDATED",
    "due_date": "2026-03-22T17:00:00Z",
    "is_done": false
  }'
```

#### Step 7: Patch Todo (Partial Update)
```bash
curl -X PATCH http://localhost:8000/api/v1/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "due_date": "2026-03-25T10:00:00Z"
  }'
```

#### Step 8: Mark Complete
```bash
curl -X POST http://localhost:8000/api/v1/todos/$TODO_ID/complete \
  -H "Authorization: Bearer $TOKEN"
```

#### Step 9: List All Todos
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos?is_done=false
```

---

## 📌 Key Features - Cấp 6

✅ Due dates for todos  
✅ Check if todo is overdue (due_date < now)  
✅ Check if todo is due today  
✅ GET /todos/overdue - Smart filtering  
✅ GET /todos/today - Smart filtering  
✅ Tags system with many-to-many relationships  
✅ Each user has isolated tags  
✅ Tags included in todo responses  
✅ Full authentication inherited from Cấp 5  

---

## 📊 Database Schema (Complete)

```sql
-- From Cấp 4-5
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  is_active BOOLEAN DEFAULT 1,
  created_at DATETIME NOT NULL
);

CREATE TABLE todos (
  id INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  is_done BOOLEAN DEFAULT 0,
  due_date DATETIME,  -- NEW in Cấp 6
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- NEW in Cấp 6
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  UNIQUE(owner_id, name),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE todos_tags (
  todo_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY (todo_id, tag_id),
  FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

---

## 📖 API Endpoint Reference

### Todo Endpoints (All require Bearer token)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /todos | List all todos (filter by is_done, search, sort, paginate) |
| GET | /todos/overdue | List overdue todos |
| GET | /todos/today | List todos due today |
| GET | /todos/{id} | Get specific todo |
| POST | /todos | Create new todo |
| PUT | /todos/{id} | Full update |
| PATCH | /todos/{id} | Partial update |
| POST | /todos/{id}/complete | Mark as complete |
| DELETE | /todos/{id} | Delete todo |

### Auth Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login & get JWT token |
| GET | /auth/me | Get current user info |

---

## 🔐 Security Notes

- ✅ All todo endpoints require `Authorization: Bearer <token>`
- ✅ Users can only see/modify their own todos & tags
- ✅ Tags are user-isolated (User A's tags ≠ User B's tags)
- ✅ Passwords hashed with bcrypt
- ✅ JWTs expire after 30 minutes (configurable)

---

## 📝 Learning Resources

- [QUICK_START_CAP6.md](QUICK_START_CAP6.md) - Fast setup guide
- [CAP6_SUMMARY.md](CAP6_SUMMARY.md) - Feature summary
- [routers/todo_router.py](routers/todo_router.py) - Todo endpoints
- [routers/auth_router.py](routers/auth_router.py) - Auth endpoints
- [models/todo.py](models/todo.py) - Data models
- [core/security.py](core/security.py) - JWT & bcrypt

**Status:** ✅ Cấp 6 Ready - Full production API with advanced features 🎉
