# Иерархия: Компания → Склад → Категория → Товар
# Система управления складом версия 2.0
from curses.ascii import isdigit
from os import pread
from tkinter.font import names

companies_for_warehouse = {
    'TechCorp': {
        'main_warehouse': {
            'electronics': {
                'laptops': {'quantity': 150, 'price': 800, 'supplier': 'Dell'},
                'phones': {'quantity': 300, 'price': 500, 'supplier': 'Apple'}
            },
            'components': {
                'processors': {'quantity': 500, 'price': 300, 'supplier': 'Intel'},
                'memory': {'quantity': 1000, 'price': 100, 'supplier': 'Samsung'}
            }
        },
        'regional_warehouse': {
            'electronics': {
                'laptops': {'quantity': 50, 'price': 800, 'supplier': 'Dell'},
                'monitors': {'quantity': 80, 'price': 200, 'supplier': 'LG'}
            }
        }
    },
    'BuildMaster': {
        'central_warehouse': {
            'materials': {
                'bricks': {'quantity': 10000, 'price': 1, 'supplier': 'BrickCo'},
                'cement': {'quantity': 5000, 'price': 10, 'supplier': 'CementLtd'}
            },
            'tools': {
                'hammers': {'quantity': 200, 'price': 15, 'supplier': 'ToolPro'},
                'drills': {'quantity': 150, 'price': 80, 'supplier': 'Bosch'}
            }
        }
    }
}


class ProductQuantity:
    """НАИБОЛЬШЕЕ КОЛИЧЕСТВО ТОВАРА НА СКЛАДЕ"""
    def __init__(self, companies_data):
        self.companies = companies_data


    def total_quantity_of_goods(self, product_name):
        """Общее количество товара по названию во всех складах"""

        total = 0

        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    if product_name in self.companies[company][warehouse][category]:
                        total += self.companies[company][warehouse][category][product_name]['quantity']

        return total


class ProductFind:
    """ПОИСК САМОГО ДОРОГОГО ТОВАРА КОМПАНИИ"""
    def __init__(self, companies_data):
        self.companies = companies_data


    def _check_company(self, company):
        """Проверка компании"""
        return company in self.companies


    def Find_the_most_expensive_product_in_the_company(self, company):
        """Найти самый дорогой товар в компании"""
        if not self._check_company(company):
            return None

        max_price = 0
        product_info = {}

        for warehouse in self.companies[company]:
            for category in self.companies[company][warehouse]:
                for products in self.companies[company][warehouse][category]:
                    price = self.companies[company][warehouse][category][products]['price']

                    if price > max_price:
                        max_price = price
                        product_info =  {
                            'warehouse': warehouse,
                            'category': category,
                            'products': products,
                            'price': price,
                            'quantity': self.companies[company][warehouse][category][products]['quantity']
                        }

        return product_info


class ProductAdd:
    """ДОБАВЛЕНИЕ ТОВАРА"""
    def add_a_new_product(self, name_company, name_warehouse, name_category, name_product,
                         name_quantity, name_price, name_supplier):
        """Добавить новый товар"""

        global companies_for_warehouse

        if name_company not in companies_for_warehouse:
            companies_for_warehouse[name_company] = {}
        if name_warehouse not in companies_for_warehouse[name_company]:
            companies_for_warehouse[name_company][name_warehouse] = {}
        if name_category not in companies_for_warehouse[name_company][name_warehouse]:
            companies_for_warehouse[name_company][name_warehouse][name_category] = {}

        if name_quantity <= 0:
            return (False, "Количество должно быть положительным")

        #если товар всё таки есть
        if name_product in companies_for_warehouse[name_company][name_warehouse][name_category]:
            companies_for_warehouse[name_company][name_warehouse][name_category][name_product]["quantity"] += name_quantity
            companies_for_warehouse[name_company][name_warehouse][name_category][name_product]['price'] = name_price
            companies_for_warehouse[name_company][name_warehouse][name_category][name_product]["supplier"] = name_supplier
            return (True, 'Товар обновлён')

        #если товара нет
        companies_for_warehouse[name_company][name_warehouse][name_category][name_product] = {
            'quantity': name_quantity,
            'price': name_price,
            'supplier': name_supplier
                    }
        return (True, 'Товар добавлен')


