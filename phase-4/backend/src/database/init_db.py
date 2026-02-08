"""
Initialize the database with required tables.
"""
from .migrations import create_db_and_tables


def init_db():
    """
    Initialize the database by creating all required tables.
    """
    create_db_and_tables()


if __name__ == "__main__":
    init_db()