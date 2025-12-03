from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str] = mapped_column(String(50), default='receipt')
    color: Mapped[str] = mapped_column(String(20), default='#6366f1')
    type: Mapped[str] = mapped_column(String(20), default='expense')