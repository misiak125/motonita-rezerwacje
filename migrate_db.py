from alembic.config import Config
from alembic import command
import os

def run_migrations():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))

    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()