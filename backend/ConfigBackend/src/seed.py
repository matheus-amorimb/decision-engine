import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domains.policies.models import (
    Block,
    BlockRule,
    BlockType,
    ConditionCriteria,
    Policy,
)
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
                start_block = Block(
                    type=BlockType.START,
                    policy_id=1,
                    decision_value=None,
                    next_block_id=2,
                    position_x=0,
                    position_y=0,
                )
                condition_block = Block(
                    type=BlockType.CONDITION,
                    policy_id=1,
                    decision_value=None,
                    position_x=500,
                    position_y=0,
                )
                decision_block_1 = Block(
                    type=BlockType.RESULT,
                    policy_id=1,
                    decision_value='APPROVED',
                    position_x=800,
                    position_y=-500,
                )
                decision_block_2 = Block(
                    type=BlockType.RESULT,
                    policy_id=1,
                    decision_value='DENIED',
                    position_x=800,
                    position_y=500,
                )

                session.add(start_block)
                session.add(condition_block)
                session.add(decision_block_1)
                session.add(decision_block_2)
                await session.flush()

                # Block Rules
                block_rule_1 = BlockRule(
                    'age',
                    ConditionCriteria.GREATER_THAN_OR_EQUAL_TO,
                    '18',
                    2,
                    3,
                )
                block_rule_2 = BlockRule(
                    'age', ConditionCriteria.ELSE, '18', 2, 4
                )

                session.add(block_rule_1)
                session.add(block_rule_2)
                await session.flush()

            except Exception as e:
                raise e


if __name__ == '__main__':
    asyncio.run(create_inital_data())
