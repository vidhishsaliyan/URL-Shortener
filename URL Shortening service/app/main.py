from fastapi import FastAPI
from .routers import url
from .models import urlModel
from .database import Base, engine
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router=url.router)