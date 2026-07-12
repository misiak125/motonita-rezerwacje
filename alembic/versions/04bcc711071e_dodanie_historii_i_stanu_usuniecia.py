"""Dodanie historii i stanu usuniecia

Revision ID: 04bcc711071e
Revises: e9e9b4edc2af
Create Date: 2026-07-12 19:01:53.203299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04bcc711071e'
down_revision: Union[str, None] = 'e9e9b4edc2af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    target_tables = ['products', 'customers', 'reservations']
    
    for table_name in target_tables:
        # Używamy batch_alter_table, co jest kluczowe dla pełnej stabilności w SQLite
        with op.batch_alter_table(table_name) as batch_op:
            # server_default automatycznie uzupełni dotychczasowe rekordy w bazie danych
            batch_op.add_column(
                sa.Column('history', sa.String(), nullable=False, server_default='Local')
            )
            batch_op.add_column(
                sa.Column('deleted', sa.Boolean(), nullable=False, server_default='0')
            )


def downgrade() -> None:
    target_tables = ['products', 'customers', 'reservations']
    
    for table_name in target_tables:
        with op.batch_alter_table(table_name) as batch_op:
            # Wycofanie migracji - bezpieczne usunięcie kolumn w trybie wsadowym
            batch_op.drop_column('history')
            batch_op.drop_column('deleted')
