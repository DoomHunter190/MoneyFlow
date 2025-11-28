from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base


class Shop(Base):
    __tablename__ = 'shops'

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String(50), default='store')