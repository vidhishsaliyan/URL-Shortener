from fastapi import FastAPI
from .routers import url
from .models import urlModel
from .database import Base, engine
app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get('/api/urls/')
def index():
    return {"message": "URL shortening service is running"}

app.include_router(router=url.router)