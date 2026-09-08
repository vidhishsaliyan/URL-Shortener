from ..database import Base
from sqlalchemy import Column, Integer, String, text, DateTime, func

class Token(Base):
    __tablename__ = "tokens"
    token_hash = Column(String, nullable=False, unique=True)
    login_id = Column(String, primary_key=True, nullable=False, unique=True)