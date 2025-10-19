from fastapi import FastAPI
import uvicorn

from app.apis.pre_process import router as pre_process

app = FastAPI()

app.include_router(pre_process)

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )