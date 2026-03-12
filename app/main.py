from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import async_session, engine, get_session
from app.models import Base
from app.routers import calls, carrier, dashboard, loads
from app.seed import seed_loads


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and seed data on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        await seed_loads(session)
    yield
    await engine.dispose()


app = FastAPI(title="Brokerage API", version="1.0.0", lifespan=lifespan)

app.include_router(carrier.router)
app.include_router(loads.router)
app.include_router(calls.router)
app.include_router(dashboard.router)


@app.get("/health", tags=["health"])
async def health():
    async with async_session() as session:
        await session.execute(text("SELECT 1"))
    return {"status": "healthy"}
