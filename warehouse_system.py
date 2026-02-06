# Иерархия: Компания → Склад → Категория → Товар
# Система управления складом версия 2.0

companies = {
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


MENU = ["1. Общее количество товара по названию во всех складах",
        "2. Найти самый дорогой товар в компании",
        "3. Добавить новый товар",
        "4. Продать товар",
        "5. Найти поставщика с наибольшим общим количеством товаров",
        "6. Просмотреть все товары с детальной информацией",
        "7. Выйти"
]


def total_quantity_of_goods():
    """Общее количество товара по названию во всех складах"""
    product_name = input("Введите название товара: ")
    total = 0

    for company in companies:
        for warehouse in companies[company]:
            for category in companies[company][warehouse]:
                if product_name in companies[company][warehouse][category]:
                    total += companies[company][warehouse][category][product_name]['quantity']

    print(f"Общее количетсво {product_name}: {total}")
    print()
    return total


def Find_the_most_expensive_product_in_the_company():
    """Найти самый дорогой товар в компании"""

    company_name = input("Ведите название компании: ")
    if company_name not in companies:
        print("Такой компании нет")
        print()
        return

    max_price = 0
    product_info = {}

    for warehouse in companies[company_name]:
        for category in companies[company_name][warehouse]:
            for products in companies[company_name][warehouse][category]:
                price = companies[company_name][warehouse][category][products]['price']

                if price > max_price:
                    max_price = price
                    product_info =  {
                        'warehouse': warehouse,
                        'category': category,
                        'products': products,
                        'price': price,
                        'quantity': companies[company_name][warehouse][category][products]['quantity']
                    }

    if product_info:
        print()
        print(f"Самый дорогой товар в {company_name}:")
        print(f"Склад: {product_info["warehouse"]}")
        print(f"Категория: {product_info["category"]}")
        print(f"Товар: {product_info["products"]}")
        print(f"Цена: {product_info["price"]}")
        print(f"Количество: {product_info["quantity"]}")
        print()


def add_a_new_product(name_company, name_warehouse, name_category, name_product,
                     name_quantity, name_price, name_supplier):
    """Добавить новый товар"""


    #если товара нет
    if name_company not in companies:
        companies[name_company] = {}
    if name_warehouse not in companies[name_company]:
        companies[name_company][name_warehouse] = {}
    if name_category not in companies[name_company][name_warehouse]:
        companies[name_company][name_warehouse][name_category] = {}

    #если товар всё таки есть
    if name_product in companies[name_company][name_warehouse][name_category]:
        print("1 - Добавить к существующему количеству")
        print("2 - Перезаписать товар")
        print("3 - Отмена")
        choice = input("Выберите действие: ")

        if choice == "1":
            companies[name_company][name_warehouse][name_category][name_product]["quantity"] += name_quantity

            update = input("Обновить цену и поставщика? (да/нет): ")
            if update.lower() == "да":
                companies[name_company][name_warehouse][name_category][name_product]['price'] = name_price
                companies[name_company][name_warehouse][name_category][name_product]["supplier"] = name_supplier

            print("КОЛИЧЕСТВО УСПЕШНО ОБНОВЛЕНО!")
            return

        elif choice == "2":
            print(f"Ваш товар перезаписан {name_quantity}")
            pass

        elif choice == "3":
            print("Вы вышли")
            return

        else:
            print("ОШИБКА")
            return

    companies[name_company][name_warehouse][name_category][name_product] = {
        'quantity': name_quantity,
        'price': name_price,
        'supplier': name_supplier
                }

def sell_product():
    """Продать товар"""
    name_company = input("Название компании: ")
    name_warehouse = input("Название склада: ")
    name_category = input("Категория: ")
    name_product = input("Название товара: ")
    name_quantity = int(input("Количество: "))

    if name_company in companies:
        if name_warehouse in companies[name_company]:
            if name_category in companies[name_company][name_warehouse]:
                if name_product in companies[name_company][name_warehouse][name_category]:
                    if name_quantity <= companies[name_company][name_warehouse][name_category][name_product]["quantity"]:
                        companies[name_company][name_warehouse][name_category][name_product]["quantity"] -= name_quantity
                        print(f"Продано {name_quantity} шт. | Осталось {companies[name_company][name_warehouse][name_category][name_product]["quantity"]}")

                        if companies[name_company][name_warehouse][name_category][name_product]["quantity"] <= 0:
                            print("Товара нет, вы хотите удалить его?: ")
                            del_user = input("да/нет")

                            if del_user.lower() == "да":
                                del companies[name_company][name_warehouse][name_category][name_product]

                            else:
                                return

                    else:
                        print("Товара не достаточно")
                else:
                    print("Продукт не найдет")
            else:
                print("Категория не найдена")
        else:
            print("Ошибка склад не найден")
    else:
        print("Ошибка компания не найдена")


def find_the_supplier_with_the_highest_total_quantity_of_goods():
    """Найти поставщика с наибольшим общим количеством товаров"""
    supplier_totals = {}

    for company in companies:
        for warehouse in companies[company]:
            for category in companies[company][warehouse]:
                for product in companies[company][warehouse][category]:
                    supplier_x = companies[company][warehouse][category][product]['supplier']
                    quantity_x = companies[company][warehouse][category][product]['quantity']
                    if supplier_x not in supplier_totals:
                        supplier_totals[supplier_x] = 0
                    supplier_totals[supplier_x] += quantity_x


    best_supplier = max(supplier_totals.items(), key=lambda x: x[1])
    print(f"{best_supplier[0]} | {best_supplier[1]}")
    print()


def view_all_products_with_detailed_information():
    """Просмотреть все товары с детальной информацией"""
    result_text = ""
    for company in companies:
        for warehouse in companies[company]:
            for category in companies[company][warehouse]:
                for product in companies[company][warehouse][category]:
                    # Добавь эту строку перед result_text += ...:
                    data = companies[company][warehouse][category][product]
                    result_text += f"{company}/{warehouse}/{category}/{product}: "
                    result_text += f"{data['quantity']} шт × {data['price']} ₽ = {data['quantity'] * data['price']} ₽ "
                    result_text += f"({data['supplier']})\n"
    return result_text

if __name__ == "__main__":
    while True:

        print(*MENU, sep="\n")
        print()
        try:
            user_input = int(input("Введите цифру для действия: "))
        except ValueError:
            print("Ошибка: введите число от 1 до 5")
            continue

        if user_input == 1:
            total_quantity_of_goods()

        elif user_input == 2:
            Find_the_most_expensive_product_in_the_company()

        elif user_input == 3:
            add_a_new_product()

        elif user_input == 4:
            sell_product()

        elif user_input == 5:
            find_the_supplier_with_the_highest_total_quantity_of_goods()

        elif user_input == 6:
            view_all_products_with_detailed_information()

        elif user_input == 7:
            break

