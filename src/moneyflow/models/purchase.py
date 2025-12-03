from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Numeric, Date, Boolean
from .base import Base
from uuid import UUID


class Purchase(Base):
    __tablename__ = 'purchases'

    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'))
    shop_id: Mapped[UUID] = mapped_column(ForeignKey('shops.id'), nullable=True)
    quantity: Mapped[Numeric] = mapped_column(Numeric(10, 3), default=1)
    price_at_purchase: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    date_bought: Mapped[Date] = mapped_column(Date, nullable=False)
    is_planned: Mapped[bool] = mapped_column(Boolean, default=False)
