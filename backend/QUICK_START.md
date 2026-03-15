# Quick Start - Cấp 4 Database Integration

## 🚀 Chạy nhanh trong 3 bước

### Step 1: Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run migrations
```bash
alembic upgrade head
```
✅ Cái này sẽ tạo file `test.db` với bảng `todos`

### Step 3: Run server
```bash
uvicorn main:app --reload
```

✅ API sẵn sàng tại: `http://localhost:8000/api/v1`

---

## 🧪 Test API ngay

### Option 1: Dùng Python script
```bash
python test_api.py
```
Chạy toàn bộ test cases (create, patch, complete, list, delete, ...)

### Option 2: Dùng FastAPI Docs
Truy cập `http://localhost:8000/docs` → thử endpoints trực tiếp từ Swagger UI

### Option 3: Dùng curl
```bash
# Create todo
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Todo","description":"Testing","is_done":false}'

# List todos
curl http://localhost:8000/api/v1/todos

# PATCH todo (partial update) - NEW
curl -X PATCH http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"is_done":true}'

# Complete todo - NEW
curl -X POST http://localhost:8000/api/v1/todos/1/complete
```

---

## 📌 Ghi chú quan trọng

1. **Database:** Mặc định dùng SQLite (`test.db`)
   - Để thay PostgreSQL, edit `.env` với `DATABASE_URL=postgresql://...`

2. **Migrations:** 
   - Tạo bảng tự động lần đầu tiên chạy `alembic upgrade head`
   - Nếu xóa nhầm `.db`, chạy lại lệnh trên

3. **Timestamps:**
   - `created_at` và `updated_at` tự động quản lý bởi server
   - Không cần gửi từ client

4. **Field mới:**
   - `description`: Optional string field
   - `updated_at`: Tự update mỗi khi sửa todo

---

## 📖 Xem chi tiết

- **README_CAP4.md** - Hướng dẫn đầy đủ
- **CAP4_SUMMARY.md** - Tóm tắt toàn bộ Cấp 4
- `test_api.py` - Test script chi tiết

---

**Happy coding! 🎉**
