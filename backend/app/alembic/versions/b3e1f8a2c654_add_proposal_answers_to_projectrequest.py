"""add proposal answers to projectrequest

Revision ID: b3e1f8a2c654
Revises: a1f3c9e2d847
Create Date: 2026-06-03 12:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = 'b3e1f8a2c654'
down_revision: str | None = 'a1f3c9e2d847'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('projectrequest', sa.Column('question_answers', JSONB(), nullable=True))
    op.add_column('projectrequest', sa.Column('feasibility_scores', JSONB(), nullable=True))


def downgrade() -> None:
    op.drop_column('projectrequest', 'feasibility_scores')
    op.drop_column('projectrequest', 'question_answers')
