from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_conf


router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(db_conf.get_db)
):

    return {
        "code": 200,
        "message": "Success",
        "data": ["获取新闻分类列表"]
    }


