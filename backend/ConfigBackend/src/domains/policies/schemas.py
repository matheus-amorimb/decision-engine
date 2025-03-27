from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from src.domains.blocks.schemas import BlockSchema, CreateOrUpdateBlockSchema


class GetPolicySchema(BaseModel):
    id: int
    name: Optional[str]


class PolicySchema(BaseModel):
    id: int
    name: Optional[str]
    flow: List[BlockSchema]


class CreatePolicySchema(BaseModel):
    name: str
    flow: Optional[List[CreateOrUpdateBlockSchema]] = []


class UpdatePolicySchema(BaseModel):
    id: int
    flow: List[CreateOrUpdateBlockSchema] = []


class PolicyDecision(BaseModel):
    decision: str


class FlowValidationError(Enum):
    MISSING_START_BLOCK = 'Flow is missing a start block.'
    MORE_THAN_ONE_START_BLOCK = 'Flow has more than one start block.'
    START_BLOCK_MISSING_NEXT = (
        'Start block is missing next_block_id or next_block_temp_id.'
    )
    CONDITION_BLOCK_MISSING_MINIMUM_RULES = (
        'Condition block must have at least two rules'
    )
    CONDITION_BLOCK_RULES_MISSING_ELSE = (
        'Condition block rules must contain ELSE rule'
    )
    CONDITION_BLOCK_RULES_WITH_MORE_THAN_ONE_ELSE = (
        'Condition block rules must contain only one ELSE rule'
    )
    CONDITION_BLOCK_RULE_MISSING_NEXT_BLOCK_ID = (
        'Condition block rule missing next block id'
    )
    MISSING_RESULT_BLOCK = 'Flow is missing a result block'
    RESULT_BLOCK_MUST_CONTAIN_DECISION_VALUE = (
        'Result block must contain decision value'
    )
    INVALID_NEXT_BLOCK_REFERENCE = 'Next_block_id or Next_block_temp_id must reference a valid block in the flow.'
    FLOW_CONTAINS_CYCLE = 'The decision flow contains a loop.'

    def code(self):
        return self.name

    def message(self):
        return self.value


class PolicyValidation(BaseModel):
    is_valid: bool
    errors: List[FlowValidationError] = []
