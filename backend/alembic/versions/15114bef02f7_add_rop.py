"""add rop

Revision ID: 15114bef02f7
Revises: c8a89c2c354f
Create Date: 2026-02-13 05:44:45.253346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15114bef02f7'
down_revision = 'c8a89c2c354f'
branch_labels = None
depends_on = None


def upgrade():
    # 1) добавляем колонку как nullable
    op.add_column("olympics_rows", sa.Column("rop", sa.String(), nullable=True))

    # 2) заполняем дефолтом для старых строк (временно)
    op.execute("UPDATE olympics_rows SET rop = 'UNKNOWN' WHERE rop IS NULL")

    # 3) делаем NOT NULL
    op.alter_column("olympics_rows", "rop", nullable=False)

def downgrade():
    op.drop_column("olympics_rows", "rop")
