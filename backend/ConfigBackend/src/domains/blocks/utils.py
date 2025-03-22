from typing import List

from src.domains.blocks.schemas import BlockRuleSchema, BlockSchema
from src.domains.policies.models import Block, BlockRule


def block_model_to_schema(block: Block) -> BlockSchema:
    return BlockSchema(
        id=block.id,
        type=block.type,
        decision_value=block.decision_value,
        next_block_id=block.next_block_id,
        next_block_rules=[
            block_rule_model_to_schema(block_rule)
            for block_rule in block.next_block_rules
        ],
    )


def block_rule_model_to_schema(block_rule: BlockRule) -> BlockRuleSchema:
    return BlockRuleSchema(
        variable_name=block_rule.variable_name,
        operator=block_rule.operator,
        value=block_rule.value,
        next_block_id=block_rule.next_block_id,
    )
