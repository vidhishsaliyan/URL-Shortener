from ..database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)