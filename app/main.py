from fastapi import FastAPI

from app.database import engine
from app.db import Base
from app.routers import complaints

app = FastAPI(title="Complaint API")
app.include_router(complaints.router, prefix="/complaints", tags=["complaints"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()