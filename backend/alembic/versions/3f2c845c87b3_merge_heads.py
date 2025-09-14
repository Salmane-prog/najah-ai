"""merge_heads

Revision ID: 3f2c845c87b3
Revises: 694619018174, add_correct_answer_to_quiz_answers
Create Date: 2025-07-22 21:52:18.953030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2c845c87b3'
down_revision: Union[str, Sequence[str], None] = ('694619018174', 'add_correct_answer_to_quiz_answers')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
