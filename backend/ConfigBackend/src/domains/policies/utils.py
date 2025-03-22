from src.domains.blocks.utils import block_model_to_schema
from src.domains.policies.models import Policy
from src.domains.policies.schemas import PolicySchema


def policy_model_to_schema(policy: Policy) -> PolicySchema:
    return PolicySchema(
        id=policy.id,
        name=policy.name,
        flow=[block_model_to_schema(block) for block in policy.blocks],
    )
