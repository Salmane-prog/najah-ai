"""bootstrap

Revision ID: dd331746d50d
Revises: 339facc8b7ca
Create Date: 2025-07-18 19:37:44.851194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd331746d50d'
down_revision: Union[str, Sequence[str], None] = '339facc8b7ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
