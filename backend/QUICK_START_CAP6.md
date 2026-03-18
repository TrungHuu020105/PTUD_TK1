# Quick Start - Cấp 6 (Due Dates + Tags + Smart Filtering)

## 🚀 Chạy Cấp 6 trong 3 bước

### Step 1: Install dependencies (from Cấp 5)
```bash
cd backend
pip install -r requirements.txt
```
No new packages needed!

### Step 2: Setup environment & migrate
```bash
# Copy .env template (if not done from Cấp 5)
cp .env.example .env

# Run migrations (creates due_date column + tags tables)
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
python test_cap6.py
```

### Manual test (7 commands)

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

**3. Create todo with due_date**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Finish report",
    "description":"Q1 analysis",
    "due_date":"2026-03-20T17:00:00Z"
  }'

export TODO_ID=1
```

**4. Create overdue todo (to test /overdue)**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Yesterday task",
    "due_date":"2026-03-17T17:00:00Z"
  }'
```

**5. Get overdue todos**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/overdue
```
Response shows todos with `due_date < now` and `is_done=false`

**6. Get today's todos**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/todos/today
```
Response shows todos with `due_date` matching today

**7. Update todo with new due_date**
```bash
curl -X PATCH http://localhost:8000/api/v1/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"due_date":"2026-03-25T10:00:00Z"}'
```

---

## 📌 Key Features - Cấp 6

✅ Due dates for todos  
✅ Smart date filtering (overdue/today)  
✅ Tags system with many-to-many  
✅ User-isolated tags  
✅ Inherits all Cấp 5 auth features  

---

## 🔗 New Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /todos/overdue` | List overdue todos (due_date < now) |
| `GET /todos/today` | List todos due today |
| All POST/PUT/PATCH /todos | Now support `due_date` field |

---

## 📊 Todo Response (Updated)

```json
{
  "id": 1,
  "owner_id": 1,
  "title": "Finish report",
  "description": "Q1 analysis",
  "is_done": false,
  "due_date": "2026-03-20T17:00:00Z",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:00Z",
  "tags": []
}
```

---

## 📚 Learn More

- [README_CAP6.md](README_CAP6.md) - Full documentation
- [CAP6_SUMMARY.md](CAP6_SUMMARY.md) - Feature summary
- [routers/todo_router.py](routers/todo_router.py) - New endpoints
- [models/todo.py](models/todo.py) - Due date + tags models

---

**Next: Run `python test_cap6.py` or use curl commands above 🎉**
