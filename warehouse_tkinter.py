import tkinter as tk
import time

from tkinter import ttk, scrolledtext
from warehouse_system import (
    ProductQuantity,
    ProductAdd,
    ProductFind,
    ProductSell,
    ProductAdd,
    ViewAllProducts,
    companies_for_warehouse

)




def show_products(companies):
    viewer = ViewAllProducts(companies_for_warehouse)

    #настройка тегов
    text_area.tag_config("company", foreground="blue", font=("Arial", 12, "bold"))
    text_area.tag_config("warehouse", foreground="green", font=("Arial", 10, "bold"))
    text_area.tag_config("category", foreground="purple", font=("Arial", 9, "italic"))

    #очистка и редактирование
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)

    total_items = 0
    total_value = 0

    for company in companies_for_warehouse:
        text_area.insert(tk.END, f"\n{'=' * 70}\n", "company")
        text_area.insert(tk.END, f"🏢 КОМПАНИЯ: {company}\n", "company")

        for warehouse in companies_for_warehouse[company]:
            text_area.insert(tk.END, f"\n  📦 СКЛАД: {warehouse}\n", "warehouse")

            for category in companies_for_warehouse[company][warehouse]:
                text_area.insert(tk.END, f"\n    📁 КАТЕГОРИЯ: {category}\n", "category")

                for product, data in companies_for_warehouse[company][warehouse][category].items():
                    qty = data['quantity']
                    price = data['price']
                    total_items += qty
                    total_value += qty * price

                    text_area.insert(tk.END,f"      • {product}: {qty} шт, {price} ₽, поставщик: {data['supplier']}\n")


    text_area.insert(tk.END, f"\n{'=' * 70}\n", "company")
    text_area.insert(tk.END, f"ИТОГО: {total_items} товаров на сумму {total_value} ₽\n")
    text_area.insert(tk.END, f"Обновлено: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    text_area.config(state=tk.DISABLED)


def add_product_gui():
    new_window = tk.Toplevel(root)
    new_window.title("Добавить")
    new_window.geometry("500x600")
    fields = [
        ("Компания:", "company"),
        ("Склад:", "warehouse"),
        ("Категория:", "category"),
        ("Товар:", "product"),
        ("Количество:", "quantity"),
        ("Цена:", "price"),
        ("Поставщик:", "supplier")
    ]
    # Создать таблицу

    entries = {}
    for label_text, key in fields:
        tk.Label(new_window, text=label_text).pack()
        entry = tk.Entry(new_window)
        entry.pack()
        entries[key] = entry

    def save_product():
        company = entries['company'].get()
        warehouse = entries['warehouse'].get()
        category = entries['category'].get()
        product = entries['product'].get()
        quantity = entries['quantity'].get()
        price = entries['price'].get()
        supplier = entries['supplier'].get()

        if not all([company, warehouse, category, product, quantity, price, supplier]):
            print("Ошибка: все поля должны быть заполнены")
            return

        adder = ProductAdd()
        adder.add_a_new_product(company, warehouse, category, product,
                                int(quantity), int(price), supplier)

        new_window.destroy()
        show_products(companies_for_warehouse)
        print(f"Товар добавлен: {product} в {company}/{warehouse}")


    tk.Button(new_window, text="❌ Отмена", command=new_window.destroy).pack()
    tk.Button(new_window, text="✅ Добавить", command=save_product).pack(pady=10)


def export_to_file():
    print("Функция экспорта будет добавлена")


def search_products():
    print("Функция поиска будет добавлена")


# Создание главного окна
root = tk.Tk()
root.title("📦 Управление складом")
root.geometry("900x700")


title = ttk.Label(root, text="CRM СИСТЕМА СКЛАДА", font=("Arial", 16))
title.pack(pady=10)

# Кнопки
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

btn1 = ttk.Button(btn_frame, text="📦 Показать товары", command=lambda: show_products(companies_for_warehouse))
btn1.pack(side=tk.LEFT, padx=5)

btn2 = ttk.Button(btn_frame, text="➕ Добавить товар", command=add_product_gui)
btn2.pack(side=tk.LEFT, padx=5)

btn3 = ttk.Button(btn_frame, text="🚪 Выход", command=root.destroy)
btn3.pack(side=tk.LEFT, padx=5)

# Текстовое поле для вывода
text_area = scrolledtext.ScrolledText(root, width=70, height=40, font=("Courier New", 20), wrap=tk.NONE, xscrollcommand=True)
text_area.pack(pady=10)



# Добавить в основное окно
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

tk.Button(button_frame, text="🔄 Обновить",
          command=lambda: show_products(companies_for_warehouse)).pack(side=tk.LEFT)
tk.Button(button_frame, text="💾 Экспорт",
          command=export_to_file).pack(side=tk.LEFT)  # нужно создать функцию
tk.Button(button_frame, text="🔍 Поиск",
          command=search_products).pack(side=tk.LEFT)  # нужно создать функцию



print("Окно создано")
root.mainloop()