from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Numeric, Date
from .base import Base
from uuid import UUID


class Car(Base):
    __tablename__ = "cars"

    name: Mapped[str] = mapped_column(String(100), default="Моя машина")
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(nullable=True)
    plate_number: Mapped[str] = mapped_column(String(20), nullable=True)
    odometer_start: Mapped[int] = mapped_column(default=0)


class Fueling(Base):
    __tablename__ = "fuelings"

    car_id: Mapped[UUID] = mapped_column(ForeignKey("cars.id"))
    liters: Mapped[Numeric] = mapped_column(Numeric(8, 3))
    price_per_liter: Mapped[Numeric] = mapped_column(Numeric(8, 2))
    total_cost: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    odometer: Mapped[int] = mapped_column()
    date: Mapped[Date] = mapped_column(Date)


class CarExpense(Base):
    __tablename__ = "car_expenses"

    car_id: Mapped[UUID] = mapped_column(ForeignKey("cars.id"))
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    odometer: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[Date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
