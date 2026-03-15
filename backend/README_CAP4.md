# To-Do List API - Cấp 4: Database Integration

## Setup Database

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup environment
Copy `.env.example` to `.env` and update DATABASE_URL if needed:
```bash
cp .env.example .env
```

### 3. Run database migrations
```bash
alembic upgrade head
```

This will create the `todos` table with the following columns:
- `id` (Integer, Primary Key)
- `title` (String 3-100)
- `description` (String, optional)
- `is_done` (Boolean, default False)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### 4. Run the app
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

Base path: `/api/v1`

### Todos

#### List todos (with pagination, filtering, searching, sorting)
```
GET /todos
  ?is_done=true/false
  &q=keyword
  &sort=created_at|-created_at
  &limit=10
  &offset=0
```

#### Create todo
```
POST /todos
Body: {
  "title": "string (3-100)",
  "description": "string (optional)",
  "is_done": false
}
```

#### Get todo
```
GET /todos/{todo_id}
```

#### Update todo (full update)
```
PUT /todos/{todo_id}
Body: {
  "title": "string",
  "description": "string",
  "is_done": boolean
}
```

#### Patch todo (partial update) - NEW
```
PATCH /todos/{todo_id}
Body: {
  "title": "string (optional)",
  "description": "string (optional)",
  "is_done": boolean (optional)
}
```
Only provided fields will be updated.

#### Complete todo - NEW
```
POST /todos/{todo_id}/complete
```
Sets `is_done=true` and updates `updated_at`.

#### Delete todo
```
DELETE /todos/{todo_id}
```

## Key Features - Cấp 4

✅ SQLModel for type-safe ORM  
✅ SQLAlchemy for database operations  
✅ Pagination from real database query  
✅ Automatic `created_at` and `updated_at` timestamps  
✅ Alembic migrations for schema versioning  
✅ PATCH endpoint for partial updates  
✅ Complete endpoint to mark todos as done  
✅ SQLite by default (can switch to PostgreSQL via DATABASE_URL)  

## Architecture

```
backend/
├── core/
│   ├── config.py           # Settings & env config
│   └── database.py         # SQLAlchemy engine & session
├── models/
│   └── todo.py             # SQLModel tables
├── schemas/
│   └── todo.py             # Pydantic request/response schemas
├── repositories/
│   └── todo_repository.py  # Database access layer
├── services/
│   └── todo_service.py     # Business logic
├── routers/
│   └── todo_router.py      # API endpoints
├── alembic/
│   ├── env.py              # Migration environment
│   ├── versions/           # Migration files
│   │   └── 001_initial.py  # Initial schema
│   └── script.py.mako      # Migration template
├── main.py                 # FastAPI app entry
├── alembic.ini             # Alembic config
├── requirements.txt        # Dependencies
└── .env.example            # Environment template
```

## Database Support

- **SQLite** (default): `sqlite:///./test.db`
- **PostgreSQL**: `postgresql://user:password@localhost/todolist`

Update `DATABASE_URL` in `.env` to switch databases.

## Testing with curl

```bash
# Create todo
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","description":"Study database integration"}'

# List todos
curl http://localhost:8000/api/v1/todos

# Get specific todo
curl http://localhost:8000/api/v1/todos/1

# Patch todo (partial update)
curl -X PATCH http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"is_done":true}'

# Complete todo
curl -X POST http://localhost:8000/api/v1/todos/1/complete

# Delete todo
curl -X DELETE http://localhost:8000/api/v1/todos/1
```
