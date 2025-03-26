import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domains.policies.models import Block, BlockRule, BlockType, Policy
from src.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def create_inital_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                # Policy
                policy = Policy('loan')

                session.add(policy)
                await session.flush()

                # #Blocks
                start_block = Block(BlockType.START, 1, None, next_block_id=2)
                condition_block = Block(BlockType.CONDITION, 1, None)
                decision_block_1 = Block(BlockType.RESULT, 1, '1000')
                decision_block_2 = Block(BlockType.RESULT, 1, '2000')

                session.add(start_block)
                session.add(condition_block)
                session.add(decision_block_1)
                session.add(decision_block_2)
                await session.flush()

                # Block Rules
                block_rule_1 = BlockRule(
                    'age', 'GREATER_OR_EQUAL_THAN', '18', 2, 3
                )
                block_rule_2 = BlockRule('age', 'ELSE', '18', 2, 4)

                session.add(block_rule_1)
                session.add(block_rule_2)
                await session.flush()
            except Exception as e:
                raise e


if __name__ == '__main__':
    asyncio.run(create_inital_data())
