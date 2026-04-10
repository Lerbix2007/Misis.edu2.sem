# demo.py
import sys
from pathlib import Path

# Добавляем путь к корневой папке scr для импорта коллекции из Lab_02_02
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent   # scr
sys.path.insert(0, str(project_root))

# Импорт коллекции из ЛР-2
from Lab_02_02.collection import StudentCollection

# Импорт наших классов
from model import Student
from base import BachelorStudent, MasterStudent


def filter_by_type(collection: StudentCollection, target_type):
    """Возвращает новую коллекцию, содержащую только объекты указанного типа"""
    filtered = [s for s in collection.get_all() if isinstance(s, target_type)]
    return StudentCollection(filtered)


def main():
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ПОЛИМОРФИЗМА И ФИЛЬТРАЦИИ КОЛЛЕКЦИИ")
    print("=" * 70)

    # 1. Создание объектов разных типов
    ordinary = Student("Обычный Студент", "2005-05-10", "БИВТ-25-6", 4.2)
    bachelor = BachelorStudent(
        "Анна Иванова", "2004-08-15", "ИВТ-25-6", 4.7,
        specialization="Прикладная математика", has_thesis=False
    )
    master = MasterStudent(
        "Дмитрий Петров", "2002-03-20", "БИВТ-25-1", 4.9,
        research_area="Машинное обучение", supervisor="Проф. Соколов"
    )

    # 2. Помещаем в коллекцию
    collection = StudentCollection()
    collection.add(ordinary)
    collection.add(bachelor)
    collection.add(master)

    print("\n1. ВСЕ СТУДЕНТЫ В КОЛЛЕКЦИИ:")
    for student in collection:
        print(f"   - {student.fio} ({type(student).__name__})")

    # 3. Полиморфный вызов метода get_scholarship_amount (без условий!)
    print("\n2. ПОЛИМОРФНЫЙ РАСЧЁТ СТИПЕНДИИ (общий интерфейс):")
    for student in collection:
        print(f"   {student.fio:25} → {student.get_scholarship_amount()} руб.")

    # 4. Демонстрация работы специфичных методов (с проверкой типа)
    print("\n3. СПЕЦИФИЧНЫЕ МЕТОДЫ (isinstance):")
    for student in collection:
        if isinstance(student, BachelorStudent):
            print(f"   Бакалавр {student.fio}: {student.defend_thesis()}")
        elif isinstance(student, MasterStudent):
            print(f"   Магистр {student.fio}: {student.publish_paper('AI Conference 2025')}")

    # 5. Фильтрация коллекции по типу (возвращает новую коллекцию)
    print("\n4. ФИЛЬТРАЦИЯ ПО ТИПУ:")
    only_bachelors = filter_by_type(collection, BachelorStudent)
    only_masters = filter_by_type(collection, MasterStudent)

    print(f"   Всего бакалавров: {len(only_bachelors)}")
    for b in only_bachelors:
        print(f"      - {b.fio} (стипендия: {b.get_scholarship_amount()} руб.)")

    print(f"   Всего магистров: {len(only_masters)}")
    for m in only_masters:
        print(f"      - {m.fio} (стипендия: {m.get_scholarship_amount()} руб.)")

    # 6. Повторный вывод коллекции после вызова специфичных методов (чтобы увидеть изменения)
    print("\n5. СОСТОЯНИЕ ПОСЛЕ ИЗМЕНЕНИЙ:")
    for student in collection:
        print(student)
        print("-" * 50)

if __name__ == "__main__":
    main()