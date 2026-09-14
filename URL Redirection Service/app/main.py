from fastapi import FastAPI
from .routers import redirect
from .utils import persist_click_count
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(func=persist_click_count, trigger="interval", minutes=1)
    scheduler.start()
    print('APP STARTUP')
    yield
    scheduler.shutdown()
    print('APP SHUTDOWN')


app = FastAPI(lifespan=lifespan)



app.include_router(router=redirect.router)