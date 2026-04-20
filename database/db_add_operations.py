#добавление в базу данных

from database.database_connect import get_connection
from datetime import datetime




class AddOperations:

    @staticmethod
    def add_product(company, warehouse, category, product=None, quantity=0, price=0, supplier=None):
        """ДОБАВЛЕНИЕ ТОВАРА В БАЗУ ДАННЫХ"""

        now = datetime.now()

        conn = get_connection()
        if not conn:
            return None

        query = """
            INSERT INTO public.warehouse
            (name_company, name_warehouse, name_category, name_product, quantity, price, supplier)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        print(f'ЗАПРОС ОТПРАВЛЕН В БАЗУ ДАННЫХ ', now)


        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (company, warehouse, category, product, quantity, price, supplier))
                new_id = cursor.fetchone()[0]
                conn.commit()
                print(f'ТОВАР ДОБАВЛЕН {new_id}', now)
                return new_id

        except Exception as e:
            print(f'ОШИБКА ДОБАВЛЕНИЯ В БАЗУ ДАННЫХ {e}', now)
            return None
        finally:
            conn.close()



if __name__ == '__main__':
    pass







