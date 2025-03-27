from http import HTTPStatus
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_session
from src.domains.policies.schemas import (
    CreatePolicySchema,
    GetPolicySchema,
    PolicyDecision,
    PolicySchema,
    UpdatePolicySchema,
)
from src.domains.policies.services import PolicyService

router = APIRouter(prefix='/policies', tags=['policies'])

DbSession = Annotated[Session, Depends(get_session)]


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=List[GetPolicySchema],
    description='Retrieve a list of all policies.',
)
async def get_all_policies(session: DbSession):
    service = PolicyService(session)
    policies = await service.get_policies()

    return policies


@router.get(
    '/{policy_id}',
    status_code=HTTPStatus.OK,
    response_model=GetPolicySchema,
    description='Retrieve a specific policy by its ID.',
)
async def get_policy(policy_id: int, session: DbSession):
    service = PolicyService(session)
    policy = await service.get_policy_by_id(policy_id)

    return policy


@router.get(
    '/blocks/{policy_id}',
    status_code=HTTPStatus.OK,
    response_model=PolicySchema,
    description='Retrieve a policy with its flow diagram (blocks).',
)
async def get_policy_with_flow(policy_id: int, session: DbSession):
    service = PolicyService(session)
    policy_with_blocks = await service.get_policy_by_id_with_flow(policy_id)

    return policy_with_blocks


@router.get(
    '/{policy_id}/variables',
    status_code=HTTPStatus.OK,
    response_model=List[str],
    description='Retrieve all variables associated with a specific policy.',
)
async def get_policy_variables(policy_id: int, session: DbSession):
    service = PolicyService(session)
    policy_variables = await service.get_policy_variables(policy_id)

    return policy_variables


@router.post(
    '/{policy_id}/decision',
    status_code=HTTPStatus.OK,
    response_model=PolicyDecision,
    description='Evaluate and return the decision based on the given data for a specific policy.',
)
async def get_policy_decision(
    policy_id: int, data: Dict[str, str], session: DbSession
):
    service = PolicyService(session)
    policy_result = await service.get_policy_decision(policy_id, data)

    return policy_result


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=PolicySchema,
    description='Create a new policy.',
)
async def create_policy(policy: CreatePolicySchema, session: DbSession):
    service = PolicyService(session)
    new_policy_id = await service.create_policy(policy)
    new_policy = await service.get_policy_by_id_with_flow(new_policy_id)

    return new_policy


@router.put(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=PolicySchema,
    description='Update an existing policy.',
)
async def update_policy(policy: UpdatePolicySchema, session: DbSession):
    service = PolicyService(session)
    policy_update_id = await service.update_policy(policy)
    new_policy = await service.get_policy_by_id_with_flow(policy_update_id)

    return new_policy
