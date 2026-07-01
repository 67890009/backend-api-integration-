from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import AsyncSessionLocal

app = FastAPI()


@app.get("/")
async def root():

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }