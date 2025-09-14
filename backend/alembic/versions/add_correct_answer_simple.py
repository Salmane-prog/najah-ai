"""add correct_answer to quiz_answers

Revision ID: add_correct_answer_simple
Revises: 68472036d73c
Create Date: 2025-01-22 10:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_correct_answer_simple'
down_revision = '68472036d73c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ajouter le champ correct_answer à la table quiz_answers
    op.add_column('quiz_answers', sa.Column('correct_answer', sa.Text(), nullable=True))


def downgrade() -> None:
    # Supprimer le champ correct_answer de la table quiz_answers
    op.drop_column('quiz_answers', 'correct_answer') 