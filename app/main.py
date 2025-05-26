from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config.database import init_db
from app.controllers.person_controller import router as person_router

static_path = "app/static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(person_router)

if os.path.exists(os.path.join(static_path, "index.html")):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
