from datetime import datetime

from sqlalchemy import DateTime, func, String, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(), comment="更新时间")

class news_category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), comment="分类名称")
    sort_order: Mapped[int] = mapped_column(default=0, comment="排序顺序")

class news(Base):
    __tablename__ = "news"

    #创建索引：提升查询速度 → 添加目录
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),
        Index("idx_publish_time", "publish_time")
    )

    id: Mapped[int] = mapped_column(primary_key=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), comment="新闻标题")
    description: Mapped[str] = mapped_column(String(500), comment="新闻描述")
    content: Mapped[str] = mapped_column(Text, comment="新闻内容")
    image: Mapped[str] = mapped_column(String(255), comment="新闻图片")
    author: Mapped[str] = mapped_column(String(50), comment="新闻作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), comment="分类ID")
    views: Mapped[int] = mapped_column(default=0, comment="浏览次数")
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment="发布时间")

    def __repr__(self):
        return f"<news(id={self.id}, title={self.title}, description={self.description}, content={self.content}, image={self.image}, author={self.author}, category_id={self.category_id}, views={self.views}, publish_time={self.publish_time})>"
