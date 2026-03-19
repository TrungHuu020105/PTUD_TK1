# Quick Start - Cấp 7 (Testing + Docker + Deployment)

## 🚀 Chạy Cấp 7 trong 5 phút

### Option 1: Local Development

**Step 1: Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2: Database**
```bash
cp .env.example .env
alembic upgrade head
```

**Step 3: Run**
```bash
uvicorn main:app --reload
```

✅ API: `http://localhost:8000/api/v1`

---

### Option 2: Docker (SQLite)

**1 command:**
```bash
docker build -t todolist-api . && \
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./test.db" \
  -e SECRET_KEY="dev-secret-key" \
  todolist-api
```

✅ API: `http://localhost:8000/api/v1`

---

### Option 3: Docker Compose (PostgreSQL)

**Setup:**
```bash
cp .env.example .env
docker-compose up -d
```

**Services:**
- API: `http://localhost:8000/api/v1`
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050` (admin/admin)

**Stop:**
```bash
docker-compose down -v
```

---

## 🧪 Run Tests

```bash
# All tests
pytest test_app.py -v

# Coverage report
pytest test_app.py --cov

# Specific test class
pytest test_app.py::TestAuth -v
```

**38+ tests covering:**
- ✅ Auth (register, login, me, errors)
- ✅ Todo CRUD (create, read, update, delete)
- ✅ Validation (422, title length)
- ✅ Auth errors (401, missing token)
- ✅ Not found (404)
- ✅ Cấp 6 features (overdue, today)
- ✅ User isolation

---

## 🧪 Quick Test (5 commands)

**1. Register**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

**2. Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

export TOKEN="<access_token_from_response>"
```

**3. Create Todo**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","due_date":"2026-03-22T17:00:00Z"}'
```

**4. List Todos**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos
```

**5. Check Overdue**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue
```

---

## 📁 New Files (Cấp 7)

```
test_app.py            # 38+ pytest tests
Dockerfile             # Multi-stage build
docker-compose.yml     # SQLite + PostgreSQL
.dockerignore          # Build optimization
README_DEPLOY.md       # This deployment guide
CAP7_SUMMARY.md        # Technical summary
COMPLETE_GUIDE.md      # Full overview (Cấp 1-7)
```

---

## 🏗️ Architecture

```
Dockerfile (multi-stage)
    ↓
Image: 200-300 MB
    ↓
docker run / docker-compose
    ↓
Services:
  - API (FastAPI) + health check
  - PostgreSQL (optional) + health check
  - pgAdmin (optional, debug profile)
    ↓
API: /api/v1
  - /auth/* (register, login, me)
  - /todos/* (CRUD + overdue + today)
  - /health (health check)
  - /docs (Swagger UI)
```

---

## ✅ Checklist

- [ ] Tests pass: `pytest test_app.py -v`
- [ ] Docker builds: `docker build -t todolist-api .`
- [ ] API runs: `docker run -p 8000:8000 todolist-api`
- [ ] curl commands work
- [ ] Auth flow complete (register → login → auth header)
- [ ] Todo CRUD works
- [ ] Cấp 6 endpoints work (/overdue, /today)

---

## 📚 Learn More

- [README_DEPLOY.md](README_DEPLOY.md) - Full deployment guide
- [CAP7_SUMMARY.md](CAP7_SUMMARY.md) - Technical details
- [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Full overview (Cấp 1-7)
- [CAP6_SUMMARY.md](CAP6_SUMMARY.md) - Cấp 6 features
- [README_CAP6.md](README_CAP6.md) - Complete Cấp 6 docs

---

## 🎉 Status

✅ **Production-Ready API - Complete & Tested** 🚀

All 7 Cấps implemented:
- ✅ Cấp 1: CRUD
- ✅ Cấp 2: Filtering
- ✅ Cấp 3: Layers
- ✅ Cấp 4: Database
- ✅ Cấp 5: Auth
- ✅ Cấp 6: Advanced
- ✅ Cấp 7: Testing + Docker ← YOU ARE HERE

Ready for: **Development → Testing → Production Deployment** 🚀
