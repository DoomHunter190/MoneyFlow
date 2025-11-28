from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_async_engine(
    settings.database_url_asyncpg,
    echo=False if not settings.DEBUG else True,  # Логи в DEBUG
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Возвращает сессию как context manager"""
    async with AsyncSessionLocal() as session:
        yield session
