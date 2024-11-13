from fastapi import FastAPI
from app.api.v1.endpoints import todos
from app.core.config import settings

app = FastAPI(title="Todo API")

app.include_router(todos.router, prefix=f"{settings.API_V1_STR}/todos", tags=["todos"])