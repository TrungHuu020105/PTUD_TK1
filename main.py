from fastapi import FastAPI

app = FastAPI(title="To-Do List API")


@app.get("/")
def root():
    return {"message": "Chào mừng bạn đến với To-Do List API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
