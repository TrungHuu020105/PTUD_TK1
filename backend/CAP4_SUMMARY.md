# Cấp 4 - Database Integration Summary

## ✅ Hoàn thành toàn bộ Cấp 4

### Những gì đã làm

#### 1. **Database Layer**
- ✅ SQLModel cho type-safe ORM và Pydantic schema reuse
- ✅ SQLAlchemy ORMsession management
- ✅ SQLite mặc định (dễ switch sang PostgreSQL)
- ✅ Database connection pooling với `SessionLocal`

**File:**
- `core/database.py` - Engine, SessionLocal, get_session dependency

#### 2. **Models & Schema**
- ✅ SQLModel table `todos` với fields:
  - `id` (Integer, Primary Key)
  - `title` (String 3-100, indexed)
  - `description` (String, optional)
  - `is_done` (Boolean, default False)
  - `created_at` (DateTime, auto)
  - `updated_at` (DateTime, auto)
- ✅ Pydantic schemas cho request/response
- ✅ Riêng biệt `ToDoCreate`, `ToDoUpdate`, `ToDoPatch` schemas

**Files:**
- `models/todo.py` - SQLModel table định nghĩa
- `schemas/todo.py` - Pydantic request/response models

#### 3. **Repository Pattern**
- ✅ `ToDoRepository` với database queries từ thực DB
- ✅ List với filtering, searching, sorting, và pagination từ DB
- ✅ Tự động update `updated_at` khi sửa
- ✅ Xử lý commit/refresh đúng cách

**File:** `repositories/todo_repository.py`

#### 4. **Service Layer**
- ✅ Business logic tách biệt khỏi endpoints
- ✅ Dependency injection pattern cho repository
- ✅ `patch_todo()` - cập nhật từng phần (tùy chọn các field)
- ✅ `complete_todo()` - đánh dấu hoàn thành

**File:** `services/todo_service.py`

#### 5. **API Endpoints - Mới & Nâng cấp**

**Endpoints cũ (nâng cấp sang DB):**
- `POST /todos` - Tạo todo mới
- `GET /todos` - Danh sách với filter/search/sort/pagination từ DB
- `GET /todos/{id}` - Chi tiết todo
- `PUT /todos/{id}` - Cập nhật toàn bộ
- `DELETE /todos/{id}` - Xóa

**Endpoints MỚI - Cấp 4:**
- ✅ `PATCH /todos/{id}` - **Cập nhật một phần** (partial update)
  - Ví dụ: `{"is_done": true}` - chỉ update `is_done`, không cần fields khác
  - Ví dụ: `{"description": "..."}` - chỉ update description
  
- ✅ `POST /todos/{id}/complete` - **Đánh dấu hoàn thành**
  - Auto set `is_done=true` và cập nhật `updated_at`

**File:** `routers/todo_router.py`

#### 6. **Migrations - Alembic**
- ✅ Alembic setup với SQLAlchemy dialect
- ✅ `alembic/env.py` - lấy config từ `core.config`
- ✅ Initial migration `001_initial.py` tạo bảng todos
- ✅ Có thể tạo migrations mới dễ dàng khi thay đổi schema

**Files:**
- `alembic.ini` - Alembic config
- `alembic/env.py` - Migration environment
- `alembic/versions/001_initial.py` - Initial schema

#### 7. **Timestamps tự động**
- ✅ `created_at` tự set khi tạo (via `datetime.now(timezone.utc)`)
- ✅ `updated_at` tự set khi tạo, rồi update mỗi khi sửa (via `update_timestamp()`)
- ✅ Không cần client gửi timestamps

#### 8. **Configuration**
- ✅ `DATABASE_URL` từ `.env` (mặc định SQLite)
- ✅ Support PostgreSQL, MySQL, ... bằng cách thay `DATABASE_URL`
- ✅ `.env.example` mẫu cho mới user

**File:** `core/config.py`

---

## 📝 Cách chạy Cấp 4

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup .env (nếu cần)
```bash
cp .env.example .env
# Edit .env nếu cần thay DATABASE_URL
```

### 3. Run migrations
```bash
alembic upgrade head
```

### 4. Run app
```bash
uvicorn main:app --reload
```

API công khai tại: `http://localhost:8000/api/v1`
Docs: `http://localhost:8000/docs`

---

## 🧪 Test Endpoints

### Dùng Python script
```bash
python test_api.py
```

### Dùng shell script (Unix/Mac/Git Bash)
```bash
bash test_api.sh
```

