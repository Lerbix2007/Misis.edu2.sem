import sys
from pathlib import Path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

lab_02_02_path = project_root / "Lab_02_02"
lab_03_path = project_root / "Lab_02_03"

sys.path.insert(0, str(lab_02_02_path))

from collection import StudentCollection
from model import Student
# Потом добавляем Lab_03 для base.py
sys.path.insert(0, str(lab_03_path))
from base import BachelorStudent, MasterStudent

from strategies import (
    is_active,
    is_excellent,
    by_fio,
    by_gpa,
    student_to_short_string,
    ShortInfoStrategy,
    GpaBonusStrategy
)


def print_title(title: str) -> None:
    """Вывести заголовок сценария."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_list(items) -> None:
    """Вывести элементы списка построчно."""
    for item in items:
        print(item)


def create_demo_collection() -> StudentCollection:
    """Создать демонстрационную коллекцию студентов."""
    students = StudentCollection()

    s1 = Student("Иванов Иван", "2008-05-14", "БИВТ-25-1", 4.85)
    s2 = Student("Петров Петр", "2007-03-20", "БИВТ-24-1", 3.90)
    s3 = Student("Сидорова Анна", "2006-09-10", "ПМИ-23-2", 4.50)

    students.add_all([s1, s2, s3])
    return students


def scenario_1_full_chain(collection: StudentCollection) -> None:
    """
    Сценарий 1:
    полная цепочка filter -> sort -> apply.
    """
    print_title("СЦЕНАРИЙ 1: filter -> sort -> apply")

    print("\nШаг 1. Фильтрация активных студентов:")
    filtered = collection.filter_by(is_active)
    print(filtered)

    print("\nШаг 2. Сортировка по GPA по убыванию:")
    sorted_collection = filtered.sort_by(by_gpa, reverse=True)
    print(sorted_collection)

    print("\nШаг 3. Преобразование в короткие строки:")
    result = sorted_collection.apply(student_to_short_string)
    print_list(result)

    print("\nТа же цепочка одной записью:")
    chain_result = (
        collection
        .filter_by(is_active)
        .sort_by(by_gpa, reverse=True)
        .apply(student_to_short_string)
    )
    print_list(chain_result)


def scenario_2_replace_strategy(collection: StudentCollection) -> None:
    """
    Сценарий 2:
    замена стратегии без изменения кода коллекции.
    """
    print_title("СЦЕНАРИЙ 2: замена стратегии")

    print("\nСортировка по ФИО:")
    result_1 = collection.sort_by(by_fio).apply(student_to_short_string)
    print_list(result_1)

    print("\nСортировка по GPA:")
    result_2 = collection.sort_by(by_gpa, reverse=True).apply(student_to_short_string)
    print_list(result_2)

    print("\nФильтрация отличников:")
    result_3 = collection.filter_by(is_excellent).apply(student_to_short_string)
    print_list(result_3)


def scenario_3_callable_object_strategy(collection: StudentCollection) -> None:
    """
    Сценарий 3:
    демонстрация callable-объекта как стратегии.
    """
    print_title("СЦЕНАРИЙ 3: callable-объект как стратегия")

    print("\nCallable-стратегия ShortInfoStrategy:")
    short_strategy = ShortInfoStrategy()
    result_1 = collection.apply(short_strategy)
    print_list(result_1)

    print("\nCallable-стратегия GpaBonusStrategy:")
    bonus_strategy = GpaBonusStrategy(0.10)
    result_2 = collection.apply(bonus_strategy)
    print_list(result_2)


def main() -> None:
    """Главная функция запуска демонстрации."""
    collection = create_demo_collection()

    scenario_1_full_chain(collection)
    scenario_2_replace_strategy(collection)
    scenario_3_callable_object_strategy(collection)


if __name__ == "__main__":
    main()