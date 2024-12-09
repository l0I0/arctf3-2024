from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.get("/")
async def root():
    """
    Проверка работоспособности API.
    """
    return {"message": "Hello World"}

@router.get("/check_db")
async def check_db(db: AsyncSession = Depends(get_db)):
    """
    Проверка подключения к базе данных.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        await db.commit()
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}
