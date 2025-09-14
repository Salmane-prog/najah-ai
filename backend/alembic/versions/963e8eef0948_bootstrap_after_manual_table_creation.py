"""bootstrap after manual table creation

Revision ID: 963e8eef0948
Revises: b94e8b5fa862
Create Date: 2025-07-18 20:18:30.616127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '963e8eef0948'
down_revision: Union[str, Sequence[str], None] = 'b94e8b5fa862'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
