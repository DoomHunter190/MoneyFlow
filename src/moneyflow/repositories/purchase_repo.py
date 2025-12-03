from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.moneyflow.models.product import Product, PriceHistory
from src.moneyflow.models.purchase import Purchase
from datetime import date


async def get_planned_purchases(session: AsyncSession):
    """Возвращает все запланированные покупки (is_planned=True)"""
    stmt = (
        select(Purchase, Product.name)
        .join(Product, Purchase.product_id == Product.id)
        .where(Purchase.is_planned == True)
        .order_by(Purchase.date_bought)
    )
    result = await session.execute(stmt)
    return result.all()

async def get_last_price_for_product(session: AsyncSession, product_name: str):
    """Ищет последнюю цену из PriceHistory или из покупок"""
    # ищем точное совпадение по имени
    product_stmt = select(Product).where(Product.name.ilike(product_name.strip()))
    product_res = await session.execute(product_stmt)
    product = product_res.scalar_one_or_none()
    
    if not product:
        return None
    
    # ищем послениб цену в истории
    stmt = (
        select(PriceHistory.price)
        .where(PriceHistory.product_id == product.id)
        .order_by(PriceHistory.date.desc())
        .limit(1)
    )
    result = await session.scalar(stmt)
    if result:
        return float(result)
    
    # если нет в истории - берем и последней покупки

    last_purchase_price = await session.scalar(
        select(Purchase.price_at_purchase)
        .where(Purchase.product_id == product.id)
        .order_by(Purchase.date_bought.desc())
        .limit(1)
    )
    return float(last_purchase_price) if last_purchase_price else None


async def add_planned_purchase(session: AsyncSession, product_name: str, price: float, quantity: float = 1):
    product_stmt = select(Product).where(Product.name.ilike(product_name.strip()))
    result = await session.execute(product_stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        product = Product(name=product_name.strip())
        session.add(product)
        await session.flush()
    
    purchase = Purchase(
        product_id=product.id,
        price_at_purchase=price,
        quantity=quantity,
        date_bought=date.today(),
        is_planned=True
    )
    session.add(purchase)
    await session.commit()
    return purchase


async def toggle_planned(session: AsyncSession, purchase_id: int, is_planned: bool):
    await session.execute(
        update(Purchase)
        .where(purchase_id == Purchase.id)
        .values(is_planned=is_planned)
    )
    await session.commit()