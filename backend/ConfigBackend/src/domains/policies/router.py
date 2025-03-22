from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_session
from src.domains.policies.schemas import (
    CreatePolicySchema,
    GetPolicySchema,
    PolicySchema,
)
from src.domains.policies.services import PolicyService

router = APIRouter(prefix='/policies', tags=['policies'])

DbSession = Annotated[Session, Depends(get_session)]


@router.get(
    '/{policy_id}', status_code=HTTPStatus.OK, response_model=GetPolicySchema
)
async def get_policy(policy_id: int, session: DbSession):
    service = PolicyService(session)
    policy = await service.get_policy_by_id(policy_id)

    return policy


@router.get(
    '/blocks/{policy_id}',
    status_code=HTTPStatus.OK,
    response_model=PolicySchema,
)
async def get_policy_with_blocks(policy_id: int, session: DbSession):
    service = PolicyService(session)
    policy_with_blocks = await service.get_policy_by_id_with_blocks(policy_id)

    return policy_with_blocks


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PolicySchema)
async def create_policy(policy: CreatePolicySchema, session: DbSession):
    service = PolicyService(session)
    new_policy_id = await service.create_policy(policy)
    new_policy = await service.get_policy_by_id_with_blocks(new_policy_id)

    return new_policy