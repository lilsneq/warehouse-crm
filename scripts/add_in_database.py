# МОДУЛЬ ДОБАВЛЕНИЕ В БУЗУ ДАННЫХ ТОВАРА



from database.db_add_operations import AddOperations

from datetime import datetime


class AddInDatabase:
    # ДОБАВЛЕНИЕ ДОВАРА В БАЗУ ДАННЫХ

    def add_a_new_product(self, name_company, name_warehouse, name_category,
                          name_product, quantity=0, price=0, supplier=None) -> bool:

        """
        ДОБАВЛЕНИЕ ТОВАРА В PostgreSQL
        :param name_company: :param name_warehouse: :param name_category: :param name_product:
        :param quantity: :param price: :param supplier: :return:
        """
        now = datetime.now()

        if quantity <= 0:
            print('ОШИБКА: КОЛИЧЕСТВО ДОЛЖНО БЫТЬ МЕНЬШЕ НУЛЯ', now)
            return False

        new_id = AddOperations.add_product(
            company=name_company,
            warehouse=name_warehouse,
            category=name_category,
            product=name_product,
            quantity=quantity,
            price=price,
            supplier=supplier
        )

        if new_id:
            print("НОВЫЙ ТОВАР ДОБАВЛЕН", now)
            return True
        return False



if __name__ == '__main__':
    #ПРОВЕРКА ОТПРАВЛЯЕТСЯ ЛИ ЗАПРОС ДОБАВЛЕНИЯ В БД
    service = AddInDatabase()
    result = service.add_a_new_product('ANGEL', 'Склад_1', 'ТВ', 'GIRL', 1, 50000, 'Тест_Поставщика')
    print("ЗАПРОС ОТПРАВЛЕН")




