#МОДУЛЬ ОБНОВЛЕНИЯ В DataBase

from database.database_connect import get_connection


class UpdateOperations:
    @staticmethod
    def update_product_info(company, warehouse, name_category, name_product, new_quantity, new_price, new_supplier) -> bool:
        """ОБНОВЛЕНИЕ quantity, price, supplier"""
        conn = get_connection()
        if not conn:
            return False

        query = """
            UPDATE public.warehouse
            SET quantity = quantity + %s,
                price = %s,
                supplier = %s
            WHERE name_company = %s
            AND name_warehouse = %s
            AND name_category = %s
            AND name_product = %s
        """

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    new_quantity, new_price, new_supplier,
                    company, warehouse, name_category, name_product
                ))
                conn.commit()

                if cursor.rowcount == 0:
                    print('ТОВАР НЕ НАЙДЕН НИЧЕГО НЕ ОБНОВЛЕННО')
                    return False
                return True


        except Exception as e:
            print(f'ОШИБКА UPDATE {e}')
            return False
        finally:
            conn.close()




if __name__ == '__main__':
    res = UpdateOperations.update_product_info('ANGEL', 'Склад_1', 'ТВ', 'GIRL', 67, 67, 'YAVA')
    print(f"Обновление успешно: {res}")
