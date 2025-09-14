from alembic import op
import sqlalchemy as sa

revision = '123456789abc'
down_revision = '25c34cbcf053'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
    )
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('subject', sa.String, nullable=False),
        sa.Column('level', sa.String, nullable=False),
    )
    with op.batch_alter_table('contents') as batch_op:
        batch_op.add_column(sa.Column('file_url', sa.String, nullable=True))
        batch_op.add_column(sa.Column('category_id', sa.Integer, nullable=True))
        batch_op.create_foreign_key('fk_contents_category_id', 'categories', ['category_id'], ['id'])

def downgrade():
    with op.batch_alter_table('contents') as batch_op:
        batch_op.drop_constraint('fk_contents_category_id', type_='foreignkey')
        batch_op.drop_column('category_id')
        batch_op.drop_column('file_url')
    op.drop_table('quizzes')
    op.drop_table('categories') 