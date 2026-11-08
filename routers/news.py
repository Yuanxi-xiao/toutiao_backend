import select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import crud

from config import db_conf
from crud import news


router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(
        page: int = 1,
        page_size: int = 100,
        db: AsyncSession = Depends(db_conf.get_db)
):
    skip = (page - 1) * page_size
    list = await news.get_categorys(skip, page_size, db)
    return {
        "code": 200,
        "message": "Success",
        "data": list
    }


