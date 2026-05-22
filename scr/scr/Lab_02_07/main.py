# main.py
"""Точка входа в приложение. Загружает данные, запускает CLI, сохраняет данные при выходе."""

import sys
from pathlib import Path

# Настройка путей для импорта
current_file = Path(__file__).resolve()
project_root = current_file.parent

# Добавляем текущую папку в путь
sys.path.insert(0, str(project_root))

from app import StudentApp
from cli import ConsoleInterface
from storage import save, load
from exceptions import SaveLoadError

DATA_FILE = "students.json"


def main() -> None:
    """Главная функция запуска приложения."""
    print("\n" + "=" * 70)
    print("🔄 ЗАГРУЗКА ДАННЫХ")
    print("=" * 70)

    # Загрузка данных из файла
    try:
        loaded_students = load(DATA_FILE)
        if loaded_students:
            print(f"✅ Загружено {len(loaded_students)} студентов из файла '{DATA_FILE}'")
        else:
            print(f"ℹ️ Файл '{DATA_FILE}' не найден или пуст. Начинаем с пустой коллекции.")
    except SaveLoadError as e:
        print(f"⚠️ Ошибка загрузки: {e}. Начинаем с пустой коллекции.")
        loaded_students = []

    # Создание приложения с загруженными данными
    app = StudentApp(loaded_students)

    # Запуск интерфейса
    cli = ConsoleInterface(app)

    try:
        cli.run()
    finally:
        # Сохранение данных при выходе
        print("\n" + "=" * 70)
        print("💾 СОХРАНЕНИЕ ДАННЫХ")
        print("=" * 70)
        try:
            save(app.get_collection(), DATA_FILE)
            print(f"✅ Сохранено {app.get_students_count()} студентов в файл '{DATA_FILE}'")
        except SaveLoadError as e:
            print(f"❌ Ошибка сохранения: {e}")


if __name__ == "__main__":
    main()