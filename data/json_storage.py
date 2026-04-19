#Импорты
import json
from config.settings import APPLICATIONS_FILE





class JSONStorage:

    def __init__(self, default_path=APPLICATIONS_FILE):
        self.default_path = default_path


    def save_data_json(self, data, filepath=None):
        #СОХРАНЕНИЕ ИЗ JSON
        target_path = filepath or self.default_path

        try:
            with open(target_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return True, f'Данные успешно сохранены в {target_path}'

        except TypeError as e:
            return False, f"Ошибка типа данных: {e}"

        except (PermissionError, OSError) as e:
            return False, f'Ошибка файловой системы: {e}'

        except Exception as e:
            return False, f'Непредвиденная ошибка: {e}'


    def load_data(self, filepath=None):
        #загрузка из файла JSON
        target_path = filepath or self.default_path
        try:
            with open(target_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                return True, data
        except FileNotFoundError as e:
            return False, f'Файл не найден {e}'

        except TypeError as e:
            return False, f"Ошибка типа данных: {e}"

        except Exception as e:
            return False, f'Ошибка: {e}'








