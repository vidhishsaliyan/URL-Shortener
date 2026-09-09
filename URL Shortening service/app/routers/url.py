from fastapi import APIRouter, HTTPException, Depends, Response, status, Request
from datetime import datetime, timezone, timedelta
from ..schemas import urlSchema
from ..models import urlModel
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils.shorten_utils import is_url_reachable
router = APIRouter(prefix="/api/urls", tags=["URL Shortening"])

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(number):
    result = ""

    while number > 0:
        number, remainder = divmod(number, 62)
        result = ALPHABET[remainder] + result

    return result.zfill(6)


@router.post('/shorten', status_code=status.HTTP_201_CREATED)
async def create_short_url(request: Request, request_body : urlSchema.RequestURL, db: Session = Depends(get_db)):
    long_url = str(request_body.long_url)

    reachable = await is_url_reachable(long_url)
    if not reachable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid URL')

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
    user_id_header = request.headers.get("X-User-ID")
    new_entry = urlModel.URL(long_url=long_url, short_url=str(short_url), expiry_time=expiry_time, user_id=user_id_header)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry