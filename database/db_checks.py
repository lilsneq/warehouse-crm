#МОДУЛЬ ПРОВЕРОК ВХОЖДЕНИЙ
import psycopg2
from database_connect import get_connection
from datetime import datetime


now = datetime.now()


def check_exists(company, warehouse, product):
    """ПРОВЕРКА ВХОЖДЕНИЯ ТОВАРА В БАЗУ ДАННЫХ"""
    conn = None

    try:
        conn = get_connection()
        if not conn:
            return False

        query = """
            SELECT 1 FROM public.warehouse
            WHERE name_company = %s AND name_warehouse = %s AND name_product = %s
            LIMIT 1;
        """
        print(f'Запрос отправлен в базу данных', now)

        with conn.cursor() as cursor:
            cursor.execute(query, (company, warehouse, product))
            exists = cursor.fetchone() is not None
            return exists

    except Exception as e:
        print(f'ОШИБКА МОДУЛЯ ПРОВЕРКИ check.py - {e}', now)
        return False
    finally:
        if conn:
            conn.close()



if __name__ == '__main__':
    #ТЕСТ ПРОВЕРКА ВХОЖДЕНИЯ ТОВАРА
    test_res = check_exists('LG', 'Основной', 'ВИЛКА')
    print(f"Результат проверки: {'Найдено' if test_res else 'Не найдено'}")

