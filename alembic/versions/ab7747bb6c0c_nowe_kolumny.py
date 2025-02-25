"""nowe kolumny

Revision ID: ab7747bb6c0c
Revises: d314ba969295
Create Date: 2025-02-25 09:53:18.135767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab7747bb6c0c'
down_revision: Union[str, None] = 'd314ba969295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("customers") as batch_op:
        batch_op.add_column(sa.Column("pesel", sa.String))
        batch_op.add_column(sa.Column("nip", sa.String))

    
    with op.batch_alter_table("reservations") as batch_op:
        batch_op.add_column(sa.Column("paid", sa.Boolean, nullable=True))
        batch_op.add_column(sa.Column("form", sa.Boolean, nullable=True))


def downgrade() -> None:
    pass
