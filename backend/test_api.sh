#!/bin/bash

# API Base URL
BASE_URL="http://localhost:8000/api/v1"

echo "=== To-Do List API - Test Examples ==="
echo ""

# Create first todo
echo "1. CREATE TODO"
curl -X POST "$BASE_URL/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Study FastAPI with SQLAlchemy and SQLModel",
    "is_done": false
  }' && echo ""

# Create second todo
echo ""
echo "2. CREATE ANOTHER TODO"
curl -X POST "$BASE_URL/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Setup Database",
    "description": "Configure SQLite and run migrations",
    "is_done": false
  }' && echo ""

# List all todos
echo ""
echo "3. LIST ALL TODOS"
curl -X GET "$BASE_URL/todos" && echo ""

# List completed todos only
echo ""
echo "4. LIST COMPLETED TODOS"
curl -X GET "$BASE_URL/todos?is_done=true" && echo ""

# Search todos
echo ""
echo "5. SEARCH TODOS (query: 'FastAPI')"
curl -X GET "$BASE_URL/todos?q=FastAPI" && echo ""

# Get first todo
echo ""
echo "6. GET TODO BY ID"
curl -X GET "$BASE_URL/todos/1" && echo ""

# PATCH todo (partial update) - update only is_done
echo ""
echo "7. PATCH TODO (update only is_done)"
curl -X PATCH "$BASE_URL/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"is_done": true}' && echo ""

# PATCH todo - update only description
echo ""
echo "8. PATCH TODO (update only description)"
curl -X PATCH "$BASE_URL/todos/2" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}' && echo ""

# Complete todo (mark as done)
echo ""
echo "9. COMPLETE TODO (POST /todos/1/complete)"
curl -X POST "$BASE_URL/todos/2/complete" && echo ""

# Full update (PUT)
echo ""
echo "10. FULL UPDATE TODO (PUT)"
curl -X PUT "$BASE_URL/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI - Updated",
    "description": "Deep dive into FastAPI with DB",
    "is_done": true
  }' && echo ""

# List with pagination and sorting
echo ""
echo "11. LIST WITH PAGINATION (limit=1, offset=0)"
curl -X GET "$BASE_URL/todos?limit=1&offset=0" && echo ""

# Sort by created_at DESC
echo ""
echo "12. LIST SORTED BY created_at DESC"
curl -X GET "$BASE_URL/todos?sort=-created_at&limit=10" && echo ""

# Delete todo
echo ""
echo "13. DELETE TODO"
curl -X DELETE "$BASE_URL/todos/1" && echo ""

# Get total count
echo ""
echo "14. LIST (shows total count)"
curl -X GET "$BASE_URL/todos" && echo ""

echo ""
echo "=== Tests completed ==="
