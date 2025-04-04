from sqlalchemy import delete

from src.domains.policies.models import Block, BlockRule
from src.repository import BaseRepository


class BlockRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = Block
        self.db_session = db_session

    async def delete_blocks_by_policy_id(self, policy_id: int):
        statement = delete(self.model).where(Block.policy_id == policy_id)
        await self.db_session.execute(statement)
        await self.db_session.flush()


class BlockRulesRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = BlockRule
        self.db_session = db_session
