import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk, scrolledtext
from data.json_storage import JSONStorage
from scripts.warehouse_system import (
    FindAProduct,
    ProductAdd,
    companies_for_warehouse

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

    entries = {}
    for label_text, key in fields:
        tk.Label(new_window, text=label_text).pack()
        entry = tk.Entry(new_window)
        entry.pack()
        entries[key] = entry

    def save_product():
        # Получаем данные
        company = entries['company'].get().strip()
        warehouse = entries['warehouse'].get().strip()
        category = entries['category'].get().strip()
        product = entries['product'].get().strip()
        quantity = entries['quantity'].get().strip()
        price = entries['price'].get().strip()
        supplier = entries['supplier'].get().strip()

        # Проверка на пустые поля
        if not all([company, warehouse, category, product, quantity, price, supplier]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        # Проверка что количество и цена - числа
        try:
            quantity_int = int(quantity)
            price_int = int(price)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество и цена должны быть числами")
            return

        # ✅ Правильно: передаем companies_for_warehouse
        adder = ProductAdd(companies_for_warehouse)

        # ✅ Метод возвращает bool, а не tuple
        success = adder.add_a_new_product(
            company, warehouse, category, product,
            quantity_int, price_int, supplier
        )

        if success:
            messagebox.showinfo("Успех", "Товар успешно добавлен/обновлен")
            new_window.destroy()
            show_products(companies_for_warehouse)  # обновляем отображение
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить товар (проверьте количество)")

    # Кнопки
    button_frame = tk.Frame(new_window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="✅ Добавить", command=save_product,
              bg="lightgreen", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="❌ Отмена", command=new_window.destroy,
              bg="lightcoral", width=15).pack(side=tk.LEFT, padx=5)


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
    search_window.geometry("600x700")

    # Создаем один экземпляр finder для всего окна поиска
    finder = FindAProduct(companies_for_warehouse)

    # Фрейм для критериев
    criteria_frame = ttk.LabelFrame(search_window, text="Критерии поиска", padding=10)
    criteria_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Поиск по названию
    tk.Label(criteria_frame, text="Поиск по названию:").grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(criteria_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5, padx=5)

    # Поиск по компании
    tk.Label(criteria_frame, text="Поиск по компании:").grid(row=1, column=0, sticky="w", pady=5)
    company_entry = tk.Entry(criteria_frame, width=30)
    company_entry.grid(row=1, column=1, pady=5, padx=5)

    # Поиск по поставщику
    tk.Label(criteria_frame, text="Поиск по поставщику:").grid(row=2, column=0, sticky="w", pady=5)
    supplier_entry = tk.Entry(criteria_frame, width=30)
    supplier_entry.grid(row=2, column=1, pady=5, padx=5)

    # Поиск по цене
    tk.Label(criteria_frame, text="Диапазон цены:").grid(row=3, column=0, sticky="w", pady=5)
    price_frame = tk.Frame(criteria_frame)
    price_frame.grid(row=3, column=1, pady=5, padx=5)

    min_price = tk.Entry(price_frame, width=10)
    min_price.pack(side=tk.LEFT)
    tk.Label(price_frame, text="—").pack(side=tk.LEFT, padx=5)
    max_price = tk.Entry(price_frame, width=10)
    max_price.pack(side=tk.LEFT)

    # Поиск по количеству
    tk.Label(criteria_frame, text="Диапазон количества:").grid(row=4, column=0, sticky="w", pady=5)
    qty_frame = tk.Frame(criteria_frame)
    qty_frame.grid(row=4, column=1, pady=5, padx=5)

    min_qty = tk.Entry(qty_frame, width=10)
    min_qty.pack(side=tk.LEFT)
    tk.Label(qty_frame, text="—").pack(side=tk.LEFT, padx=5)
    max_qty = tk.Entry(qty_frame, width=10)
    max_qty.pack(side=tk.LEFT)

    # Кнопка сброса
    tk.Button(criteria_frame, text="🔄 Сбросить критерии",
              command=lambda: reset_criteria(finder, [name_entry, company_entry, supplier_entry,
                                                      min_price, max_price, min_qty, max_qty])).grid(row=5, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)

    # Функция применения всех критериев
    def apply_criteria():
        # Устанавливаем критерии через setter'ы
        finder.name = name_entry.get()
        finder.company = company_entry.get()
        finder.supplier = supplier_entry.get()

        # Обработка цены
        try:
            min_p = int(min_price.get()) if min_price.get() else 0
            max_p = int(max_price.get()) if max_price.get() else float('inf')
            finder.price_range = (min_p, max_p)
        except ValueError:
            finder.price_range = (0, float('inf'))

        # Обработка количества
        try:
            min_q = int(min_qty.get()) if min_qty.get() else 0
            max_q = int(max_qty.get()) if max_qty.get() else float('inf')
            finder.quantity_range = (min_q, max_q)
        except ValueError:
            finder.quantity_range = (0, float('inf'))

        # Получаем результаты через getter
        results = finder.results

        # Формируем заголовок с активными критериями
        active_criteria = []
        if finder.name:
            active_criteria.append(f"название: '{finder.name}'")
        if finder.company:
            active_criteria.append(f"компания: '{finder.company}'")
        if finder.supplier:
            active_criteria.append(f"поставщик: '{finder.supplier}'")
        if finder.price_range != (0, float('inf')):
            min_p, max_p = finder.price_range
            if max_p == float('inf'):
                active_criteria.append(f"цена ≥ {min_p}")
            else:
                active_criteria.append(f"цена: {min_p}-{max_p}")
        if finder.quantity_range != (0, float('inf')):
            min_q, max_q = finder.quantity_range
            if max_q == float('inf'):
                active_criteria.append(f"количество ≥ {min_q}")
            else:
                active_criteria.append(f"количество: {min_q}-{max_q}")

        title = "Результаты поиска"
        if active_criteria:
            title = f"Поиск по: {', '.join(active_criteria)}"

        display_search_results(results, title)

        # Закрываем окно поиска
        search_window.destroy()

    # Кнопки
    button_frame = tk.Frame(search_window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="🔍 Найти", command=apply_criteria,
              bg="lightblue", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="❌ Отмена", command=search_window.destroy,
              width=15).pack(side=tk.LEFT, padx=5)


def reset_criteria(finder, entries):
    """Сброс всех критериев"""
    finder.reset()
    for entry in entries:
        entry.delete(0, tk.END)
    messagebox.showinfo("Сброс", "Все критерии сброшены")


def display_search_results(results, title):
    """Показать результаты поиска в главном окне"""
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)

    text_area.insert(tk.END, f"{'=' * 70}\n", "company")
    text_area.insert(tk.END, f"{title}\n", "company")
    text_area.insert(tk.END, f"{'=' * 70}\n\n", "company")

    if not results:
        text_area.insert(tk.END, "❌ Ничего не найдено\n")
    else:
        text_area.insert(tk.END, f"✅ Найдено товаров: {len(results)}\n\n")
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
# def load_data_on_start():
#     storage = JSONStorage()
#
#     if messagebox.askyesno("Загрузка", "Загрузить данные из файла?"):
#         success, data = storage.load_data()
#         if success and data:
#             global companies_for_warehouse
#             companies_for_warehouse = data
#             messagebox.showinfo("Успех", f"Загружено {len(data)} компаний")  # опционально
#             print(f"Данные загружены из файла")
#
#         else:
#             messagebox.showerror("Ошибка", "Не удалось загрузить файл")
#             print("Ошибка при загрузки, используются данные по умолчанию")
#     else:
#         print("Используются данные по умолчанию")
#
#     show_products(companies_for_warehouse)




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
