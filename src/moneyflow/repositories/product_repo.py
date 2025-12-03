from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.moneyflow.models.product import Product, PriceHistory
from src.moneyflow.models.shop import Shop
from datetime import date


async def get_all_products(session: AsyncSession):
    stmt = select(Product).order_by(Product.name)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_price_history(session: AsyncSession, product_id: str):
    stmt = (
        select(PriceHistory, Shop.name, Shop.icon)
        .join(Shop, PriceHistory.shop_id == Shop.id)
        .where(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.date.desc())
    )
    result = await session.execute(stmt)
    return result.all()  # [(PriceHistory, shop_name, shop_icon), ...]


async def add_price_manually(session: AsyncSession, product_id: str, shop_name: str, price: float):
    # Ищем магазин по имени (с иконкой!)
    stmt = select(Shop).where(Shop.name.ilike(shop_name.strip()))
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()

    if not shop:
        # Создаём новый магазин (иконка по умолчанию — 'store')
        shop = Shop(name=shop_name.strip().title())
        session.add(shop)
        await session.flush()  # чтобы получить shop.id

    price_entry = PriceHistory(
        product_id=product_id,
        shop_id=shop.id,
        price=price,
        date=date.today()
    )
    session.add(price_entry)
    await session.commit()
    return price_entry
