from typing import Dict, List

from src.domains.blocks.schemas import (
    CreateOrUpdateBlockRuleSchema,
    CreateOrUpdateBlockSchema,
)
from src.domains.policies.models import BlockType, ConditionCriteria
from src.domains.policies.schemas import (
    FlowValidationError,
    PolicyValidation,
)


def print_helper(variable: str = '', value: any = None):
    print('\n')
    print('#' * 20 + ' ' + variable + ' ' + '#' * 20)
    print(value)
    print('#' * 40 + '#' * (len(variable) + 2))


def validate_policy_flow(
    flow: List[CreateOrUpdateBlockSchema],
) -> PolicyValidation:
    errors = []

    block_type_to_list: Dict[BlockType, List[CreateOrUpdateBlockSchema]] = {
        BlockType.START: [],
        BlockType.CONDITION: [],
        BlockType.RESULT: [],
    }

    block_ids = []
    for block in flow:
        block_ids.append(block.id or block.temp_id)

        if block.type in block_type_to_list:
            block_type_to_list[block.type].append(block)

    errors = (
        validate_start_block(block_type_to_list[BlockType.START])
        + validate_condition_block(block_type_to_list[BlockType.CONDITION])
        + validate_result_block(block_type_to_list[BlockType.RESULT])
    )

    if len(errors) == 0:
        """
        Validate block references only after ensuring the required blocks exist in the flow.
        Otherwise, missing blocks might cause incorrect block reference errors.
        """
        errors.extend(
            validate_next_block_references(
                block_ids,
                block_type_to_list[BlockType.START][0],
                block_type_to_list[BlockType.CONDITION],
            )
        )

    if len(errors) == 0:
        """
        Validate that the flow is a Directed Acyclic Graph (DAG) only after ensuring 
        that all blocks reference valid nodes. Otherwise, invalid references might 
        lead to incorrect validation results.
        """
        errors.extend(validate_flow_is_directed_acyclic(flow))

    is_valid = len(errors) == 0

    return PolicyValidation(is_valid=is_valid, errors=errors)


def validate_start_block(
    start_blocks: List[CreateOrUpdateBlockSchema],
) -> List[FlowValidationError]:
    errors = []

    if len(start_blocks) == 0:
        errors.append(FlowValidationError.MISSING_START_BLOCK)
    else:
        if len(start_blocks) > 1:
            errors.append(FlowValidationError.MORE_THAN_ONE_START_BLOCK)

        if len(start_blocks) == 1:
            if (
                start_blocks[0].next_block_id is None
                and start_blocks[0].next_block_temp_id is None
            ):
                errors.append(FlowValidationError.START_BLOCK_MISSING_NEXT)

    return errors


def validate_condition_block(
    condition_blocks: List[CreateOrUpdateBlockSchema],
) -> List[FlowValidationError]:
    errors = []

    for condition_block in condition_blocks:
        errors.extend(
            validate_condition_block_rules(condition_block.next_block_rules)
        )

    return errors


def validate_condition_block_rules(
    next_block_rules: List[CreateOrUpdateBlockRuleSchema],
) -> List[FlowValidationError]:
    errors = []

    if len(next_block_rules) < 2:
        errors.append(
            FlowValidationError.CONDITION_BLOCK_MISSING_MINIMUM_RULES
        )

    else_rule = []
    for rule in next_block_rules:
        if rule.operator == ConditionCriteria.ELSE:
            else_rule.append(rule)

        if rule.next_block_id is None and rule.next_block_temp_id is None:
            errors.append(
                FlowValidationError.CONDITION_BLOCK_RULE_MISSING_NEXT_BLOCK_ID
            )

    if len(else_rule) == 0:
        errors.append(FlowValidationError.CONDITION_BLOCK_RULES_MISSING_ELSE)
    elif len(else_rule) > 1:
        errors.append(
            FlowValidationError.CONDITION_BLOCK_RULES_WITH_MORE_THAN_ONE_ELSE
        )

    return errors


