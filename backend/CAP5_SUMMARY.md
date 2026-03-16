# CAP 5 - AUTHENTICATION & USER SEPARATION - SUMMARY

## ✅ Hoàn thành Cấp 5

Đã triển khai **JWT Authentication** + **User Data Isolation** đầy đủ cho To-Do List API.

---

## 🔐 Authentication System

### Auth Flow
```
1. POST /auth/register → Create user account
                         ↓
2. POST /auth/login    → Verify email/password → Return JWT token
                         ↓
3. GET /auth/me        → Use token to get current user (requires Bearer token)
                         ↓
4. ALL /todos/*        → All todo operations require valid Bearer token
```

### Security Implementation
- **Password:** Bcrypt hashing via passlib (never stored plaintext)
- **Token:** JWT (HS256) with configurable expiration
- **Authorization:** Bearer token in Authorization header
- **Email:** Unique, validated email-validator

---

## 👥 User Model

**Bảng: `users`**
```python
id: int (PK)
email: str (UNIQUE)
hashed_password: str
is_active: bool = True
created_at: datetime (auto)
```

**Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Get JWT token
- `GET /auth/me` - Current authenticated user

---

## 📝 Todo User Separation

**Bảng: `todos` (Updated)**
```python
id: int (PK)
owner_id: int (FK → users.id)  # <-- NEW
title: str
description: str (optional)
is_done: bool
created_at: datetime (auto)
updated_at: datetime (auto)
```

### Authorization Rules
- ✅ User can see only their own todos
- ✅ User cannot create todos for other users
- ✅ Trying to access other user's todo → 404 (not 403, better privacy)
- ✅ All endpoints require valid Bearer token

**Example:***
- User A creates todo#1 (owner_id=1)
- User B tries GET /todos/1 with their token → 404
- User B's GET /todos → Returns only their todos

---

## 🛠️ Key Files

| File | Purpose |
|------|---------|
| `models/user.py` | SQLModel User table |
| `models/todo.py` | Updated with owner_id FK |
| `core/security.py` | JWT + password hashing (NEW) |
| `repositories/user_repository.py` | User DB queries (NEW) |
| `services/user_service.py` | Auth logic (NEW) |
| `routers/auth_router.py` | /auth endpoints (NEW) |
| `routers/todo_router.py` | Updated with auth header + owner_id filter |
| `alembic/versions/002_add_users.py` | Migration (NEW) |

---

## 🚀 Setup Steps

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Setup .env with SECRET_KEY
cp .env.example .env
# Generate: python -c "import secrets; print(secrets.token_hex(32))"

# 3. Run migrations
alembic upgrade head

# 4. Run server
uvicorn main:app --reload

# 5. Test
python test_cap5.py
```

---

## 🔑 JWT Token Format

Header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Payload (decoded):
```json
{
  "sub": 1,  // user_id
  "exp": 1626384000,  // expiration timestamp
  "iat": 1626380400   // issued at
}
```

---

## 📊 Database Changes

### New Migration: `002_add_users.py`
- Creates `users` table
- Adds `owner_id` column to `todos`
- Creates FK constraint: `todos.owner_id → users.id`
- Creates index on `users.email` (for login lookup)
- Creates index on `todos.owner_id` (for user query filtering)

Run:
```bash
alembic upgrade head
```

---

## ✨ Examples

### 1. Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"Pass123!"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"Pass123!"}'

# Response includes access_token
# Save: TOKEN=eyJhbGc...
```

### 3. Create Todo (with auth)
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Learn Cấp 5","description":"JWT auth"}'
```

### 4. List Own Todos
```bash
curl -X GET http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 Security Checklist

- ✅ Passwords hashed with bcrypt (not reversible)
- ✅ Tokens have expiration (default 30 min)
- ✅ SECRET_KEY configurable per environment
- ✅ Email validated format
- ✅ User A can't access User B's data (owner_id check)
- ✅ All todo routes require valid token
- ✅ Invalid token returns 401
- ✅ Foreign key constraint prevents orphaned todos

---

## 2️⃣ What's Different from Cấp 4?

| Feature | Cấp 4 | Cấp 5 |
|---------|-------|-------|
| Users | ❌ | ✅ Single user assumed → Per-user data |
| Auth | ❌ | ✅ JWT Bearer tokens |
| Todo ownership | ❌ | ✅ owner_id FK to users |
| User isolation | ❌ | ✅ Can't see other's todos |
| Password | ❌ | ✅ Bcrypt hashing |
| Login | ❌ | ✅ /auth/login endpoint |
| Token expiry | ❌ | ✅ Configurable expiration |

---

## 🎯 Tiêu chí đạt - Cấp 5

✅ Bảng users: id, email, hashed_password, is_active, created_at  
✅ JWT login: POST /auth/register, POST /auth/login, GET /auth/me  
✅ Todo gắn owner_id  
✅ User A không xem/xóa todo của User B  
✅ Password hash bằng passlib/bcrypt  
✅ Bearer token in Authorization header  
✅ Automatic user isolation on all todo operations  

---

## 📚 Test Files

- **test_cap5.py** - Full auth flow test (register → login → create → list)
- Run: `python test_cap5.py`

---

## NextSteps (Cấp 6+)

- Rate limiting (prevent brute force)
- Email verification
- Password reset flow
- Admin dashboard
- User roles & permissions
- Refresh tokens
- OAuth2 social login

---

**Cấp 5 Hoàn Thành! 🎉**

API giờ có **Authentication** + **Multi-User Support** đầy đủ.

Sẵn sàng cho Cấp 6 - Advanced Features!
