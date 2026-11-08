from datetime import datetime

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(), comment="更新时间")

class news_category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), comment="分类名称")
    sort_order: Mapped[int] = mapped_column(default=0, comment="排序顺序")
