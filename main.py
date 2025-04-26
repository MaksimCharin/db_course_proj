from config import get_db_config
from src.db_manager import DBManager
from src.init_db import initialize_database
from src.utils import user_interface


def main() -> None:
    """Точка входа в программу"""
    db_config = get_db_config()

    initialize_database(db_config)

    user_manager = DBManager(db_config)
    user_interface(user_manager)
    user_manager.close()

if __name__ == "__main__":
    main()
