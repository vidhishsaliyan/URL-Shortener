"""expiry non-nullable

Revision ID: dfc9fe42a8c7
Revises: 6edbaef783e6
Create Date: 2026-08-21 19:57:45.972477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfc9fe42a8c7'
down_revision: Union[str, Sequence[str], None] = '6edbaef783e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("urls", "expiry_time", nullable=False)


def downgrade() -> None:
    op.alter_column("urls", "expiry_time", nullable=True)

