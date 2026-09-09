from fastapi import FastAPI
from .routers import auth
from .models import usersModel, authModel
from .database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from .config import settings
from .database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    https_only=False,
    same_site="lax"
)

@app.get('/api/auth')
def index():
    return {"message": "auth service is running"}

app.include_router(router=auth.router)