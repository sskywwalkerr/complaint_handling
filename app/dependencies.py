from app.database import get_db


async def get_db_session():
    async with get_db() as session:
        yield session
