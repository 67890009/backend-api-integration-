from fastapi import FastAPI
from sqlalchemy import text
from app.leave_types.router import router as leave_type_router
from app.auth.router import router as auth_router
from app.core.config import settings
from app.db.session import AsyncSessionLocal
import app.db.model
app = FastAPI()

app.include_router(leave_type_router)
app.include_router(auth_router)
@app.get("/")
async def root():

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))

    return {
        "database": result.scalar(),
        "jwt_algorithm": settings.JWT_ALGORITHM,
    }