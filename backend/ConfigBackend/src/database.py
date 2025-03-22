from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
