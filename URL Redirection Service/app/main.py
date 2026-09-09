from fastapi import FastAPI
from .routers import redirect
app = FastAPI()

app.include_router(router=redirect.router)