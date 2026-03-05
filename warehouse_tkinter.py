import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk, scrolledtext
from json_storage import JSONStorage
from warehouse_system import (
    ProductQuantity,
    ProductSell,
    FindAProduct,
    FindSupplier,
    ProductAdd,
    ViewAllProducts,
    companies_for_warehouse,
    export_to_file

)




def show_products(companies_for_warehouse):

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
        result = adder.add_a_new_product(company, warehouse, category, product,
                                int(quantity), int(price), supplier)

        if result[0]:  # успех
            messagebox.showinfo("Успех", result[1])
            new_window.destroy()
            show_products(companies_for_warehouse)
        else:  # ошибка
            messagebox.showerror("Ошибка", result[1])

        print(f"Товар добавлен: {product} в {company}/{warehouse}")


    tk.Button(new_window, text="❌ Отмена", command=new_window.destroy).pack()
    tk.Button(new_window, text="✅ Добавить", command=save_product).pack(pady=10)


def export_to_file():
    storage = JSONStorage()
    success, message = storage.save_data_json(companies_for_warehouse)
    if success:
        messagebox.showinfo("Успех", message)
    else:
        messagebox.showerror("Ошибка", message)


def search_products():
    """Главное окно поиска"""
    search_window = tk.Toplevel(root)
    search_window.title("🔍 Поиск товаров")
    search_window.geometry("500x600")

    # Поле ввода для поиска по названию
    tk.Label(search_window, text="Поиск по названию:").pack(pady=5)
    name_entry = tk.Entry(search_window)
    name_entry.pack()
    tk.Button(search_window, text="Искать по названию",
              command=lambda: search_by_name(name_entry.get())).pack(pady=5)

    # Поиск по компании
    tk.Label(search_window, text="Поиск по компании:").pack(pady=5)
    company_entry = tk.Entry(search_window)
    company_entry.pack()
    tk.Button(search_window, text="Искать по компании",
              command=lambda: search_by_company(company_entry.get())).pack(pady=5)

    # Поиск по поставщику
    tk.Label(search_window, text="Поиск по поставщику:").pack(pady=5)
    supplier_entry = tk.Entry(search_window)
    supplier_entry.pack()
    tk.Button(search_window, text="Искать по поставщику",
              command=lambda: search_by_supplier(supplier_entry.get())).pack(pady=5)

    # Поиск по цене
    tk.Label(search_window, text="Диапазон цены:").pack(pady=5)
    frame_price = tk.Frame(search_window)
    frame_price.pack()
    min_price = tk.Entry(frame_price, width=10)
    min_price.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_price, text="—").pack(side=tk.LEFT)
    max_price = tk.Entry(frame_price, width=10)
    max_price.pack(side=tk.LEFT, padx=5)
    tk.Button(search_window, text="Искать по цене",
              command=lambda: search_by_price(int(min_price.get()), int(max_price.get()))).pack(pady=5)

    # Поиск по количеству
    tk.Label(search_window, text="Диапазон количества:").pack(pady=5)
    frame_qty = tk.Frame(search_window)
    frame_qty.pack()
    min_qty = tk.Entry(frame_qty, width=10)
    min_qty.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_qty, text="—").pack(side=tk.LEFT)
    max_qty = tk.Entry(frame_qty, width=10)
    max_qty.pack(side=tk.LEFT, padx=5)
    tk.Button(search_window, text="Искать по количеству",
              command=lambda: search_by_quantity(int(min_qty.get()), int(max_qty.get()))).pack(pady=5)


def search_by_name(name):
    finder = FindAProduct(companies_for_warehouse)
    results = finder.search_by_product_name(name)
    display_search_results(results, f"Результаты поиска по названию '{name}'")


def search_by_company(company):
    finder = FindAProduct(companies_for_warehouse)
    results = finder.search_by_company(company)
    display_search_results(results, f"Товары компании '{company}'")


def search_by_supplier(supplier):
    finder = FindAProduct(companies_for_warehouse)
    results = finder.search_by_supplier(supplier)
    display_search_results(results, f"Товары поставщика '{supplier}'")


def search_by_price(min_p, max_p):
    finder = FindAProduct(companies_for_warehouse)
    results = finder.search_by_price_range(min_p, max_p)
    display_search_results(results, f"Товары от {min_p} до {max_p} ₽")


def search_by_quantity(min_q, max_q):
    finder = FindAProduct(companies_for_warehouse)
    results = finder.search_by_quantity_range(min_q, max_q)
    display_search_results(results, f"Товары от {min_q} до {max_q} шт")


def display_search_results(results, title):
    """Показать результаты поиска в главном окне"""
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)

    text_area.insert(tk.END, f"{'=' * 70}\n", "company")
    text_area.insert(tk.END, f"{title}\n", "company")
    text_area.insert(tk.END, f"{'=' * 70}\n\n", "company")

    if not results:
        text_area.insert(tk.END, "Ничего не найдено\n")
    else:
        for item in results:
            text_area.insert(tk.END,
                             f"• {item['product']}: {item['quantity']} шт, {item['price']} ₽\n"
                             f"  Компания: {item['company']}, Склад: {item['warehouse']}\n"
                             f"  Категория: {item['category']}, Поставщик: {item['supplier']}\n\n")

    text_area.config(state=tk.DISABLED)



# Создание главного окна
root = tk.Tk()
root.title("📦 Управление складом")
root.geometry("900x700")


# ЗАГРУЗКА JSON ФАЙЛА ПРИ СТАРТЕ ПРОГРАММЫ
def load_data_on_start():
    storage = JSONStorage()

    if messagebox.askyesno("Загрузка", "Загрузить данные из файла?"):
        success, data = storage.load_data()
        if success and data:
            global companies_for_warehouse
            companies_for_warehouse = data
            messagebox.showinfo("Успех", f"Загружено {len(data)} компаний")  # опционально
            print(f"Данные загружены из файла")

        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить файл")
            print("Ошибка при загрузки, используются данные по умолчанию")
    else:
        print("Используются данные по умолчанию")

    show_products(companies_for_warehouse)




title = ttk.Label(root, text="CRM СИСТЕМА СКЛАДА", font=("Arial", 16))
title.pack(pady=10)

# Кнопки
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

btn_show = ttk.Button(btn_frame, text="📦 Показать товары",
                      command=lambda: show_products(companies_for_warehouse))
btn_show.pack(side=tk.LEFT, padx=5)

btn_add = ttk.Button(btn_frame, text="➕ Добавить товар", command=add_product_gui)
btn_add.pack(side=tk.LEFT, padx=5)

btn_refresh = ttk.Button(btn_frame, text="🔄 Обновить",
                         command=lambda: show_products(companies_for_warehouse))
btn_refresh.pack(side=tk.LEFT, padx=5)

btn_export = ttk.Button(btn_frame, text="💾 Экспорт", command=export_to_file)
btn_export.pack(side=tk.LEFT, padx=5)

btn_search = ttk.Button(btn_frame, text="🔍 Поиск", command=search_products)
btn_search.pack(side=tk.LEFT, padx=5)

btn_exit = ttk.Button(btn_frame, text="🚪 Выход", command=root.destroy)
btn_exit.pack(side=tk.LEFT, padx=5)

# Текстовое поле для вывода
text_area = scrolledtext.ScrolledText(root, width=70, height=40, font=("Courier New", 20), wrap=tk.NONE, xscrollcommand=True)
text_area.pack(pady=10)







print("Окно создано")
root.mainloop()