class ProductSell:
    """ПРОДАЖА ТОВАРА"""
    def set_sale_data(self, company, warehouse, category, product, quantity):
        self.name_company = company
        self.name_warehouse = warehouse
        self.name_category = category
        self.name_product = product

        if quantity.isdigit():
            self.name_quantity = int(quantity)


    def sell_product(self):
        """Продать товар"""
        if not self.name_company:
            return False
        if not self.name_warehouse:
            return False
        if not self.name_category:
            return False
        if not self.name_product:
            return False
        if not self.name_quantity:
            return False
        if not self._check_company():
            return False
        if not self._check_warehouse():
            return False
        if not self._check_category():
            return False
        if not self._check_product():
            return False
        if not self._check_quantity():
            return False

        self._update_quantity()
        self._check_if_empty_and_delete()
        return True



    def _check_company(self):
        """Проверка компании"""
        return self.name_company in companies_for_warehouse


    def _check_warehouse(self):
        """Проверка склада"""
        return self.name_warehouse in companies_for_warehouse[self.name_company]


    def _check_category(self):
        """Проверка категории"""
        return self.name_category in companies_for_warehouse[self.name_company][self.name_warehouse]


    def _check_product(self):
        """Проверка продукта"""
        return self.name_product in companies_for_warehouse[self.name_company][self.name_warehouse][self.name_category]


    def _check_quantity(self):
        """Проверка количества"""
        product = companies_for_warehouse[self.name_company][self.name_warehouse][self.name_category][self.name_product]['quantity']
        return self.name_quantity <= product


    def _update_quantity(self):
        """Вычитание товара из количества"""
        product = companies_for_warehouse[self.name_company][self.name_warehouse][self.name_category][self.name_product]
        product["quantity"] -= self.name_quantity


    def _check_if_empty_and_delete(self):
        """Удаление товара если его меньше 0"""
        if companies_for_warehouse[self.name_company][self.name_warehouse][self.name_category][self.name_product]["quantity"] <= 0:
            del companies_for_warehouse[self.name_company][self.name_warehouse][self.name_category][self.name_product]



class FindSupplier:
    """Найти поставщика с наибольшим общим количеством товаров"""
    def __init__(self, companies_data):
        self.companies = companies_data


    def find_the_supplier_with_the_highest_total_quantity_of_goods(self):
        """Поиск поставщика"""
        supplier_totals = {}

        if not supplier_totals:
            return None

        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product in self.companies[company][warehouse][category]:
                        supplier_x = self.companies[company][warehouse][category][product]['supplier']
                        quantity_x = self.companies[company][warehouse][category][product]['quantity']
                        if supplier_x not in supplier_totals:
                            supplier_totals[supplier_x] = 0
                        supplier_totals[supplier_x] += quantity_x


        best_supplier = max(supplier_totals.items(), key=lambda x: x[1])
        return best_supplier


class ViewAllProducts:
    """Просмотреть все товары с детальной информацией"""
    def __init__(self, companies_data):
        self.companies = companies_data



    def view_all_products_with_detailed_information(self):
        """Просмотреть все товары"""
        result_text = ""
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product in self.companies[company][warehouse][category]:
                        data = self.companies[company][warehouse][category][product]
                        result_text += f"{company}/{warehouse}/{category}/{product}: "
                        result_text += f"{data['quantity']} шт × {data['price']} ₽ = {data['quantity'] * data['price']} ₽ "
                        result_text += f"({data['supplier']})\n"
        return result_text


class FindAProduct:
    """Поиск продукта по складу"""
    def __init__(self, companies_data):
        self.companies = companies_data


    def search_by_product_name(self, name):
        """Поиск названия"""
        result_text = []
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product,data in self.companies[company][warehouse][category]:
                        if name == product:
                            result_text.append({
                                        'company': company,
                                        'warehouse': warehouse,
                                        'category': category,
                                        'product': product,
                                        'quantity': data['quantity'],
                                        'price': data['price'],
                                        'supplier': data['supplier']
                                    })
        return result_text


    def search_by_company(self, company):
        """все товары компании"""
        result_text = []
        if company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product,data in self.companies[company][warehouse][category]:
                        result_text.append({
                            'company': company,
                            'warehouse': warehouse,
                            'category': category,
                            'product': product,
                            'quantity': data['quantity'],
                            'price': data['price'],
                            'supplier': data['supplier']
                        })

        return result_text


    def search_by_supplier(self, supplier):
        """поиск по поставщику"""
        result_text = []
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product, data in self.companies[company][warehouse][category]:
                        if supplier == data['supplier']:
                            result_text.append({
                                        'company': company,
                                        'warehouse': warehouse,
                                        'category': category,
                                        'product': product,
                                        'quantity': data['quantity'],
                                        'price': data['price'],
                                        'supplier': data['supplier']
                                    })
        return result_text


    def search_by_price_range(self, min_price, max_price):
        """товары в ценовом диапазоне"""
        result_text = []
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product, data in self.companies[company][warehouse][category]:
                        if min_price <= data['price'] <= max_price:
                            result_text.append({
                                        'company': company,
                                        'warehouse': warehouse,
                                        'category': category,
                                        'product': product,
                                        'quantity': data['quantity'],
                                        'price': data['price'],
                                        'supplier': data['supplier']
                                    })
        return result_text


    def search_by_quantity_range(self, min_qty, max_qty):
        """товары по количеству"""
        result_text = []
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product, data in self.companies[company][warehouse][category]:
                        if min_qty <= data['quantity'] <= max_qty:
                            result_text.append({
                                        'company': company,
                                        'warehouse': warehouse,
                                        'category': category,
                                        'product': product,
                                        'quantity': data['quantity'],
                                        'price': data['price'],
                                        'supplier': data['supplier']
                                    })
        return result_text


