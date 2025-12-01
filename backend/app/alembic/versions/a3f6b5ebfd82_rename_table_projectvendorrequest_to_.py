"""Rename table ProjectVendorRequest to ProjectRequest

Revision ID: a3f6b5ebfd82
Revises: 19c46f12b705
Create Date: 2025-12-01 12:23:52.696898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = 'a3f6b5ebfd82'
down_revision = '19c46f12b705'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Создаем новый enum, если его еще нет
    request_initiator_enum = postgresql.ENUM('company', 'vendor', name='requestinitiator')
    request_initiator_enum.create(op.get_bind(), checkfirst=True)

    # 2. Переименовываем таблицу
    op.rename_table('projectvendorrequest', 'projectrequest')

    # 3. Добавляем новый столбец
    op.add_column(
        'projectrequest',
        sa.Column('initiator', sa.Enum('company', 'vendor', name='requestinitiator'), nullable=True)
    )

    # Если нужно — обновляем все старые строки (например, ставим default)
    op.execute("UPDATE projectrequest SET initiator = 'company'")

    # И теперь делаем NOT NULL
    op.alter_column('projectrequest', 'initiator', nullable=False)


def downgrade():
    # отменяем действия в обратном порядке
    op.alter_column('projectrequest', 'initiator', nullable=True)
    op.drop_column('projectrequest', 'initiator')

    op.rename_table('projectrequest', 'projectvendorrequest')

    request_initiator_enum = postgresql.ENUM('company', 'vendor', name='requestinitiator')
    request_initiator_enum.drop(op.get_bind(), checkfirst=True)
