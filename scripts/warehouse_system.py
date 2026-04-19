# Иерархия: Компания → Склад → Категория → Товар
# Система управления складом версия 2.0
from data.json_storage import JSONStorage



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


class ProductFindMax:
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
    """method for adding a product to a dictionary"""
    def __init__(self, companies_data: dict, storage=None):
        """
        Args:
            companies_data (dict): dictionary with companies data
            storage (dict): dictionary with storage data
        """
        self._companies = companies_data
        self._storage = storage or JSONStorage()

    def add_a_new_product(self, name_company, name_warehouse, name_category, name_product,
                         name_quantity, name_price, name_supplier) -> bool:
        """
        Args:
            name_company (str): name of the company
            name_warehouse (str): name of the warehouse
            name_category (str): name of the category
            name_product (str): name of the product
            name_quantity (int): quantity of the product
            name_price (int): price of the product
            name_supplier (str): name of the supplier
        Returns:
            bool: True if the product was added
        """

        if name_company not in self._companies:
            self._companies[name_company] = {}
        if name_warehouse not in self._companies[name_company]:
            self._companies[name_company][name_warehouse] = {}
        if name_category not in self._companies[name_company][name_warehouse]:
            self._companies[name_company][name_warehouse][name_category] = {}

        if name_quantity <= 0:
            return False

        products = self._companies[name_company][name_warehouse][name_category]
        #If the item is still there, we will exchange it.
        if name_product in products:
            products[name_product]["quantity"] += name_quantity
            products[name_product]['price'] = name_price
            products[name_product]["supplier"] = name_supplier
            return True

        # if there is no cheese, we create it
        products[name_product] = {
            'quantity': name_quantity,
            'price': name_price,
            'supplier': name_supplier
                        }
        self._storage.save_data_json(self._companies)
        return True


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

        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product in self.companies[company][warehouse][category]:
                        supplier_x = self.companies[company][warehouse][category][product]['supplier']
                        quantity_x = self.companies[company][warehouse][category][product]['quantity']
                        if not supplier_totals:
                            return None
                        if supplier_x not in supplier_totals:
                            supplier_totals[supplier_x] = 0
                        supplier_totals[supplier_x] += quantity_x


        best_supplier = max(supplier_totals.items(), key=lambda x: x[1])
        return best_supplier


class ViewAllProducts:
    """Просмотреть все товары с детальной информацией"""
    def __init__(self, companies_data):
        self._companies = companies_data

    # def _format_product(self, company, warehouse, category, product, data):
    #     """защищённый метод для форматирования строки"""
    #     total = data['quantity'] * data['price']
    #     return (f"{company}/{warehouse}/{category}/{product}: {data['quantity']} шт"
    #             f" × {data['price']} ₽ = {total} ₽ ({data['supplier']})\n")

    def view_all_products_with_detailed_information(self):
        """Просмотреть все товары"""
        result = ""
        for company in self._companies:
            for warehouse in self._companies[company]:
                for category in self._companies[company][warehouse]:
                    for product in self._companies[company][warehouse][category]:
                        data = self._companies[company][warehouse][category][product]
                        # result += self._format_product(company, warehouse, category, product, data)

        return result


class FindAProduct:
    """filter search"""
    def __init__(self, companies_data: dict):
        self.companies = companies_data
        self._search_name = ""
        self._search_company = ""
        self._search_supplier = ""
        self._min_price = 0
        self._max_price = float('inf')
        self._min_qty = 0
        self._max_qty = float('inf')
        self._last_results = []

    @property
    def results(self) -> list:
        """
        accepts and forms strings, int
        Returns:
            list: List of dictionaries with found products.
        """
        result_text = []
        for company in self.companies:
            for warehouse in self.companies[company]:
                for category in self.companies[company][warehouse]:
                    for product,data in self.companies[company][warehouse][category].items():

                        if self._matches_criteria(company, product, data):
                            result_text.append({
                                        'company': company,
                                        'warehouse': warehouse,
                                        'category': category,
                                        'product': product,
                                        'quantity': data['quantity'],
                                        'price': data['price'],
                                        'supplier': data['supplier']
                                    })
        self._last_results = result_text
        return result_text

    def _matches_criteria(self, company: str, product: str, data: dict) -> bool:
        """
        Checking that all criteria are met
        Args:
            company (str): Company name
            product (str): Product name
            data (dict): Product data (quantity, price, supplier)
        Returns:
            bool: True if the product meets all criteria, otherwise False
        """

        # Search by name
        if self._search_name:
            name_match = self._search_name.lower().strip() == product.lower().strip()
            if not name_match:
                return False

        # Search by company
        if self._search_company:
            company_match = self._search_company.lower().strip() == company.lower().strip()
            if not company_match:
                return False

        # Search by supplier
        if self._search_supplier:
            supplier_match = self._search_supplier.lower().strip() == data['supplier'].lower().strip()
            if not supplier_match:
                return False

        # Search by price
        price_match = self._min_price <= data['price'] <= self._max_price
        if not price_match:
            return False

        # Search by quantity
        quantity_match = self._min_qty <= data['quantity'] <= self._max_qty
        if not quantity_match:
            return False

        return True

    #getter and setter properties
    @property
    def name(self) -> str:
        return self._search_name.lower().strip()

    @name.setter
    def name(self, name: str) -> None:
        self._search_name = name

    @property
    def company(self) -> str:
        return self._search_company.lower().strip()

    @company.setter
    def company(self, company: str) -> None:
        self._search_company = company

    @property
    def supplier(self) -> str:
        return self._search_supplier.lower().strip()

    @supplier.setter
    def supplier(self, supplier: str) -> None:
        self._search_supplier = supplier

    @property
    def price_range(self) -> tuple:
        return self._min_price, self._max_price

    @price_range.setter
    def price_range(self, prices: tuple) -> None:
        self._min_price, self._max_price = prices

    @property
    def quantity_range(self) -> tuple:
        return self._min_qty, self._max_qty

    @quantity_range.setter
    def quantity_range(self, quantities: tuple) -> None:
        self._min_qty, self._max_qty = quantities

    def reset(self) -> None:
        """reset criterion"""
        self._search_name = ""
        self._search_company = ""
        self._search_supplier = ""
        self._min_price = 0
        self._max_price = float('inf')
        self._min_qty = 0
        self._max_qty = float('inf')


def load_data_from_file():
    """Loading data from a JSON file on startup"""
    global companies_for_warehouse
    storage = JSONStorage()
    filepath = 'warehouse_data.json'
    success, result = storage.load_data()

    if success and result:
        companies_for_warehouse = result
        print("Данные загружены из JSON")
    else:
        print("Используются тестовые данные")

def export_to_file():
    """Saving data to a JSON file (called from the GUI)"""
    global companies_for_warehouse
    storage = JSONStorage()
    success, message = storage.save_data_json(companies_for_warehouse)
    return success, message


load_data_from_file()



