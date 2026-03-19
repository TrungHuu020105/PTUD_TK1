# Cấp 7 - Testing, Documentation & Deployment

## 🧪 Testing Suite

### Install Test Dependencies
```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests
```bash
pytest test_app.py -v
```

### Run Specific Test Class
```bash
# Auth tests only
pytest test_app.py::TestAuth -v

# Todo creation tests
pytest test_app.py::TestTodoCreate -v

# Cấp 6 smart filtering tests
pytest test_app.py::TestCap6SmartFiltering -v
```

### Run with Coverage
```bash
pip install pytest-cov
pytest test_app.py --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 📋 Test Coverage

### Auth Tests (9 tests)
- ✅ Register successful
- ✅ Duplicate email validation
- ✅ Invalid email format
- ✅ Login successful
- ✅ Login wrong password
- ✅ Login nonexistent user
- ✅ Get current user
- ✅ Missing auth header (401)
- ✅ Invalid token (401)

### Todo CRUD Tests (20+ tests)
- ✅ Create with/without due_date
- ✅ Validation errors (title length)
- ✅ List with pagination/filter/search/sort
- ✅ Get single todo
- ✅ 404 on nonexistent
- ✅ Full update (PUT)
- ✅ Partial update (PATCH)
- ✅ Mark complete endpoint
- ✅ Delete todo
- ✅ Auth required (401)

### Cấp 6 Features (5 tests)
- ✅ GET /todos/overdue - past-due todos
- ✅ GET /todos/today - today's todos
- ✅ Overdue with pagination
- ✅ Today with search
- ✅ Completed todos not in overdue/today

### User Isolation (2 tests)
- ✅ Users see only their todos
- ✅ Users cannot modify other's todos

### Health Checks (2 tests)
- ✅ /health endpoint
- ✅ / root endpoint

**Total: 38+ integration tests covering all major flows**

---

## 🐳 Docker Deployment

### Option 1: SQLite (Development/Testing)

**Simple one-command setup:**
```bash
# Build image
docker build -t todolist-api:latest .

# Run with SQLite
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./test.db" \
  -e SECRET_KEY="your-secret-key-here" \
  todolist-api:latest
```

API available at: `http://localhost:8000/api/v1`

**Or use docker-compose:**
```bash
# Environment setup
cp .env.example .env
# Edit .env to set SECRET_KEY

# Run
docker-compose up app
```

---

### Option 2: PostgreSQL (Production)

**Full setup with docker-compose:**

```bash
# 1. Setup environment
cp .env.example .env

# 2. Edit .env
nano .env
# Update: SECRET_KEY, POSTGRES_PASSWORD (optional)

# 3. Start services
docker-compose up -d

# 4. Verify
curl http://localhost:8000/health
```

**Services running:**
- API: `http://localhost:8000/api/v1`
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050` (admin/admin)

**View logs:**
```bash
docker-compose logs -f app
docker-compose logs -f postgres
```

**Stop services:**
```bash
docker-compose down          # Keep database
docker-compose down -v       # Remove database volume
```

---

### Environment Variables

Create `.env` file:
```bash
# Database (SQLite by default)
DATABASE_URL=sqlite:///./test.db

# Or PostgreSQL
# DATABASE_URL=postgresql://user:password@postgres:5432/todolist_db

# JWT Configuration
SECRET_KEY=your-random-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
APP_NAME=To-Do List API
DEBUG=False
API_V1_PREFIX=/api/v1

# PostgreSQL (if using docker-compose)
POSTGRES_USER=todolist_user
POSTGRES_PASSWORD=todolist_password_123
```

**Generate secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Local Development Setup

### 1. Clone & Install
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Create .env
cp .env.example .env

# Run migrations
alembic upgrade head
```

### 3. Run Server
```bash
uvicorn main:app --reload
```

API: `http://localhost:8000/api/v1`
Docs: `http://localhost:8000/docs` (Swagger UI)
ReDoc: `http://localhost:8000/redoc`

### 4. Run Tests
```bash
pytest test_app.py -v
```

---

## 📮 API Testing

### Quick Test Flow (5 commands)

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

# Save token
export TOKEN="<access_token_from_response>"
```

**3. Create Todo**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Buy groceries",
    "description":"Milk, eggs, bread",
    "due_date":"2026-03-22T17:00:00Z"
  }'
```

**4. List Todos**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos?limit=10&offset=0
```

**5. Get Overdue (Cấp 6)**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue
```

---

## 🔧 Production Deployment

### AWS ECS / Google Cloud Run

**Key configurations:**
```dockerfile
# In Dockerfile:
- Multi-stage build (slim image)
- Non-root user (security)
- Health checks
- Auto-migrations on startup

# Environment variables:
- DATABASE_URL → Cloud SQL / RDS connection string
- SECRET_KEY → Use secrets manager
- DEBUG=False
```

