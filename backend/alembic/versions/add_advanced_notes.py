"""Add advanced notes tables

Revision ID: add_advanced_notes
Revises: 
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_advanced_notes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Créer la table des matières avancées
    op.create_table('advanced_subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('note_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advanced_subjects_id'), 'advanced_subjects', ['id'], unique=False)
    op.create_unique_constraint('uq_advanced_subjects_name', 'advanced_subjects', ['name'])
    
    # Créer la table des chapitres avancés
    op.create_table('advanced_chapters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('note_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['subject_id'], ['advanced_subjects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advanced_chapters_id'), 'advanced_chapters', ['id'], unique=False)
    
    # Créer la table des notes avancées
    op.create_table('advanced_notes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=True),
        sa.Column('tags', sqlite.JSON, nullable=True),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=True),
        sa.Column('is_shared', sa.Boolean(), nullable=True),
        sa.Column('shared_with', sqlite.JSON, nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advanced_notes_id'), 'advanced_notes', ['id'], unique=False)


def downgrade():
    # Supprimer les tables dans l'ordre inverse
    op.drop_index(op.f('ix_advanced_notes_id'), table_name='advanced_notes')
    op.drop_table('advanced_notes')
    
    op.drop_index(op.f('ix_advanced_chapters_id'), table_name='advanced_chapters')
    op.drop_table('advanced_chapters')
    
    op.drop_index(op.f('ix_advanced_subjects_id'), table_name='advanced_subjects')
    op.drop_table('advanced_subjects')

