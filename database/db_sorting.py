# СОРТИРОВКА

from database.database_connect import get_connection

class SortedOperations:

    @staticmethod
    def get_sorting_monotone(sort_by='id', reverse=False):
        """СОРТИРОВКА ПО МОНОТОНОСТИ ОТ БОЛЬШЕГО ИЛИ ОТ МЕНЬШЕГО С ВЫБОРОМ ТАБЛИЦЫ СОРТИРОВКИ"""
        conn = get_connection()

        rev = 'DESC' if reverse else 'ASC'

        if not conn:
            return None

        query = f"SELECT * FROM public.warehouse ORDER BY {sort_by} {rev};"

        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

        except Exception as e:
            print(f'ОШИБКА СОРТИРОВКИ: {e}')
            return []
        finally:
            conn.close()




if __name__ == '__main__':
    rows = SortedOperations.get_sorting_monotone('name_product')
    col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]

    # 2. Печатаем строки
    for row in rows:
        # ljust(col_widths[i]) выравнивает по левому краю с нужным отступом
        formatted_row = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
        print(f"| {formatted_row} |")

