"""set foriegn key urls

Revision ID: c72467742931
Revises: 8f667baf6139
Create Date: 2026-08-24 01:30:32.993366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c72467742931'
down_revision: Union[str, Sequence[str], None] = '8f667baf6139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_urls_user_id',
        'urls',
        'users',
        ['user_id'],
        ['user_id']
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_urls_user_id',
        'urls',
        type_='foreignkey'
    )
