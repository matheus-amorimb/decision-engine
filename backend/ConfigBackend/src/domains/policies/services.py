from typing import Dict, List

from sqlalchemy.orm import Session

from ConfigBackend.src.domains.blocks.utils import (
    create_or_update_block_rule_schema_to_entity,
    create_or_updated_block_schema_to_entity,
)
from ConfigBackend.src.utils.string_utils import (
    convert_spaces_to_underscores,
    convert_underscores_to_spaces,
)
from src.domains.blocks.repository import BlockRepository, BlockRulesRepository
from src.domains.blocks.schemas import (
    CreateOrUpdateBlockRuleSchema,
    CreateOrUpdateBlockSchema,
)
from src.domains.policies.models import Block, BlockRule, BlockType, Policy
from src.domains.policies.repository import PolicyRepository
from src.domains.policies.schemas import (
    CreatePolicySchema,
    GetPolicySchema,
    PolicyDecision,
    PolicySchema,
    UpdatePolicySchema,
)
from src.domains.policies.utils import (
    calculate_flow_decision,
    policy_model_to_schema,
)
from src.domains.policies.validations import validate_policy_flow
from src.exceptions import (
    PolicyFlowValidationException,
    ResourceNotFoundException,
    ValidationException,
)


class PolicyService:
    def __init__(self, db: Session):
        self.policy_repository = PolicyRepository(db)
        self.block_repository = BlockRepository(db)
        self.block_rules_repository = BlockRulesRepository(db)
        self.session = db

        self.temp_id_to_id = {}

    async def get_policies(self) -> List[GetPolicySchema]:
        result = await self.policy_repository.get_all()

        return [policy_model_to_schema(policy) for policy in result]

    async def get_policy_by_id(self, policy_id: int) -> Policy:
        result = await self.policy_repository.get_by_id(Policy, policy_id)
        if not result:
            raise ResourceNotFoundException('policy_not_found')

        return result

    async def get_policy_by_id_with_flow(self, policy_id: int) -> PolicySchema:
        result = await self.policy_repository.get_by_id_with_blocks(policy_id)

        if not result:
            raise ResourceNotFoundException('policy_not_found')

        return policy_model_to_schema(result)

    async def get_policy_variables(self, policy_id: int) -> List[str]:
        policy = await self.policy_repository.get_by_id_with_blocks(policy_id)

        if not policy:
            raise ResourceNotFoundException('policy_not_found')

        policy_variables = []
        for block in policy.blocks:
            for rule in block.next_block_rules:
                rule_name_sanitized = convert_underscores_to_spaces(
                    rule.variable_name
                )
                if rule_name_sanitized not in policy_variables:
                    policy_variables.append(rule_name_sanitized)

        return policy_variables

    async def create_policy(self, policy_schema: CreatePolicySchema) -> int:
        async with self.session.begin():
            try:
                # Save new policy
                new_policy = await self.policy_repository.create(
                    Policy(convert_spaces_to_underscores(policy_schema.name))
                )

                if len(policy_schema.flow) == 0:
                    return new_policy.id

                # Validate flow
                policy_validation = validate_policy_flow(policy_schema.flow)
                if not policy_validation.is_valid:
                    raise PolicyFlowValidationException(
                        policy_validation.errors
                    )

                # Save new blocks
                await self.__handle_save_new_blocks(
                    new_policy.id, policy_schema.flow
                )

                # Save new rules
                await self.__handle_save_new_rules(policy_schema)

            except Exception as e:
                raise e

        return new_policy.id


    async def update_policy(self, policy_schema: UpdatePolicySchema) -> int:
        async with self.session.begin():
            try:
                policy_update = await self.policy_repository.get_by_id(
                    Policy, policy_schema.id
                )

                if not policy_update:
                    raise ResourceNotFoundException(
                        'policy_not_found'
                    )

                """
                You're about to witness a crime, so proceed at your own risk...
                Due to time constraints, I've temporarily decided to apply this (crime) of a solution to handle cases where a user updates a policy's flow. 
                Instead of updating only the modified blocks, adding new ones, and removing deleted ones, I'm straight-up deleting all blocks for the given policy and recreating them from scratch. 
                This saves me a lot of time for now and also makes it easier on the frontend when retrieving the policy's flow, 
                since doing it this way means I don't have to worry about keeping the original block IDs in the frontend.
                
                Unfortunately, if you're reading this, it means I didn't have enough time to clean up the crime scene. 
                Either way, let this be a record that this is by no means the correct way to do this.
                """

                await self.block_repository.delete_blocks_by_policy_id(
                    policy_schema.id
                )

                if len(policy_schema.flow) == 0:
                    return policy_update.id

                # Validate flow
                policy_validation = validate_policy_flow(policy_schema.flow)
                if not policy_validation.is_valid:
                    raise PolicyFlowValidationException(
                        policy_validation.errors
                    )

                # Save new blocks
                await self.__handle_save_new_blocks(
                    policy_update.id, policy_schema.flow
                )

                # Save new rules
                await self.__handle_save_new_rules(policy_schema)

            except Exception as e:
                raise e

        return policy_update.id

    async def get_policy_decision(
        self, policy_id: int, data: Dict[str, str]
    ) -> PolicyDecision:
        policy_variables = await self.get_policy_variables(policy_id)

        for variable in policy_variables:
            if variable not in data.keys():
                raise ValidationException(f'variable_in_decision_is_missing')

        policy = await self.policy_repository.get_by_id_with_blocks(policy_id)
        policy_decision = calculate_flow_decision(policy.blocks, data)

        return PolicyDecision(decision=policy_decision)

    async def __handle_save_new_blocks(
        self, policy_id: int, blocks_schemas: List[CreateOrUpdateBlockSchema]
    ) -> None:
        start_block_id = None
        start_block_next_block_temp_id = None
        for block_schema in blocks_schemas:
            block_entity = create_or_updated_block_schema_to_entity(
                policy_id, block_schema
            )
            new_block = await self.block_repository.create(block_entity)

            """
            Start block are the only one that holds a reference to a temp_id besides the rules.
            So, we must keep tracking of this block so we can updated it once all the blocks are created.
            """
            if block_schema.type == BlockType.START:
                start_block_id = new_block.id
                start_block_next_block_temp_id = (
                    block_schema.next_block_temp_id
                )

            self.temp_id_to_id[block_schema.temp_id] = new_block.id

        await self.__handle_update_start_block_with_next_block_id(
            start_block_id, start_block_next_block_temp_id
        )

    async def __handle_update_start_block_with_next_block_id(
        self, block_id: int, next_block_temp_id: int
    ) -> None:
        start_block = await self.block_repository.get_by_id(Block, block_id)
        next_block_id = self.temp_id_to_id.get(next_block_temp_id)
        start_block.next_block_id = next_block_id
        await self.block_repository.update(start_block)

    async def __handle_save_new_rules(
        self, policy_schema: CreatePolicySchema
    ) -> None:
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
