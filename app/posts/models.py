from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
