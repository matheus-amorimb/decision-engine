from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.domains.policies.models import Block, Policy
from src.repository import BaseRepository


class PolicyRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = Policy
        self.db_session = db_session

    async def get_all(self) -> List[Policy]:
        db_policies = await self.db_session.scalars(select(self.model))

        return db_policies

    async def get_by_name(self, name: str) -> Policy:
        db_policy = await self.db_session.scalar(
            select(self.model).where(self.model.name == name)
        )

        return db_policy

    async def get_by_id_with_blocks(self, id: int) -> Policy:
        db_policy = await self.db_session.scalar(
            select(self.model).where(self.model.id == id)
        )

        return db_policy
