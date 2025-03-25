from typing import List, Optional

from pydantic import BaseModel

from src.domains.policies.models import BlockType, ConditionCriteria


class BlockRuleSchema(BaseModel):
    variable_name: str
    operator: ConditionCriteria
    value: str
    next_block_id: Optional[int] = None
    next_block_temp_id: Optional[int] = None


class BlockSchema(BaseModel):
    id: Optional[int] = None
    type: BlockType
    decision_value: Optional[str] = None
    next_block_id: Optional[int] = None
    next_block_rules: Optional[List[BlockRuleSchema]] = []


class CreateOrUpdateBlockRuleSchema(BaseModel):
    variable_name: str
    operator: ConditionCriteria
    value: Optional[str] = None
    next_block_id: Optional[int] = None
    next_block_temp_id: Optional[str] = None


class CreateOrUpdateBlockSchema(BaseModel):
    id: Optional[int] = None
    temp_id: Optional[str] = None
    type: BlockType
    decision_value: Optional[str] = None
    next_block_id: Optional[int] = None
    next_block_temp_id: Optional[str] = None
    next_block_rules: Optional[List[CreateOrUpdateBlockRuleSchema]] = []
