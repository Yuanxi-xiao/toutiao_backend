from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_conf
from models.news import news_category


async def get_categorys(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(db_conf.get_db)
):
    stmt = select(news_category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
