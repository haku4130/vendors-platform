"""Migrate requirements from JSON-encoded strings to JSONB objects

Revision ID: a1f3c9e2d847
Revises: 0566a24719c6
Create Date: 2026-06-01 00:00:00.000000

"""
from alembic import op

revision = 'a1f3c9e2d847'
down_revision = '0566a24719c6'
branch_labels = None
depends_on = None


def upgrade():
    # Each element in requirements was stored as a JSON-encoded string
    # (e.g. '"{\\"group\\":\\"...\\"}"'). Convert each string element to
    # the actual JSONB object it encodes.
    op.execute("""
        UPDATE project
        SET requirements = (
            SELECT jsonb_agg(
                CASE
                    WHEN jsonb_typeof(elem) = 'string'
                    THEN (elem #>> '{}')::jsonb
                    ELSE elem
                END
            )
            FROM jsonb_array_elements(requirements) AS elem
        )
        WHERE jsonb_typeof(requirements) = 'array'
    """)


def downgrade():
    # Re-encode each object element back to a JSON string.
    op.execute("""
        UPDATE project
        SET requirements = (
            SELECT jsonb_agg(to_jsonb(elem::text))
            FROM jsonb_array_elements(requirements) AS elem
        )
        WHERE requirements IS NOT NULL
    """)
