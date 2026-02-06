import tkinter as tk

from tkinter import ttk, scrolledtext
from warehouse_system import (
    companies,
    view_all_products_with_detailed_information,
    add_a_new_product,
    sell_product
)


def show_products():
    try:
        text_area.delete(1.0, tk.END)

        for company in companies:
            text_area.insert(tk.END, f"\n{'=' * 70}\n")
            text_area.insert(tk.END, f"🏢 КОМПАНИЯ: {company}\n")
            text_area.insert(tk.END, f"{'=' * 70}\n")

            for warehouse in companies[company]:
                text_area.insert(tk.END, f"\n  📦 СКЛАД: {warehouse}\n")

                for category in companies[company][warehouse]:
                    text_area.insert(tk.END, f"\n    📁 КАТЕГОРИЯ: {category}\n")

                    for product_name, product_data in companies[company][warehouse][category].items():
                        # product_data уже словарь с quantity, price, supplier
                        text_area.insert(tk.END,
                                         f"      • {product_name}: {product_data['quantity']} шт, "
                                         f"{product_data['price']} ₽, поставщик: {product_data['supplier']}\n")


    except Exception as e:
        text_area.insert(tk.END, f"Ошибка: {e}")


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

        add_a_new_product(company, warehouse, category, product,
                          int(quantity), int(price), supplier)

        new_window.destroy()
        print(f"Товар добавлен: {product} в {company}/{warehouse}")


    tk.Button(new_window, text="❌ Отмена", command=new_window.destroy).pack()
    tk.Button(new_window, text="✅ Добавить", command=save_product).pack(pady=10)


# Создание главного окна
root = tk.Tk()
root.title("📦 Управление складом")
root.geometry("900x700")


title = ttk.Label(root, text="CRM СИСТЕМА СКЛАДА", font=("Arial", 16))
title.pack(pady=10)

# Кнопки
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

btn1 = ttk.Button(btn_frame, text="📦 Показать товары", command=show_products)
btn1.pack(side=tk.LEFT, padx=5)

btn2 = ttk.Button(btn_frame, text="➕ Добавить товар", command=add_product_gui)
btn2.pack(side=tk.LEFT, padx=5)

btn3 = ttk.Button(btn_frame, text="🚪 Выход", command=root.destroy)
btn3.pack(side=tk.LEFT, padx=5)

# Текстовое поле для вывода
text_area = scrolledtext.ScrolledText(root, width=70, height=40, font=("Courier New", 20), wrap=tk.NONE, xscrollcommand=True)
text_area.pack(pady=10)

print("Окно создано")
root.mainloop()