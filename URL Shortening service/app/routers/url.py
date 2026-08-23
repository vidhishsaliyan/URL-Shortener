from fastapi import APIRouter, HTTPException, Depends, Response, status
from datetime import datetime, timezone, timedelta
from ..schemas import urlSchema
from ..models import urlModel
from ..database import get_db
from sqlalchemy.orm import Session
import sqlalchemy
router = APIRouter(prefix="/api/urls", tags=["URL"])

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(number):
    result = ""

    while number > 0:
        number, remainder = divmod(number, 62)
        result = ALPHABET[remainder] + result

    return result.zfill(6)


@router.post('/shorten', status_code=status.HTTP_201_CREATED)
async def create_short_url(request : urlSchema.RequestURL, db: Session = Depends(get_db)):
    expiry_minutes = 30
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    try:
        value = db.execute(urlModel.counter)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry! Out of service")
    SPACE = 62**6
    value = (value*26860463)%SPACE
    short_url = base62_encode(value)
    new_entry = urlModel.URL(long_url=request.long_url, short_url=str(short_url), expiry_time=expiry_time)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry