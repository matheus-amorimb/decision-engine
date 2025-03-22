from src.domains.policies.models import Block, BlockRule
from src.repository import BaseRepository


class BlockRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = Block
        self.db_session = db_session


class BlockRulesRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session)
        self.model = BlockRule
        self.db_session = db_session
