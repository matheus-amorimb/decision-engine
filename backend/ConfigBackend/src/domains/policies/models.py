from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class BlockType(Enum):
    START = 'start'
    CONDITION = 'condition'
    RESULT = 'result'


class ConditionCriteria(Enum):
    EQUAL = '='
    LOWER_THAN = '<'
    LOWER_OR_EQUAL_THAN = '<='
    GREATER_THAN = '>'
    GREATER_OR_EQUAL_THAN = '>='
    ELSE = 'else'


@table_registry.mapped_as_dataclass
class Policy:
    __tablename__ = 'policies'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    blocks: Mapped[List['Block']] = relationship(
        init=False,
        back_populates='policy',
        default_factory=list,
        lazy='selectin',
    )


@table_registry.mapped_as_dataclass
class Block:
    __tablename__ = 'blocks'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    type: Mapped[BlockType] = mapped_column(SAEnum(BlockType))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    policy_id: Mapped[int] = mapped_column(ForeignKey('policies.id'))
    policy: Mapped['Policy'] = relationship(
        init=False, lazy='selectin', repr=False
    )

    position_x: Mapped[float] = mapped_column(nullable=True, default=None)
    position_y: Mapped[float] = mapped_column(nullable=True, default=None)

    decision_value: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )

    next_block_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('blocks.id'), nullable=True, default=None
    )

    next_block_rules: Mapped[List['BlockRule']] = relationship(
        init=False,
        lazy='selectin',
        foreign_keys='BlockRule.current_block_id',
        cascade='all, delete-orphan',
    )


@table_registry.mapped_as_dataclass
class BlockRule:
    __tablename__ = 'block_rules'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    variable_name: Mapped[str]
    operator: Mapped[ConditionCriteria]
    value: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    current_block_id: Mapped[int] = mapped_column(
        ForeignKey('blocks.id', ondelete='CASCADE')
    )
    next_block_id: Mapped[int] = mapped_column(
        ForeignKey('blocks.id', ondelete='CASCADE')
    )
