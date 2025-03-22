from typing import List

from sqlalchemy.orm import Session

from src.domains.blocks.repository import BlockRepository, BlockRulesRepository
from src.domains.blocks.schemas import (
    CreateOrUpdateBlockRuleSchema,
    CreateOrUpdateBlockSchema,
)
from src.domains.policies.models import Block, BlockRule, BlockType, Policy
from src.domains.policies.repository import PolicyRepository
from src.domains.policies.schemas import CreatePolicySchema, PolicySchema
from src.domains.policies.utils import policy_model_to_schema
from src.domains.policies.validations import validate_policy_flow
from src.exceptions import (
    PolicyFlowValidationException,
    ResourceNotFoundException,
)


class PolicyService:
    def __init__(self, db: Session):
        self.policy_repository = PolicyRepository(db)
        self.block_repository = BlockRepository(db)
        self.block_rules_repository = BlockRulesRepository(db)
        self.session = db

        self.temp_id_to_id = {}

    async def get_policy_by_id(self, policy_id: int) -> Policy:
        result = await self.policy_repository.get_by_id(Policy, policy_id)
        if not result:
            raise ResourceNotFoundException('policy_not_found')

        return result

    async def get_policy_by_id_with_blocks(
        self, policy_id: int
    ) -> PolicySchema:
        result = await self.policy_repository.get_by_id_with_blocks(policy_id)

        if not result:
            raise ResourceNotFoundException('policy_not_found')

        return policy_model_to_schema(result)

    async def create_policy(self, policy_schema: CreatePolicySchema) -> int:
        async with self.session.begin():
            try:
                existing_policy = await self.policy_repository.get_by_name(
                    policy_schema.name.lower()
                )

                # if existing_policy:
                # raise ConflictException(f"policy_name_{policy.name}_already_in_use")

                policy_validation = validate_policy_flow(policy_schema.flow)
                if not policy_validation.is_valid:
                    raise PolicyFlowValidationException(
                        policy_validation.errors
                    )

                # Save new policy
                new_policy = await self.policy_repository.create(
                    Policy(policy_schema.name)
                )

                # Save new blocks
                await self.handle_save_new_blocks(
                    new_policy.id, policy_schema.flow
                )

                # Save new rules
                await self.handle_save_new_rules(policy_schema)

            except Exception as e:
                raise e

        return new_policy.id

    async def handle_save_new_blocks(
        self, policy_id: int, blocks_schemas: List[CreateOrUpdateBlockSchema]
    ):
        start_block_id = None
        start_block_next_block_temp_id = None
        for block_schema in blocks_schemas:
            """
            Start block are the only one that holds a reference to a temp_id besides the rules.
            So, we must keep tracking of this block so we can updated it once all the blocks are created.
            """
            block_entity = create_or_updated_block_schema_to_entity(
                policy_id, block_schema
            )
            new_block = await self.block_repository.create(block_entity)

            if block_schema.type == BlockType.START:
                start_block_id = new_block.id
                start_block_next_block_temp_id = (
                    block_schema.next_block_temp_id
                )

            self.temp_id_to_id[block_schema.temp_id] = new_block.id

        await self.handle_update_start_block_with_next_block_id(
            start_block_id, start_block_next_block_temp_id
        )

    async def handle_update_start_block_with_next_block_id(
        self, block_id: int, next_block_temp_id: int
    ):
        start_block = await self.block_repository.get_by_id(Block, block_id)
        next_block_id = self.temp_id_to_id.get(next_block_temp_id)
        start_block.next_block_id = next_block_id
        await self.block_repository.update(start_block)

    async def handle_save_new_rules(self, policy_schema: CreatePolicySchema):
        for block_schema in policy_schema.flow:
            for rule_schema in block_schema.next_block_rules:
                current_block_id = self.temp_id_to_id.get(block_schema.temp_id)
                next_block_id = self.temp_id_to_id.get(
                    rule_schema.next_block_temp_id
                )
                rule_entity = create_or_update_block_rule_schema_to_entity(
                    current_block_id, next_block_id, rule_schema
                )
                await self.block_rules_repository.create(rule_entity)


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
    )


def create_or_update_block_rule_schema_to_entity(
    current_block_id, next_block_id, block_rule: CreateOrUpdateBlockRuleSchema
) -> BlockRule:
    return BlockRule(
        variable_name=block_rule.variable_name,
        current_block_id=current_block_id,
        next_block_id=next_block_id,
        operator=block_rule.operator,
        value=block_rule.value,
    )
