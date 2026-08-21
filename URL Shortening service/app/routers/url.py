from fastapi import APIRouter, HTTPException, Depends, Response, status
from datetime import datetime, timezone, timedelta
from ..schemas import urlSchema
from ..models import urlModel
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/api/urls", tags=["URL"])

@router.post('/shorten', status_code=status.HTTP_201_CREATED)
async def create_short_url(request : urlSchema.RequestURL, db: Session = Depends(get_db)):
    expiry_minutes = 30
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    short_url = "dfgkjh.com"
    new_url = urlModel.URLs(long_url=request.long_url, short_url=short_url, expiry_time=expiry_time)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url