### Dùng curl
```bash
# Create
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học API","description":"Chi tiết"}'

# PATCH (NEW) - chỉ update is_done
curl -X PATCH http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"is_done":true}'

# Complete (NEW)
curl -X POST http://localhost:8000/api/v1/todos/1/complete

# List với filter
curl "http://localhost:8000/api/v1/todos?is_done=true&q=Học&sort=-created_at&limit=10&offset=0"
```

---

## 🏗️ Architecture Cấp 4

```
backend/
│
├── core/
│   ├── __init__.py
│   ├── config.py                 # Cấu hình từ .env
│   └── database.py               # SQLAlchemy engine, SessionLocal
│
├── models/
│   ├── __init__.py
│   └── todo.py                   # SQLModel table (database schema)
│
├── schemas/
│   ├── __init__.py
│   └── todo.py                   # Pydantic models (request/response)
│
├── repositories/
│   ├── __init__.py
│   └── todo_repository.py        # Database access (SELECT, INSERT, UPDATE, DELETE)
│
├── services/
│   ├── __init__.py
│   └── todo_service.py           # Business logic (list, create, patch, complete)
│
├── routers/
│   ├── __init__.py
│   └── todo_router.py            # API endpoints (Depends(get_session))
│
├── alembic/
│   ├── env.py                    # Migration environment
│   ├── script.py.mako            # Migration template
│   └── versions/
│       ├── __init__.py
│       └── 001_initial.py        # Initial migration (create todos table)
│
├── main.py                       # FastAPI app, create_db_and_tables()
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Dependencies
├── .env.example                  # Environment mẫu
├── README_CAP4.md                # Hướng dẫn chi tiết
├── test_api.py                   # Python test script
├── test_api.sh                   # Shell test script
└── test.db                       # SQLite database (generated)
```

---

## 📊 Database Schema

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR,
    is_done BOOLEAN DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX ix_todos_title ON todos(title);
```

---

## 🎯 Chức năng mới Cấp 4 vs Cấp 3

| Tính năng | Cấp 3 | Cấp 4 |
|---|---|---|
| Dữ liệu | RAM (mất khi restart) | Dự lưu DB (SQLite) |
| Schema | Không có | SQLModel + Migrations |
| Timestamps | Tính toán RAM | Tự động từ DB |
| Pagination | Từ memory | Thực từ DB query |
| PATCH endpoint | ❌ | ✅ |
| Complete endpoint | ❌ | ✅ |
| Description field | ❌ | ✅ |
| Migrations | ❌ | Alembic ✅ |
| ORM | ❌ | SQLAlchemy + SQLModel ✅ |

---

## 💡 Tips

1. **Switch database:** Đổi `DATABASE_URL` trong `.env`:
   ```
   # PostgreSQL
   DATABASE_URL=postgresql://user:pass@localhost/todolist
   
   # MySQL
   DATABASE_URL=mysql+pymysql://user:pass@localhost/todolist
   ```

2. **Tạo migration mới:** Khi thay đổi model
   ```bash
   alembic revision --autogenerate -m "Mô tả thay đổi"
   alembic upgrade head
   ```

3. **Rollback migration:** Quay lại phiên bản trước
   ```bash
   alembic downgrade -1  # quay lại 1 bước
   ```

4. **Reset database:** Xóa hết dữ liệu
   - Xóa file `.db` (SQLite)
   - Rồi chạy `alembic upgrade head` lại

5. **Debug SQL:** Set `DEBUG=true` trong `.env` để thấy queries

---

## 📚 Files quan trọng

- `models/todo.py` - Xem schema table
- `repositories/todo_repository.py` - Xem cách query database
- `services/todo_service.py` - Xem business logic (PATCH, complete)
- `routers/todo_router.py` - Xem  API endpoints
- `test_api.py` hoặc `test_api.sh` - Chạy test

---

## ✨ Tiêu chí đạt Cấp 4

✅ Dùng SQLAlchemy & SQLModel  
✅ Bảng todos đủ fields (id, title, description, is_done, created_at, updated_at)  
✅ Migration bằng Alembic  
✅ PATCH endpoint cập nhật một phần  
✅ Complete endpoint đánh dấu hoàn thành  
✅ Timestamps tự cập nhật  
✅ Pagination thực từ DB query  

---

**Cấp 4 hoàn thành! Sẵn sàng cho Cấp 5 + Auth, hoặc Cấp 6 + Advanced Features 😎**
