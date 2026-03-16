# To-Do List API - Complete Guide (Cấp 1-5 Overview)

## 📚 Progression Overview

```
Cấp 1 ── Cấp 2 ── Cấp 3 ── Cấp 4 ── Cấp 5
CRUD   Filter  Layers   DB      Auth
```

---

## 🏗️ Architecture Summary

### Cấp 1: CRUD cơ bản (In-Memory)
- **Data:** Dictionary in RAM
- **Models:** Pydantic (ToDo)
- **Validation:** Pydantic field validators
- **Endpoints:** POST, GET, PUT, DELETE
- **Status:** ✅ Basic CRUD works

### Cấp 2: Validation + Filter/Sort/Pagination
- **Data:** Still in RAM
- **Additions:** 
  - Advanced validation (min_length, trim)
  - Filter (is_done), search (keyword), sort, pagination
  - Response format: {items, total, limit, offset}
  - Timestamps (created_at)
- **Status:** ✅ API features like production

### Cấp 3: Architecture + Settings
- **Structure:** Router → Service → Repository
- **Config:** pydantic-settings (env-based)
- **Prefix:** /api/v1 versioning
- **Routing:** APIRouter with clean main.py
- **Benefit:** Maintainable, testable code
- **Status:** ✅ Enterprise-like structure

### Cấp 4: Database + ORM
- **Database:** SQLite (default) or PostgreSQL
- **ORM:** SQLAlchemy + SQLModel
- **Schema:** Alembic migrations
- **Data Persistence:** Real database, survives restarts
- **New Field:** owner_id placeholder
- **Endpoints:** + PATCH (partial update), + /complete
- **Features:** Automatic timestamps, pagination from DB
- **Status:** ✅ Production-ready database layer

### Cấp 5: Authentication + Multi-User
- **Auth:** JWT Bearer tokens (python-jose)
- **Passwords:** Bcrypt hashing (passlib)
- **Users:** Separate user table with email login
- **Isolation:** User A can't see User B's todos
- **Endpoints:** /auth/register, /auth/login, /auth/me
- **Ownership:** Every todo links to owner_id
- **Status:** ✅ Multi-user system complete

---

## 🔄 Data Model Evolution

### Cấp 1-2: Simple ToDo
```python
{
  "id": 1,
  "title": "Task",
  "is_done": false,
  "created_at": "2026-03-16T10:00:00Z"
}
```

### Cấp 3-4: Enhanced ToDo
```python
{
  "id": 1,
  "title": "Task",
  "description": "Details",  # NEW in Cấp 4
  "is_done": false,
  "created_at": "2026-03-16T10:00:00Z",
  "updated_at": "2026-03-16T10:00:00Z"
}
```

### Cấp 5: Multi-User ToDo
```python
{
  "id": 1,
  "owner_id": 1,  # NEW - Links to user
  "title": "Task",
  "description": "Details",
  "is_done": false,
  "created_at": "2026-03-16T10:00:00Z",
  "updated_at": "2026-03-16T10:00:00Z"
}
```

### Cấp 5: New - User
```python
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-03-16T10:00:00Z"
}
```

---

## 📁 File Structure - Final (Cấp 5)

```
backend/
├── core/
│   ├── config.py           # Settings (env, db, jwt)
│   ├── database.py         # SQLAlchemy setup
│   └── security.py         # JWT + bcrypt (NEW Cấu 5)
│
├── models/
│   ├── todo.py             # SQLModel ToDo table
│   └── user.py             # SQLModel User table (NEW Cấp 5)
│
├── schemas/
│   ├── todo.py             # Pydantic ToDoCreate, ToDoUpdate, etc
│   └── user.py             # Pydantic User, Token (NEW Cấp 5)
│
├── repositories/
│   ├── todo_repository.py  # DB queries for ToDo
│   └── user_repository.py  # DB queries for User (NEW Cấp 5)
│
├── services/
│   ├── todo_service.py     # Business logic for ToDo
│   └── user_service.py     # Auth logic (NEW Cấp 5)
│
├── routers/
│   ├── __init__.py         # Router aggregator
│   ├── todo_router.py      # /todos endpoints
│   └── auth_router.py      # /auth endpoints (NEW Cấp 5)
│
├── alembic/
│   ├── env.py
│   ├── versions/
│   │   ├── 001_initial.py
│   │   └── 002_add_users.py (NEW Cấp 5)
│   └── script.py.mako
│
├── main.py                 # FastAPI app entry
├── alembic.ini
├── requirements.txt
├── .env.example
│
└── Documentation:
    ├── README_CAP4.md
    ├── README_CAP5.md      # (NEW)
    ├── CAP4_SUMMARY.md
    ├── CAP5_SUMMARY.md     # (NEW)
    ├── QUICK_START.md
    └── QUICK_START_CAP5.md # (NEW)
```

