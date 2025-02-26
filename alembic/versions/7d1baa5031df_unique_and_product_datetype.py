"""unique and product datetype

Revision ID: 7d1baa5031df
Revises: ab7747bb6c0c
Create Date: 2025-02-26 15:20:00.327260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '7d1baa5031df'
down_revision: Union[str, None] = 'ab7747bb6c0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(sa.Column("expected_delivery_temp", sa.DateTime()))
        batch_op.add_column(sa.Column("old_price", sa.Float()))

    connection = op.get_bind()
    products_table = table(
        "products",
        column("id", sa.Integer),
        column("expected_delivery", sa.String),
        column("expected_delivery_temp", sa.DateTime),
        column("old_price", sa.Float),
        column("price", sa.Float)
    )

    results = connection.execute(sa.select(products_table.c.id, products_table.c.expected_delivery))
    for row in results:
        try:
            new_date = datetime.strptime(row.expected_delivery, "%d.%m.%Y")  
        except (ValueError, TypeError):
            new_date = None 
        
        connection.execute(
            products_table.update().where(products_table.c.id == row.id).values(expected_delivery_temp=new_date, old_price=row.price)
        )

    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("expected_delivery")
        batch_op.alter_column("expected_delivery_temp", new_column_name="expected_delivery")

    with op.batch_alter_table("brands") as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False, unique=True)
    
    with op.batch_alter_table("colours") as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False, unique=True)


    with op.batch_alter_table("models") as batch_op:
        batch_op.alter_column("namehash", existing_type=sa.String(), unique=True)


def downgrade():
    with op.batch_alter_table("brands") as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False, unique=False)
    
    with op.batch_alter_table("colours") as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False, unique=False)
    
    with op.batch_alter_table("models") as batch_op:
        batch_op.alter_column("namehash", existing_type=sa.String(), unique=False)

    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(sa.Column("expected_delivery_temp", sa.String))

    connection = op.get_bind()
    products_table = table(
        "products",
        column("id", sa.Integer),
        column("expected_delivery", sa.DateTime),
        column("expected_delivery_temp", sa.String),
    )

    results = connection.execute(sa.select(products_table.c.id, products_table.c.expected_delivery))
    for row in results:
        connection.execute(
            products_table.update()
            .where(products_table.c.id == row.id)
            .values(expected_delivery_temp=row.expected_delivery.strftime("%d.%m.%Y") if row.expected_delivery else None)
        )

    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("expected_delivery")
        batch_op.drop_column("old_price")
        batch_op.alter_column("expected_delivery_temp", new_column_name="expected_delivery")


