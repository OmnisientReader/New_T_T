from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.core.database import init_db
from app.routers import table, reservation
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application startup...")
    yield
    logger.info("Application shutdown...")


app = FastAPI(
    title="Restaurant Booking API",
    description="API for booking tables in a restaurant.",
    version="0.1.0",
    lifespan=lifespan
)


app.include_router(table.router)
app.include_router(reservation.router)

@app.get("/", tags=["Root"])
async def read_root():

    return {"message": "Welcome to the Restaurant Booking API!"}

