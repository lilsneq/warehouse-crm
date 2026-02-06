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
        result = view_all_products_with_detailed_information()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result)
    except Exception as e:
        text_area.insert(tk.END, f"Ошибка: {e}")


def add_product_gui():
    new_window = tk.Toplevel(root)
    new_window.title("Добавить")
    new_window.geometry("300x400")
    fields = [
        ("Компания:", "company"),
        ("Склад:", "warehouse"),
        ("Категория:", "category"),
        ("Товар:", "product"),
        ("Количество:", "quantity"),
        ("Цена:", "price"),
        ("Поставщик:", "supplier")
    ]

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

        new_window.destroy()
        print(f"Товар добавлен: {product} в {company}/{warehouse}")


    tk.Button(new_window, text="❌ Отмена", command=new_window.destroy).pack()
    tk.Button(new_window, text="✅ Добавить", command=save_product).pack(pady=10)


# Создание главного окна
root = tk.Tk()
root.title("📦 Управление складом")
root.geometry("600x500")


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
text_area = scrolledtext.ScrolledText(root, width=70, height=20)
text_area.pack(pady=10)

print("Окно создано")
root.mainloop()