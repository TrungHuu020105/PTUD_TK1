# To-Do List API

## Cấp 0 — Làm quen FastAPI (Hello To-Do)

### Mục tiêu

Tạo API tối thiểu chạy được với FastAPI.

### Yêu cầu

- Tạo project FastAPI
- Endpoint:
  - `GET /health` → trả `{ "status": "ok" }`
  - `GET /` → trả message chào

### Tiêu chí đạt

Chạy uvicorn và gọi được 2 endpoint.

---

## Cấu trúc project

```
TK1_todolist/
├── main.py            # App FastAPI với 2 endpoint
├── requirements.txt   # Dependencies (fastapi, uvicorn)
└── README.md
```

## Cách thực hiện

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy server

```bash
uvicorn main:app --reload --port 8000
```

### 3. Kiểm tra endpoint

| Method | Path      | Response                                              |
| ------ | --------- | ----------------------------------------------------- |
| GET    | `/`       | `{"message": "Chào mừng bạn đến với To-Do List API!"}` |
| GET    | `/health` | `{"status": "ok"}`                                    |

- Mở trình duyệt truy cập: `http://localhost:8000`
- Xem health check: `http://localhost:8000/health`
- Swagger UI (tài liệu API tự động): `http://localhost:8000/docs`