---

## 🔗 Endpoint Evolution

### Cấp 1
```
POST   /todos
GET    /todos
GET    /todos/{id}
PUT    /todos/{id}
DELETE /todos/{id}
```

### Cấp 2 (Same endpoints)
```
GET /todos?is_done=true&q=keyword&sort=-created_at&limit=10&offset=0
```

### Cấp 3 (Same as Cấp 2)
```
Prefix: /api/v1
All endpoints above
```

### Cấp 4 (New endpoints)
```
+ PATCH  /todos/{id}
+ POST   /todos/{id}/complete
```

### Cấp 5 (New auth + secured todos)
```
NEW:
+ POST   /auth/register
+ POST   /auth/login
+ GET    /auth/me

UPDATED (require Bearer token):
+ All /todos/* endpoints
  (filtered by owner_id, only see own todos)
```

---

## 🛡️ Security Evolution

| Feature | Cấp 1-3 | Cấp 4 | Cấp 5 |
|---------|---------|-------|-------|
| Authentication | ❌ | ❌ | ✅ |
| Authorization | ❌ | ❌ | ✅ |
| User Data Isolation | ❌ | ❌ | ✅ |
| Password Hashing | ❌ | ❌ | ✅ |
| Token Expiration | ❌ | ❌ | ✅ |

---

## 💾 Data Persistence Evolution

| Level | Cấp 1-3 | Cấp 4+ |
|-------|---------|--------|
| Storage | RAM (list/dict) | SQLite/PostgreSQL|
| Survival | Restart = Lost | Permanent |
| Scalability | Single dict | Full database |
| Querying | In-memory filter | SQL queries |
| Indexing | Manual | Automatic |

---

## 🚀 Running Final Version (Cấp 5)

### Setup
```bash
cd backend

# 1. Install
pip install -r requirements.txt

# 2. Environment
cp .env.example .env
# Edit .env: Set SECRET_KEY to random 32-char hex

# 3. Database
alembic upgrade head

# 4. Run
uvicorn main:app --reload
```

### Test
```bash
# Full test suite
python test_cap5.py

# Or manual
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

---

## 📊 Metrics

| Metric | Cấp 1 | Cấp 5 |
|--------|-------|-------|
| Files | 1 | ~20+ |
| Lines of Code | ~50 | ~1000+ |
| Database Tables | 0 | 2 |
| API Endpoints | 5 | 8+ |
| Auth Methods | 0 | JWT |
| Users Supported | 1 | Many |
| Data Persistence | No | Yes |

---

## 🎓 Concepts Learned

### Cấp 1-2
- Pydantic validation
- Response schemas
- Query parameters

### Cấp 3
- Layered architecture
- Repository pattern
- Service layer
- Environment config

### Cấp 4
- SQLAlchemy ORM
- Database migrations (Alembic)
- Foreign keys
- Pagination from DB

### Cấp 5
- JWT authentication
- Password hashing
- Bearer tokens
- Multi-user authorization

---

## 🔍 Recommended Reading Order

1. [README_CAP5.md](README_CAP5.md) - Full Cấp 5 docs
2. [CAP5_SUMMARY.md](CAP5_SUMMARY.md) - Quick summary
3. [routers/auth_router.py](routers/auth_router.py) - Auth endpoints
4. [routers/todo_router.py](routers/todo_router.py) - Updated todo endpoints
5. [test_cap5.py](test_cap5.py) - Working examples

---

## 💡 Next Steps (Future Cấp)

### Cấp 6: Advanced Features
- Rate limiting
- Email verification
- Password reset
- Admin panel
- User roles

### Cấp 7: Frontend
- React/Vue frontend
- Auth UI (login form)
- Todo CRUD UI

### Cấp 8: Deployment
- Docker containerization
- CI/CD pipeline
- Environment-specific configs

---

## ✨ Key Takeaways

- **Modularity:** Each cấp builds on previous, no breaking changes
- **Scalability:** From simple CRUD to multi-user system
- **Architecture:** Clean separation of concerns (3-layer pattern)
- **Database:** Production-grade persistence
- **Security:** JWT + bcrypt + user isolation
- **Documentation:** Comprehensive guides at each step

---

## 📞 Quick Reference

**Current API Base:** `http://localhost:8000/api/v1`  
**Docs (Swagger):** `http://localhost:8000/docs`  
**Current Version:** Cấp 5 (Complete with Auth)  
**Database:** SQLite (test.db) by default  
**Python:** 3.13+

---

**Status: ✅ Complete & Production-Ready (Cấp 5)**

From zero to multi-user auth system! 🎉

---

*For detailed implementation, see corresponding README_CAP#.md files*
