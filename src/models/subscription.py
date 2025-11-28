from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Numeric, Date
from .base import Base
from uuid import UUID


class Subscription(Base):
    __tablename__ = 'subscriptions'

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='RUB')
    cycle: Mapped[str] = mapped_column(String(20), default='monthly')  # monthly, yearly, weekly, custom
    next_payment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey('categories.id'), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
