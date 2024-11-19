"""drop items table

Revision ID: c69235fd07bf
Revises: a8238dffc468
Create Date: 2024-11-19 11:18:44.189509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c69235fd07bf'
down_revision: Union[str, None] = 'a8238dffc468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
