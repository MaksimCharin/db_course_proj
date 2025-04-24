from dotenv import load_dotenv
import os

def get_db_config():
    """Получение конфигурации базы данных из переменных окружения"""
    load_dotenv()
    db_config = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'client_encoding': os.getenv('DB_CLIENT_ENCODING')
    }
    return db_config
