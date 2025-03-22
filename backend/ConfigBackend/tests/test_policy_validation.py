from typing import List

import pytest

from src.domains.blocks.schemas import (
    CreateOrUpdateBlockRuleSchema,
    CreateOrUpdateBlockSchema,
)
from src.domains.policies.validations import (
    FlowValidationError,
    validate_policy_flow,
)


def create_start_block(id: int, next_block_id: int = None):
    return CreateOrUpdateBlockSchema(
        id=id, next_block_id=next_block_id, type='start'
    )


def create_condition_block(
    id: int, next_block_rules: List[CreateOrUpdateBlockRuleSchema]
):
    return CreateOrUpdateBlockSchema(
        id=id, type='condition', next_block_rules=next_block_rules
    )


def create_result_block(id: int, decision_value: str):
    return CreateOrUpdateBlockSchema(
        id=id, type='result', decision_value=decision_value
    )


def create_rule(
    variable_name: str,
    operator: str,
    value: str,
    next_block_id: int,
    next_block_temp_id: int = None,
):
    return CreateOrUpdateBlockRuleSchema(
        variable_name=variable_name,
        operator=operator,
        next_block_id=next_block_id,
        value=value,
    )


@pytest.fixture
def block_rules() -> List[CreateOrUpdateBlockRuleSchema]:
    return [
        create_rule('age', '>=', '18', 4),
        create_rule('age', 'else', '0', 5),
    ]


@pytest.fixture
def block_rule_else() -> List[CreateOrUpdateBlockRuleSchema]:
    return [
        create_rule('age', 'else', '0', 5),
    ]


@pytest.fixture
def block_rules_without_else() -> List[CreateOrUpdateBlockRuleSchema]:
    return [
        create_rule('age', '>=', '18', 4),
        create_rule('age', '<', '0', 5),
    ]


@pytest.fixture
def flow_missing_start_block(block_rules) -> List[CreateOrUpdateBlockSchema]:
    condition_block = create_condition_block(
        id=2, next_block_rules=block_rules
    )
    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [condition_block, result_block_1, result_block_2]

    return flow


@pytest.fixture
def flow_with_start_block_missing_next_block_id(
    block_rules,
) -> List[CreateOrUpdateBlockSchema]:
    start_block = create_start_block(id=1)
    condition_block = create_condition_block(
        id=2, next_block_rules=block_rules
    )
    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [start_block, condition_block, result_block_1, result_block_2]

    return flow


@pytest.fixture
def flow_with_two_start_blocks(
    block_rules,
) -> List[CreateOrUpdateBlockSchema]:
    start_block_1 = create_start_block(id=1)
    start_block_2 = create_start_block(id=1)
    condition_block = create_condition_block(
        id=2, next_block_rules=block_rules
    )
    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [
        start_block_1,
        start_block_2,
        condition_block,
        result_block_1,
        result_block_2,
    ]

    return flow


@pytest.fixture
def flow_with_condition_with_less_than_two_rules(
    block_rule_else,
) -> List[CreateOrUpdateBlockSchema]:
    start_block = create_start_block(id=1, next_block_id=2)
    condition_block = create_condition_block(
        id=2, next_block_rules=block_rule_else
    )
    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [
        start_block,
        condition_block,
        result_block_1,
        result_block_2,
    ]

    return flow


@pytest.fixture
def flow_with_condition_missing_else_rule(
    block_rules_without_else,
) -> List[CreateOrUpdateBlockSchema]:
    start_block = create_start_block(id=1, next_block_id=2)
    condition_block = create_condition_block(
        id=2, next_block_rules=block_rules_without_else
    )
    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [
        start_block,
        condition_block,
        result_block_1,
        result_block_2,
    ]

    return flow


@pytest.fixture
def flow_with_condition_block_rule_missing_next_block_id() -> List[
    CreateOrUpdateBlockSchema
]:
    start_block = create_start_block(id=1, next_block_id=2)

    else_rule = create_rule('age', 'else', 'else', None)
    rule_missing_next_block_id = create_rule('age', '>=', '18', None)
    condition_block = create_condition_block(
        id=2, next_block_rules=[else_rule, rule_missing_next_block_id]
    )

    result_block_1 = create_result_block(id=3, decision_value='true')
    result_block_2 = create_result_block(id=4, decision_value='false')

    flow = [
        start_block,
        condition_block,
        result_block_1,
        result_block_2,
    ]

    return flow


