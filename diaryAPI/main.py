from fastapi import FastAPI 
from routers import router as diary

app = FastAPI(
    title="Diary API Service",
    description="일기장 관리 및 인증 시스템 API",
    version="1.0.0",
)

app.include_router(diary)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Diary API Service is running successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)