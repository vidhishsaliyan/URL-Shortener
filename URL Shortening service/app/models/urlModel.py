from ..database import Base
from sqlalchemy import Column, Integer, String, text, DateTime, func, Sequence, ForeignKey
class URL(Base):
    __tablename__ = "urls"
    short_url = Column(String, primary_key=True, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expiry_time = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(Integer, server_default=text("0"), nullable=False)
    user_id = Column(Integer,  nullable=False)


counter = Sequence(name="counter", start=1000, increment=1, metadata=Base.metadata)