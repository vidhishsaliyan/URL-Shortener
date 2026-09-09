from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, text
from ..config import settings
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

router = APIRouter(tags=['URL Redirect'])

@router.get('/{short_url}')
def redirect_url(short_url: str):
    with engine.connect() as db:
        result = db.execute(text("SELECT long_url FROM urls WHERE short_url = :code"), {"code":short_url}).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Short URL not found')
    long_url = result.long_url
    print(long_url)
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)