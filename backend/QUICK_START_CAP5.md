# Quick Start - Cấp 5 Authentication

## 🚀 Chạy Cấp 5 trong 3 bước

### Step 1: Install new dependencies
```bash
cd backend
pip install -r requirements.txt
```
New: `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `email-validator`

### Step 2: Setup environment & migrate
```bash
# Copy .env template
cp .env.example .env

# Run migrations (creates users table + owner_id on todos)
alembic upgrade head
```

### Step 3: Run server
```bash
uvicorn main:app --reload
```

✅ API sẵn sàng: `http://localhost:8000/api/v1`

---

## 🧪 Quick Test

### Full test script
```bash
python test_cap5.py
```

### Manual test (3 commands)

**1. Register user**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

**2. Login & get token**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Copy "access_token" from response
export TOKEN="<paste-token-here>"
```

**3. Create todo with auth**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"My Task","description":"Testing auth"}'
```

---

## 📌 Key Features - Cấp 5

✅ User registration & login  
✅ JWT Bearer token auth  
✅ Each user sees only their todos  
✅ Password hashing with bcrypt  
✅ User cannot access other user's data  

---

## 📖 Learn More

- [README_CAP5.md](README_CAP5.md) - Full documentation
- [routers/auth_router.py](routers/auth_router.py) - Auth endpoints
- [routers/todo_router.py](routers/todo_router.py) - Updated with auth
- [core/security.py](core/security.py) - JWT & password logic

---

**Next: Test with `python test_cap5.py` 🎉**
