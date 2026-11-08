from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_conf
from models import news

# 获取新闻分类
async def get_categorys(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = select(news.news_category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#查询指定新闻分类下的新闻
async def get_news_list(
        category_id: int,
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = select(news.news).where(news.news.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#查询指定分类下的新闻的数量
async def get_news_count(
        category_id: int,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = select(func.count(news.news.id)).where(news.news.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

