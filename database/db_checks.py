#МОДУЛЬ ПРОВЕРОК ВХОЖДЕНИЙ

import psycopg2
from database.database_connect import get_connection
from datetime import datetime



class CheckProduct:
    # КЛАСС ПРОВЕРКИ ТОВАРА В БД ПО 4 КРИТЕРИЯМ
    @staticmethod
    def check_exists(company, warehouse, category, product):
        """ПРОВЕРКА ВХОЖДЕНИЯ ТОВАРА В БАЗУ ДАННЫХ"""
        now = datetime.now()
        conn = None

        try:
            conn = get_connection()
            if not conn:
                return False

            query = """
                SELECT 1 FROM public.warehouse
                WHERE name_company = %s 
                    AND name_warehouse = %s
                    AND name_category = %s
                    AND name_product = %s
                LIMIT 1;
            """
            print(f'Запрос отправлен в базу данных', now)

            with conn.cursor() as cursor:
                cursor.execute(query, (company, warehouse, category, product))
                exists = cursor.fetchone() is not None
                if cursor.rowcount == 0:
                    print('ТОВАР НЕ НАЙДЕН НИЧЕГО НЕ ОБНОВЛЕННО')
                    return False
                return exists

        except Exception as e:
            print(f'ОШИБКА МОДУЛЯ ПРОВЕРКИ check.py - {e}', now)
            return False
        finally:
            if conn:
                conn.close()



if __name__ == '__main__':
    #ТЕСТ ПРОВЕРКА ВХОЖДЕНИЯ ТОВАРА
    res = check_exists('LG', 'Склад_1', 'ТВ', 'OLED55')
    print(f"Обновление успешно: {res}")

