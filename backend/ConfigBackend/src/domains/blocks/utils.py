from typing import List

from ConfigBackend.src.utils.string_utils import (
    convert_underscores_to_spaces,
    convert_spaces_to_underscores,
)
from src.domains.blocks.schemas import (
    BlockRuleSchema,
    BlockSchema,
    CreateOrUpdateBlockRuleSchema,
    CreateOrUpdateBlockSchema,
)
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
        position_x=block.position_x,
        position_y=block.position_y,
    )


def block_rule_model_to_schema(block_rule: BlockRule) -> BlockRuleSchema:
    return BlockRuleSchema(
        variable_name=convert_underscores_to_spaces(block_rule.variable_name),
        operator=block_rule.operator,
        value=block_rule.value,
        next_block_id=block_rule.next_block_id,
    )


def block_schemas_to_entities(
    policy_id: int, flow: List[CreateOrUpdateBlockSchema]
) -> List[Block]:
    return [
        create_or_updated_block_schema_to_entity(policy_id, block_schema)
        for block_schema in flow
    ]


def create_or_updated_block_schema_to_entity(
    policy_id: int, block: CreateOrUpdateBlockSchema
) -> Block:
    return Block(
        type=block.type,
        policy_id=policy_id,
        decision_value=block.decision_value,
        position_y=block.position_y,
        position_x=block.position_x,
    )


def create_or_update_block_rule_schema_to_entity(
    current_block_id, next_block_id, block_rule: CreateOrUpdateBlockRuleSchema
) -> BlockRule:
    return BlockRule(
        variable_name=convert_spaces_to_underscores(block_rule.variable_name),
        current_block_id=current_block_id,
        next_block_id=next_block_id,
        operator=block_rule.operator,
        value=block_rule.value,
    )
