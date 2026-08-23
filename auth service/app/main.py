from fastapi import FastAPI
from .routers import auth
from .models import usersModel
from .database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from .config import settings

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    https_only=False,
    same_site="lax"
)

@app.get('/')
def index():
    return {"message": "auth service is running"}

Base.metadata.create_all(bind=engine)
app.include_router(router=auth.router)