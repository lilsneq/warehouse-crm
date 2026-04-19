#МОДУЛЬ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ

import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)


def get_connection() -> psycopg2.connect:
    """ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ"""
    url = os.getenv("DB_HOST")
    if not url:
        print('ОШИБКА: нет ключа .env')
        return None


    try:
        conn = psycopg2.connect(url)
        return conn

    except Exception as e:
        print(f'ОШИБКА ПРИ ПОДКЛЮЧЕНИИ К БАЗЕ ДАННЫХ: {e}')
        return None


if __name__ == '__main__':
    connection = get_connection()
    if connection:
        print('БАЗА ДАННЫХ ПОДКЛЮЧЕНА')
        connection.close()

