from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, model: Type[T], id: int) -> T:
        result = await self.db_session.get(model, id)

        return result

    async def create(self, model: T) -> T:
        self.db_session.add(model)
        await self.db_session.flush()
        await self.db_session.refresh(model)

        return model

    async def update(self, model: T) -> T:
        self.db_session.add(model)
        await self.db_session.flush()
        await self.db_session.refresh(model)

        return model
