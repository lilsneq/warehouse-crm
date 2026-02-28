#Импорты
import json
from tkinter import filedialog
from datetime import datetime
import os





class JSONStorage:
    def save_data_json(self, data, filepath=None):
        try:
            if filepath is None:
                filepath = filedialog.asksaveasfilename(defaultextension=".json")

                if not filepath:
                    print("No file selected")

            with open(filepath, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return True, f'Данные успешно сохранены в {filepath}'

        except TypeError as e:
            # Ошибка несериализуемого типа
            return False, f"Ошибка типа данных: {str(e)}"

        except (PermissionError, OSError) as e:
            return False, f'Ошибка файловой системы: {str(e)}'

        except Exception as e:
            return False, f'Непредвиденная ошибка: {str(e)}'


    def load_data(self, filepath=None):
        try:
            if filepath is None:
                filepath = filedialog.askopenfilename()
                if not filepath:
                    return False, "Файл не выбран"

            with open(filepath, "r", encoding='utf-8') as f:
                data = json.load(f)
                return True, data

        except TypeError as e:
            print(f"Ошибка типа данных: {e}")

        except Exception as e:
            return False, f'Ошибка: {str(e)}'








