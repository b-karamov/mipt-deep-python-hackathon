from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from repository.tables import metadata
from api.dependencies import engine
from api.routes import users, posts, comments


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="CommentHub API",
    description="API для системы постов и комментариев",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в CommentHub API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("!!!ПЕРЕЙДИ ПО ССЫЛКЕ: http://localhost:8000/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
