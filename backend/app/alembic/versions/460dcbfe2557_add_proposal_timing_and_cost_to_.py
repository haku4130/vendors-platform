"""add_proposal_timing_and_cost_to_projectrequest

Revision ID: 460dcbfe2557
Revises: b3e1f8a2c654
Create Date: 2026-06-05 10:31:04.033989

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '460dcbfe2557'
down_revision = 'b3e1f8a2c654'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('projectrequest', sa.Column('days_to_start', sa.Integer(), nullable=True))
    op.add_column('projectrequest', sa.Column('duration_days', sa.Integer(), nullable=True))
    op.add_column('projectrequest', sa.Column('proposed_cost', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('projectrequest', 'proposed_cost')
    op.drop_column('projectrequest', 'duration_days')
    op.drop_column('projectrequest', 'days_to_start')