**Example for AWS:**
```bash
# Build and push to ECR
docker build -t todolist-api:1.0 .
docker tag todolist-api:1.0 AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/todolist:1.0
docker push AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/todolist:1.0

# Create CloudFormation / Terraform for ECS/ALB
# Ensure health checks pass: http://APP:8000/health
# Set DATABASE_URL to RDS PostgreSQL endpoint
```

### Kubernetes

**Deploy:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Check status:**
```bash
kubectl get pods
kubectl logs -f pod/todolist-api-xxx
kubectl port-forward svc/todolist-api 8000:8000
```

---

## 📊 Project Structure (Final - Cấp 7)

```
backend/
├── core/
│   ├── config.py           # Environment settings
│   ├── database.py         # SQLAlchemy + SQLModel setup
│   └── security.py         # JWT + password hashing
│
├── models/
│   ├── todo.py             # ToDo + Tag + TodoTag SQLModel
│   └── user.py             # User SQLModel
│
├── schemas/
│   ├── todo.py             # Pydantic schemas + TagSchema
│   └── user.py             # User/Token Pydantic schemas
│
├── repositories/
│   ├── todo_repository.py  # Todo DB queries
│   └── user_repository.py  # User DB queries
│
├── services/
│   ├── todo_service.py     # Todo business logic
│   └── user_service.py     # Auth logic
│
├── routers/
│   ├── __init__.py
│   ├── todo_router.py      # /todos endpoints
│   └── auth_router.py      # /auth endpoints
│
├── alembic/                # Database migrations
│   └── versions/
│       ├── 001_initial.py
│       ├── 002_add_users.py
│       └── 003_add_due_date_and_tags.py
│
├── main.py                 # FastAPI app
├── test_app.py             # 38+ pytest integration tests (NEW - Cấp 7)
│
├── Dockerfile              # Multi-stage Docker build (NEW - Cấp 7)
├── docker-compose.yml      # SQLite + PostgreSQL setup (NEW - Cấp 7)
├── .dockerignore           # Docker build optimization
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── alembic.ini             # Alembic configuration
└── README_DEPLOY.md        # This file (NEW - Cấp 7)
```

---

## ✅ Deployment Checklist

- [ ] All tests pass: `pytest test_app.py -v`
- [ ] `.env.secret` created with strong SECRET_KEY
- [ ] DATABASE_URL points to production database
- [ ] DEBUG=False in production
- [ ] Health checks configured: `/health`
- [ ] Migrations run before app starts
- [ ] Docker image built and tested locally
- [ ] Environment variables set in deployment platform
- [ ] Database backups configured
- [ ] Logging configured (consider ELK/CloudWatch)
- [ ] Rate limiting configured (if needed)
- [ ] CORS configured appropriately
- [ ] API documentation accessible at `/docs`

---

## 🚨 Troubleshooting

### Database connection error
```
Error: could not translate host name to address

# Fix: Ensure DATABASE_URL is correct
# Docker: Use service name "postgres" (not localhost)
# Local: Use "sqlite:///./test.db" or PostgreSQL connection string
```

### Tests fail with "AttributeError: no attribute 'metadata'"
```
# Fix: Ensure models are imported in main.py
from models.todo import ToDo  # noqa
from models.user import User  # noqa
```

### Docker build fails: "E: Could not get lock"
```
# Fix: Race condition. Try again or use:
docker-compose build --no-cache
```

### 401 Unauthorized on protected endpoints
```
# Check token format:
# Header: Authorization: Bearer <token>
# Not: Authorization: <token>
# Generate new token with POST /auth/login
```

---

## 📚 Documentation Files

- [README_CAP6.md](README_CAP6.md) - Cấp 6 features (due_date, tags, smart filtering)
- [QUICK_START_CAP6.md](QUICK_START_CAP6.md) - Quick setup guide
- [CAP6_SUMMARY.md](CAP6_SUMMARY.md) - Technical summary
- [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Cấp 1-6 progression overview
- [README_DEPLOY.md](README_DEPLOY.md) - This file (Cấp 7 deployment)

---

## 🎓 Learning Outcomes (Cấp 1-7)

**Cấp 1:** Basic CRUD with Pydantic  
**Cấp 2:** Filtering, pagination, validation  
**Cấp 3:** Layered architecture (Router/Service/Repository)  
**Cấp 4:** SQLAlchemy ORM + Alembic migrations  
**Cấp 5:** JWT Auth + multi-user isolation  
**Cấp 6:** Advanced features (due_date, tags, smart filtering)  
**Cấp 7:** Testing (pytest) + Docker + Deployment ← YOU ARE HERE ✅

---

**Status:** ✅ **Production-Ready Full-Stack API** 🚀

Next steps:
- Deploy to cloud platform (AWS/GCP/Azure)
- Monitor with logging/tracing
- Scale with Kubernetes
- Add CI/CD pipeline (GitHub Actions/GitLab CI)

