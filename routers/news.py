from fastapi import APIRouter, Depends, Query, HTTPException
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

# 获取新闻详情
@router.get("/detail")
async def get_news_detail(
        news_id: int = Query(..., alias="id"),
        db: AsyncSession = Depends(db_conf.get_db)
):
    detail = await news.get_news_detail(news_id, db)
    views = await news.get_news_view(detail.id, db)
    related = await news.get_news_related(detail.id, detail.category_id, limit=5, db=db)
    if views is  None:
        raise HTTPException(
            status_code=404,
            detail="Views not found"
        )
    if detail is None:
        raise HTTPException(
            status_code=404,
            detail="News not found"
        )
    return {
        "code": 200,
        "message": "Success",
        "data": {
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "author": detail.author,
            "publish_time": detail.publish_time,
            "categoryId": detail.category_id,
            "view": detail.views,
            "relatedNews":related
        }
    }
