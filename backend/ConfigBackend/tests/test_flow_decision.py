from src.domains.policies.models import (
    Block,
    BlockRule,
    BlockType,
    ConditionCriteria,
    Policy,
)
from src.domains.policies.utils import calculate_flow_decision


def test_calculate_flow_decision():
    # Create a mock policy
    policy = Policy(name='Test Policy')
    policy.id = 1  # Manually set policy ID

    # Create mock blocks
    start_block = Block(
        type=BlockType.START, policy_id=policy.id, decision_value=None
    )
    condition_block = Block(
        type=BlockType.CONDITION, policy_id=policy.id, decision_value=None
    )
    result_block_pass = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='Accepted'
    )
    result_block_fail = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='Rejected'
    )

    # Manually set IDs after instantiation
    start_block.id = 1
    condition_block.id = 2
    result_block_pass.id = 3
    result_block_fail.id = 4

    # Set relationships after instantiation
    start_block.next_block_id = 2
    condition_block.next_block_rules = [
        BlockRule(
            variable_name='age',
            operator=ConditionCriteria.GREATER_THAN,
            value='18',
            next_block_id=3,
            current_block_id=2,
        ),
        BlockRule(
            variable_name='age',
            operator=ConditionCriteria.ELSE,
            value='',
            next_block_id=4,
            current_block_id=2,
        ),
    ]

    flow = [start_block, condition_block, result_block_pass, result_block_fail]

    # Test case where age is greater than 18
    input_data = {'Age': '20'}
    assert calculate_flow_decision(flow, input_data) == 'Accepted'

    # Test case where age is 18 or less
    input_data = {'Age': '16'}
    assert calculate_flow_decision(flow, input_data) == 'Rejected'


def test_complex_flow_with_multiple_conditions():
    # Create a mock policy
    policy = Policy(name='Complex Policy')
    policy.id = 1

    # Create mock blocks
    start_block = Block(
        type=BlockType.START, policy_id=policy.id, decision_value=None
    )
    condition_block1 = Block(
        type=BlockType.CONDITION, policy_id=policy.id, decision_value=None
    )
    condition_block2 = Block(
        type=BlockType.CONDITION, policy_id=policy.id, decision_value=None
    )
    condition_block3 = Block(
        type=BlockType.CONDITION, policy_id=policy.id, decision_value=None
    )
    result_approved = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='Approved'
    )
    result_rejected = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='Rejected'
    )
    result_review = Block(
        type=BlockType.RESULT,
        policy_id=policy.id,
        decision_value='Needs Review',
    )

    # Set IDs
    start_block.id = 1
    condition_block1.id = 2
    condition_block2.id = 3
    condition_block3.id = 4
    result_approved.id = 5
    result_rejected.id = 6
    result_review.id = 7

    # Set relationships
    start_block.next_block_id = 2
    condition_block1.next_block_rules = [
        BlockRule(
            variable_name='age',
            operator=ConditionCriteria.GREATER_THAN,
            value='21',
            next_block_id=3,
            current_block_id=2,
        ),
        BlockRule(
            variable_name='age',
            operator=ConditionCriteria.ELSE,
            value='',
            next_block_id=6,
            current_block_id=2,
        ),
    ]
    condition_block2.next_block_rules = [
        BlockRule(
            variable_name='income',
            operator=ConditionCriteria.GREATER_THAN_OR_EQUAL_TO,
            value='50000',
            next_block_id=5,
            current_block_id=3,
        ),
        BlockRule(
            variable_name='income',
            operator=ConditionCriteria.ELSE,
            value='',
            next_block_id=4,
            current_block_id=3,
        ),
    ]
    condition_block3.next_block_rules = [
        BlockRule(
            variable_name='credit_score',
            operator=ConditionCriteria.GREATER_THAN_OR_EQUAL_TO,
            value='600',
            next_block_id=5,
            current_block_id=4,
        ),
        BlockRule(
            variable_name='credit_score',
            operator=ConditionCriteria.ELSE,
            value='',
            next_block_id=7,
            current_block_id=4,
        ),
    ]

    flow = [
        start_block,
        condition_block1,
        condition_block2,
        condition_block3,
        result_approved,
        result_rejected,
        result_review,
    ]

    # Test cases
    # Approved (age > 21 AND income >= 50000)
    assert (
        calculate_flow_decision(
            flow, {'Age': '25', 'Income': '60000', 'Credit Score': '650'}
        )
        == 'Approved'
    )

    # Rejected (age <= 21)
    assert (
        calculate_flow_decision(
            flow, {'Age': '18', 'Income': '60000', 'Credit Score': '650'}
        )
        == 'Rejected'
    )

    # Rejected (age > 21, income <= 50000, but credit_score >= 600)
    assert (
        calculate_flow_decision(
            flow, {'Age': '25', 'Income': '60000', 'Credit Score': '550'}
        )
        == 'Approved'
    )

    # Needs Review (age > 21, income < 50000, but credit_score <= 600)
    assert (
        calculate_flow_decision(
            flow, {'Age': '25', 'Income': '49999', 'Credit Score': '599'}
        )
        == 'Needs Review'
    )


def test_equals_operator():
    policy = Policy(name='Equality Test')
    policy.id = 1

    start_block = Block(
        type=BlockType.START, policy_id=policy.id, decision_value=None
    )
    condition_block = Block(
        type=BlockType.CONDITION, policy_id=policy.id, decision_value=None
    )
    result_match = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='Match'
    )
    result_no_match = Block(
        type=BlockType.RESULT, policy_id=policy.id, decision_value='No Match'
    )

    start_block.id = 1
    condition_block.id = 2
    result_match.id = 3
    result_no_match.id = 4

    start_block.next_block_id = 2
    condition_block.next_block_rules = [
        BlockRule(
            variable_name='country',
            operator=ConditionCriteria.EQUAL,
            value='USA',
            next_block_id=3,
            current_block_id=2,
        ),
        BlockRule(
            variable_name='country',
            operator=ConditionCriteria.ELSE,
            value='',
            next_block_id=4,
            current_block_id=2,
        ),
    ]

    flow = [start_block, condition_block, result_match, result_no_match]

    assert calculate_flow_decision(flow, {'Country': 'USA'}) == 'Match'
    assert calculate_flow_decision(flow, {'Country': 'Canada'}) == 'No Match'
