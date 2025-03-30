import operator
from typing import Callable, Dict, List
from ConfigBackend.src.utils.string_utils import (
    convert_spaces_to_underscores,
    convert_underscores_to_spaces,
)
from src.domains.blocks.utils import block_model_to_schema
from src.domains.policies.models import (
    Block,
    BlockType,
    ConditionCriteria,
    Policy,
)
from src.domains.policies.schemas import PolicySchema


conditionCriteriaToOperatorFunc: Dict[str, Callable[[int, int], bool]] = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '=': operator.eq,
    '!=': operator.ne,
}


def policy_model_to_schema(policy: Policy) -> PolicySchema:
    return PolicySchema(
        id=policy.id,
        name=convert_underscores_to_spaces(policy.name),
        flow=[block_model_to_schema(block) for block in policy.blocks],
    )


def calculate_flow_decision(
    flow: List[Block], input_data: Dict[str, str]
) -> str:
    def find_block_by_id(block_id: str) -> Block:
        return next((block for block in flow if block.id == block_id), None)

    def determine_next_block_id(block: Block) -> str:
        for rule in block.next_block_rules:
            if rule.operator != ConditionCriteria.ELSE:
                rule_variable = rule.variable_name
                rule_operator = conditionCriteriaToOperatorFunc[
                    rule.operator.value
                ]
                rule_value = rule.value

                input_value = input_data_normalized[rule_variable]

                if rule_operator(input_value, rule_value):
                    return rule.next_block_id

        return next(
            (
                rule.next_block_id
                for rule in block.next_block_rules
                if rule.operator == ConditionCriteria.ELSE
            ),
            None,
        )

    # Normalize the input_data keys
    input_data_normalized = normalize_dict_keys(input_data)

    # Find the starting block
    start_block = next(
        (block for block in flow if block.type == BlockType.START), None
    )
    # Find the following block after starting block
    current_block = find_block_by_id(start_block.next_block_id)

    # Traverse the flow until a RESULT block is reached
    while current_block.type != BlockType.RESULT:
        next_block_id = determine_next_block_id(current_block)
        current_block = find_block_by_id(next_block_id)

    return current_block.decision_value


def normalize_dict_keys(input_dict: Dict[str, str]) -> Dict[str, str]:
    return {
        convert_spaces_to_underscores(key): value
        for key, value in input_dict.items()
    }
