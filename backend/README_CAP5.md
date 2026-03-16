# Cấp 5 - Authentication + User Separation

## ✅ Hoàn thành Cấp 5 - JWT Auth + User Isolation

### Những gì đã làm

#### 1. **User Management**
- ✅ Bảng `users` với: id, email (unique), hashed_password, is_active, created_at
- ✅ Bcrypt password hashing via passlib
- ✅ User registration & login endpoints

**Files:**
- `models/user.py` - SQLModel User table
- `schemas/user.py` - Pydantic User request/response schemas
- `repositories/user_repository.py` - User database queries
- `services/user_service.py` - Register, login, validation logic

#### 2. **JWT Authentication**
- ✅ OAuth2 Bearer token system
- ✅ Token generation & verification via python-jose
- ✅ Access tokens với expiration (default 30 minutes)
- ✅ Configurable SECRET_KEY & ALGORITHM

**Files:**
- `core/security.py` - Password hashing, JWT token creation/validation
- `core/config.py` - JWT settings (SECRET_KEY, ALGORITHM, EXPIRE_MINUTES)

#### 3. **Auth Endpoints - NEW**

**POST /api/v1/auth/register**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```
Response: User object + timestamps

**POST /api/v1/auth/login**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```
Response: JWT access token
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**GET /api/v1/auth/me**
- Header: `Authorization: Bearer <token>`
- Response: Current authenticated user

**File:** `routers/auth_router.py`

#### 4. **Todo User Separation**
- ✅ Todo model now includes `owner_id` FK → users.id
- ✅ Each user only sees/modifies their own todos
- ✅ Authorization check on every todo endpoint

**Changes:**
- `models/todo.py` - Added `owner_id: int = Field(foreign_key="users.id")`
- `schemas/todo.py` - Added `owner_id` to response
- `repositories/todo_repository.py` - Filter all queries by owner_id
- `services/todo_service.py` - Accept owner_id parameter
- `routers/todo_router.py` - Extract user_id from Authorization header

**File:** `routers/todo_router.py`

#### 5. **Authorization Checks**
- ✅ All todo endpoints require `Authorization: Bearer <token>` header
- ✅ User can only access/modify their own todos
- ✅ 404 if accessing other user's todo (not 403, better security)
- ✅ Login required for all operations except /auth/register & /auth/login

**Implementation:**
```python
def get_current_user_id(authorization: str = Header(None)) -> int:
    # Parse "Bearer <token>" header
    # Decode JWT token
    # Return user_id from token payload
```

#### 6. **Database Migrations**
- ✅ Initial schema (001_initial.py) - todos table
- ✅ NEW: 002_add_users.py - users table + owner_id FK

**Files:**
- `alembic/versions/001_initial.py` - Initial todos table
- `alembic/versions/002_add_users.py` - NEW: users + owner_id

---

## 🚀 Setup & Run Cấp 5

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

New packages: `python-jose`, `passlib[bcrypt]`, `python-multipart`, `email-validator`

### 2. Update .env
```bash
cp .env.example .env
```

Generate secure SECRET_KEY (production):
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Update `.env`:
```
SECRET_KEY=<your-generated-key>
```

### 3. Run migrations
```bash
alembic upgrade head
```

Creates: `users` table + `owner_id` column on `todos`

### 4. Run server
```bash
uvicorn main:app --reload
```

---

## 🧪 Test Cấp 5

### Flow: Register → Login → Create Todo → Get Todos

#### Step 1: Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "mypassword123"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-03-16T10:00:00..."
}
```

#### Step 2: Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "mypassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save TOKEN for next requests**

#### Step 3: Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

#### Step 4: Create Todo (with auth)
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "Learn Authentication",
    "description": "Implement JWT",
    "is_done": false
  }'
```

Response includes `owner_id`:
```json
{
  "id": 1,
  "owner_id": 1,  # <-- User ID
  "title": "Learn Authentication",
  "description": "Implement JWT",
  "is_done": false,
  "created_at": "2026-03-16T10:00:00...",
  "updated_at": "2026-03-16T10:00:00..."
}
```

#### Step 5: List Todos (user only sees their own)
```bash
curl http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <TOKEN>"
```

Returns only todos created by the authenticated user

#### Test: Try accessing other user's todo
1. Register second user
2. With second user's token, try: `GET /todos/1` (created by first user)
3. Result: 404 "ToDo not found" (because owner_id doesn't match)

---

## 🔐 Security Features

✅ **Password Hashing**
- Bcrypt with salt, never store plaintext passwords

✅ **JWT Token**
- HS256 algorithm, configurable expiration (default 30 min)
- Token includes user_id in `sub` claim

✅ **Authorization**
- All todo endpoints require valid Bearer token
- User cannot access other user's todos (verified via owner_id)

✅ **Email Validation**
- Valid email format required
- Unique email per user

✅ **Error Handling**
- 401 Unauthorized - missing/invalid token
- 404 Not Found - todo not found (don't reveal other users)
- 400 Bad Request - duplicate email, weak password

---

## 📊 Database Schema - Updated

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME NOT NULL
);
```

### Todos Table (Updated)
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,  -- NEW: FK to users
    title VARCHAR(100) NOT NULL,
    description VARCHAR,
    is_done BOOLEAN DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

---

## 📁 New/Updated Files

### New
- `models/user.py` - User table
- `schemas/user.py` - User schemas + Token
- `repositories/user_repository.py` - User queries
- `services/user_service.py` - Auth logic
- `routers/auth_router.py` - Auth endpoints
- `core/security.py` - JWT + password hashing
- `alembic/versions/002_add_users.py` - Migration

### Updated
- `models/todo.py` - Added owner_id FK
- `schemas/todo.py` - Added owner_id
- `repositories/todo_repository.py` - Filter by owner_id
- `services/todo_service.py` - Accept owner_id
- `routers/todo_router.py` - JWT auth header, owner_id
- `routers/__init__.py` - Include auth router
- `core/config.py` - JWT settings
- `.env.example` - JWT config
- `requirements.txt` - New auth packages

---

## 🎯 Tiêu chí đạt Cấp 5

✅ User model & registration  
✅ JWT login endpoint  
✅ GET /auth/me endpoint  
✅ Todo gắn owner_id  
✅ User A không xem/xóa todo của User B  
✅ Password hash bằng passlib/bcrypt  
✅ Authorization check trên tất cả todo endpoints  
✅ Database migrations for users table  

---

## 💡 Advanced Tips

### Generate Secure SECRET_KEY (Production)
```python
import secrets
secrets.token_urlsafe(32)
```

### Change Token Expiration
Update `.env`:
```
ACCESS_TOKEN_EXPIRE_MINUTES=60  # Longer expiration
```

### Reset password (TODO)
Could add in Cấp 6: POST /auth/forgot-password, POST /auth/reset-password

### Role-based access (TODO)
Could add: admin, moderator, user roles in Cấp 6+

### Email verification (TODO)
Could add: send verification link on registration

---

## 📚 File References

- **Security:** [core/security.py](core/security.py)
- **Auth Router:** [routers/auth_router.py](routers/auth_router.py)
- **Todo Router (updated):** [routers/todo_router.py](routers/todo_router.py)
- **Config:** [core/config.py](core/config.py)
- **Migration:** [alembic/versions/002_add_users.py](alembic/versions/002_add_users.py)

---

**Cấp 5 hoàn thành! 🎉 Đã có Authentication + User Isolation đầy đủ**

Sẵn sàng cho Cấp 6+ (Rate Limiting, Email Verification, Admin Panel, etc.)
