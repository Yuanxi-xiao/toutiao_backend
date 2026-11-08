from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import crud

from config import db_conf
from crud import news


router = APIRouter(prefix="/api/news",tags=["news"])

# 获取新闻分类
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

# 获取新闻列表
@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(db_conf.get_db)
):
    skip = (page - 1) * page_size
    list = await news.get_news_list(category_id, skip, page_size, db)
    total = await news.get_news_count(category_id, db)
    hasMore = (skip + len(list)) < total
    return {
        "code": 200,
        "message": "Success",
        "data": {
            "list": list,
            "total": total,
            "hasMore" : hasMore
        }
    }

