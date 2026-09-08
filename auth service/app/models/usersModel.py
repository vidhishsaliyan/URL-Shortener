from ..database import Base
from sqlalchemy import Column, Integer, String, text, DateTime, func

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, nullable=False, primary_key=True)
    google_sub = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)