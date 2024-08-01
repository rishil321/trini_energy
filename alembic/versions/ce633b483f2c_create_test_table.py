"""create test table

Revision ID: ce633b483f2c
Revises: b802911f087c
Create Date: 2024-07-29 21:12:52.864688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce633b483f2c'
down_revision: Union[str, None] = 'b802911f087c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
