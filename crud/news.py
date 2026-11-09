from fastapi import Depends
from sqlalchemy import select, func, update
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

#查询新闻详情
async def get_news_detail(
        news_id: int,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = select(news.news).where(news.news.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#更新新闻浏览量
async def get_news_view(
        news_id: int,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = update(news.news).where(news.news.id == news_id).values(views = news.news.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    #更新 → 检查数据是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0

#查询相关新闻
async def get_news_related(
        news_id: int,
        category_id: int,
        db: AsyncSession,
        limit: int = 5
):
    stmt = select(news.news).where(
        news.news.id != news_id,
        news.news.category_id == category_id
    ).order_by(
        news.news.id.desc(), #默认是升序，desc表示降序
        news.news.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    #列表推导式 推导出新闻的核心数据， 然后再 return
    return [{
        "id": detail.id,
        "title": detail.title,
        "content": detail.content,
        "image": detail.image,
        "author": detail.author,
        "publish_time": detail.publish_time,
        "categoryId": detail.category_id,
        "view": detail.views
    } for detail in related_news]

