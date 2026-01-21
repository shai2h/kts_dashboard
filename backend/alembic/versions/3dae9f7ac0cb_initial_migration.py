from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3dae9f7ac0cb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('kts_manager_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manager', sa.String(), nullable=False),
    sa.Column('podr', sa.String(), nullable=False),
    sa.Column('plan', sa.Numeric(precision=18, scale=2), nullable=False),
    sa.Column('tec', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('procent', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('kts_manager_plan')