def validate_result_block(
    result_blocks: List[CreateOrUpdateBlockSchema],
) -> List[FlowValidationError]:
    errors = []

    if len(result_blocks) == 0:
        errors.append(FlowValidationError.MISSING_RESULT_BLOCK)
        return errors

    for result in result_blocks:
        if not result.decision_value:
            errors.append(
                FlowValidationError.RESULT_BLOCK_MUST_CONTAIN_DECISION_VALUE
            )

    return errors


def validate_next_block_references(
    block_ids: List[int],
    start_block: CreateOrUpdateBlockSchema,
    condition_blocks: List[CreateOrUpdateBlockSchema],
) -> List[FlowValidationError]:
    errors = []

    start_block_next_block_ref = (
        start_block.next_block_id or start_block.next_block_temp_id
    )
    if start_block_next_block_ref not in block_ids:
        errors.append(FlowValidationError.INVALID_NEXT_BLOCK_REFERENCE)

    for condition_block in condition_blocks:
        for rule in condition_block.next_block_rules:
            if (
                rule.next_block_id not in block_ids
                and rule.next_block_temp_id not in block_ids
            ):
                errors.append(FlowValidationError.INVALID_NEXT_BLOCK_REFERENCE)

    return errors


def validate_flow_is_directed_acyclic(
    flow: List[CreateOrUpdateBlockSchema],
) -> List[FlowValidationError]:
    """
    Validates whether the flow forms a Directed Acyclic Graph (DAG).
    This is done using a Depth-First Search (DFS) based topological sorting algorithm.
    """

    errors = []

    # Step 1: Convert the flow into an adjacency list, where each
    # node is mapped to its children, representing the graph's structure.
    adjacency_dict = policy_flow_to_adjacency_dict(flow)

    # Step 2: Check if the graph can be topologically sorted,
    # which confirms that it is a Directed Acyclic Graph (DAG).
    # Only DAG are able to be topologically sorted.
    is_acyclic = can_topologically_sort(adjacency_dict)

    if not is_acyclic:
        errors.append(FlowValidationError.FLOW_CONTAINS_CYCLE)

    return errors


def policy_flow_to_adjacency_dict(
    flow: List[CreateOrUpdateBlockSchema],
) -> Dict[int, List[int]]:
    adjacency_dict = {}
    for block in flow:
        block_id = block.id or block.temp_id

        if block.type == BlockType.START:
            # Start block has a single outgoing edge
            next_block = block.next_block_id or block.next_block_temp_id
            adjacency_dict[block_id] = [next_block] if next_block else []

        if block.type == BlockType.CONDITION:
            block_edges = []
            # Condition block has multiple outgoing edges
            for rule in block.next_block_rules:
                block_edges.append(
                    rule.next_block_id or rule.next_block_temp_id
                )

            adjacency_dict[block_id] = block_edges

        if block.type == BlockType.RESULT:
            # Result blocks do not have outgoing edges.
            adjacency_dict[block_id] = []

    return adjacency_dict


def can_topologically_sort(adjacency_dict: Dict[int, List[int]]) -> bool:
    nodes_sorted = []
    nodes_visited = {}

    for node_key, _ in adjacency_dict.items():
        if node_key not in nodes_visited:
            is_acyclic = dfs_detect_cycle(
                node_key, nodes_visited, nodes_sorted, adjacency_dict
            )
            if not is_acyclic:
                return is_acyclic

    return is_acyclic


def dfs_detect_cycle(
    key: int,
    nodes_visited: Dict[str, bool],
    nodes_sorted: List[int],
    adjacency_dict: Dict[int, List[int]],
) -> bool:
    nodes_visited[key] = True

    children_keys = adjacency_dict[key]
    for child_key in children_keys:
        if (
            nodes_visited.get(child_key, False)
            and child_key not in nodes_sorted
        ):
            return False

        if child_key not in nodes_sorted:
            is_acyclic = dfs_detect_cycle(
                child_key, nodes_visited, nodes_sorted, adjacency_dict
            )
            if not is_acyclic:
                return False

    nodes_sorted.append(key)

    return True
