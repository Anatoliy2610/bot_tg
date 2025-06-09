from fastapi import FastAPI

from app.users.router import router as users_router
from app.posts.router import router as posts_router
from app.database import Base, engine, SessionLocal



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(posts_router)

