#МОДУЛЬ ПОИСКА
from database.database_connect import get_connection

class ViewAllOperations:

    @staticmethod
    def find_product():
        conn = get_connection()
        if not conn:
            return []

        query = """
            SELECT * FROM public.warehouse
            ORDER BY id ASC;
            """
        print("ЗАПРОС В БАЗУ ДАННЫХ ОТПРАВЛЕН")

        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows

        except Exception as e:
            print(f'ОШИБКА ПОЛУЧЕНИЯ ДАННЫХ {e}')
            return []
        finally:
            conn.close()




if __name__ == '__main__':
    rows = ViewAllOperations.find_product()
    col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]

    # 2. Печатаем строки
    for row in rows:
        # ljust(col_widths[i]) выравнивает по левому краю с нужным отступом
        formatted_row = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
        print(f"| {formatted_row} |")