@pytest.fixture
def flow_with_result_block_missing(
    block_rules,
) -> List[CreateOrUpdateBlockSchema]:
    start_block = create_start_block(1, 2)
    condition_block = create_condition_block(2, block_rules)

    flow = [start_block, condition_block]

    return flow


@pytest.fixture
def flow_with_result_block_missing_decision_value(
    block_rules,
) -> List[CreateOrUpdateBlockSchema]:
    start_block = create_start_block(1, 2)
    condition_block = create_condition_block(2, block_rules)
    result_block_1 = create_result_block(3, None)
    result_block_2 = create_result_block(4, '')

    flow = [start_block, condition_block, result_block_1, result_block_2]

    return flow


def test_validate_policy_flow_must_return_false_when_missing_start_block(
    flow_missing_start_block,
):
    policy_validation = validate_policy_flow(flow_missing_start_block)

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow is missing a start block'
    )
    assert (
        policy_validation.errors[0] == FlowValidationError.MISSING_START_BLOCK
    )


def test_validate_policy_flow_must_return_false_when_start_block_does_not_contain_next_block_id(
    flow_with_start_block_missing_next_block_id,
):
    policy_validation = validate_policy_flow(
        flow_with_start_block_missing_next_block_id
    )

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when start block is missing next_block_id'
    )
    assert (
        policy_validation.errors[0]
        == FlowValidationError.START_BLOCK_MISSING_NEXT
    )


def test_validate_policy_flow_must_return_false_when_has_more_than_two_start_blocks(
    flow_with_two_start_blocks,
):
    policy_validation = validate_policy_flow(flow_with_two_start_blocks)

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow has more than two start block'
    )
    assert (
        policy_validation.errors[0]
        == FlowValidationError.MORE_THAN_ONE_START_BLOCK
    )


def test_validate_policy_flow_must_return_false_when_condition_block_has_less_than_two_rules(
    flow_with_condition_with_less_than_two_rules,
):
    policy_validation = validate_policy_flow(
        flow_with_condition_with_less_than_two_rules
    )

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow has a condition with less than two rules'
    )
    assert (
        policy_validation.errors[0]
        == FlowValidationError.CONDITION_BLOCK_MISSING_MINIMUM_RULES
    )


def test_validate_policy_flow_must_return_false_when_condition_block_missing_else_rule(
    flow_with_condition_missing_else_rule,
):
    policy_validation = validate_policy_flow(
        flow_with_condition_missing_else_rule
    )

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow has a condition without else rule in next_block_rules'
    )
    assert (
        policy_validation.errors[0]
        == FlowValidationError.CONDITION_BLOCK_RULES_MISSING_ELSE
    )


def test_validate_policy_flow_must_return_false_when_condition_block_rule_missing_next_block_id(
    flow_with_condition_block_rule_missing_next_block_id,
):
    policy_validation = validate_policy_flow(
        flow_with_condition_block_rule_missing_next_block_id
    )

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow has a condition block rule missing next_block_id'
    )
    assert (
        policy_validation.errors[0]
        == FlowValidationError.CONDITION_BLOCK_RULE_MISSING_NEXT_BLOCK_ID
    )


def test_validate_policy_flow_must_return_false_when_decision_block_missing(
    flow_with_result_block_missing,
):
    policy_validation = validate_policy_flow(flow_with_result_block_missing)

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when flow is missing a result block'
    )

    assert (
        policy_validation.errors[0] == FlowValidationError.MISSING_RESULT_BLOCK
    )


def test_policy_flow_returns_false_when_decision_block_missing_value(
    flow_with_result_block_missing_decision_value,
):
    policy_validation = validate_policy_flow(
        flow_with_result_block_missing_decision_value
    )

    assert policy_validation.is_valid == False, (
        'Expected policy_validation.is_valid to be False when result block is missing a decision value'
    )

    assert (
        policy_validation.errors[0]
        == FlowValidationError.RESULT_BLOCK_MUST_CONTAIN_DECISION_VALUE
    )

    assert len(policy_validation.errors) == 2


# TODO: Search how to name tests properly
