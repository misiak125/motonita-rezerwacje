"""rewizja4

Revision ID: d314ba969295
Revises: 
Create Date: 2025-02-22 23:16:10.807315

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = 'd314ba969295'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    with op.batch_alter_table("models") as batch_op:
        batch_op.add_column(sa.Column("namehash", sa.String, nullable=True))

    connection = op.get_bind()
    models_table = table(
        "models",
        column("id", sa.Integer),
        column("brand_id", sa.Integer),
        column("name", sa.String),
        column("namehash", sa.String),
    )

    results = connection.execute(sa.select(models_table.c.id, models_table.c.brand_id, models_table.c.name))
    for row in results:
        hash_value = f"{row.brand_id}$^{row.name}"
        connection.execute(
            models_table.update().where(models_table.c.id == row.id).values(namehash=hash_value)
        )

    with op.batch_alter_table("models") as batch_op:
        batch_op.alter_column("namehash", existing_type=sa.String, nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("models") as batch_op:
        batch_op.drop_column("namehash")
