"""bootstrap after manual re-creation

Revision ID: 68472036d73c
Revises: 5b61af7a1d86
Create Date: 2025-07-18 20:26:26.558253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68472036d73c'
down_revision: Union[str, Sequence[str], None] = '5b61af7a1d86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
