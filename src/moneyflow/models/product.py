from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Numeric, Date
from .base import Base
from uuid import UUID


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    default_category_id: Mapped[UUID] = mapped_column(ForeignKey('categories.id'), nullable=True)


class PriceHistory(Base):
    __tablename__ = 'price_history'

    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False)
    shop_id: Mapped[UUID] = mapped_column(ForeignKey('shops.id'), nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
