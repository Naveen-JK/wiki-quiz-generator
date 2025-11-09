"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create wikipedia_articles table
    op.create_table('wikipedia_articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('key_entities', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sections', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('quiz_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('related_topics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('raw_html', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_wikipedia_articles_id'), 'wikipedia_articles', ['id'], unique=False)
    op.create_index(op.f('ix_wikipedia_articles_url'), 'wikipedia_articles', ['url'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_wikipedia_articles_url'), table_name='wikipedia_articles')
    op.drop_index(op.f('ix_wikipedia_articles_id'), table_name='wikipedia_articles')
    op.drop_table('wikipedia_articles')