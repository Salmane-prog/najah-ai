"""add correct_answer to quiz_answers

Revision ID: add_correct_answer_to_quiz_answers
Revises: 123456789abc
Create Date: 2025-01-22 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_correct_answer_to_quiz_answers'
down_revision = '123456789abc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ajouter le champ correct_answer à la table quiz_answers
    op.add_column('quiz_answers', sa.Column('correct_answer', sa.Text(), nullable=True))


def downgrade() -> None:
    # Supprimer le champ correct_answer de la table quiz_answers
    op.drop_column('quiz_answers', 'correct_answer') 