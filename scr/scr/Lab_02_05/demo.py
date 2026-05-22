import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

lab_02_02_path = project_root / "Lab_02_02"
lab_03_path = project_root / "Lab_02_03"

sys.path.insert(0, str(lab_02_02_path))
from collection import StudentCollection
from model import Student

sys.path.insert(0, str(lab_03_path))

from strategies import (
    is_excellent,
    is_bachelor,
    make_gpa_filter,
    by_fio,
    by_gpa,
    by_group_and_gpa,
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
    """Создать демонстрационную коллекцию студентов (минимум 5 штук по ТЗ)."""
    students = StudentCollection()

    s1 = Student("Иванов Иван", "2008-05-14", "БИВТ-25-1", 4.85)
    s2 = Student("Петров Петр", "2007-03-20", "БИВТ-24-1", 3.90)
    s3 = Student("Сидорова Анна", "2006-09-10", "ПМИ-23-2", 4.50)
    s4 = Student("Алексеев Алексей", "2007-11-23", "БИВТ-25-1", 4.95)
    s5 = Student("Михайлов Михаил", "2005-01-15", "МАГ-24-1", 4.20)

    students.add_all([s1, s2, s3, s4, s5])
    return students


def demonstrate_builtins(collection: StudentCollection) -> None:
    """Демонстрация встроенных функций filter() и map() на списках (ТЗ 3 и 4)."""
    print_title("БАЗОВЫЕ ТРЕБОВАНИЯ: Встроенные filter() и map()")
    raw_list = collection.items if hasattr(collection, 'items') else list(collection)

    # 1. Встроенный filter
    print("\nВстроенный filter() (Выбор отличников):")
    excellent_students = list(filter(is_excellent, raw_list))
    print_list([s.fio for s in excellent_students])

    # 2. Встроенный map
    print("\nВстроенный map() (Извлечение ФИО):")
    names = list(map(lambda x: x.fio, raw_list))
    print(names)


def scenario_1_full_chain(collection: StudentCollection) -> None:
    """Сценарий 1: полная цепочка filter -> sort -> apply."""
    print_title("СЦЕНАРИЙ 1: Цепочка filter_by -> sort_by -> apply")

    print("\nШаг 1. Фильтрация студентов бакалавриата:")
    filtered = collection.filter_by(is_bachelor)
    print(filtered)

    print("\nШаг 2. Сортировка по GPA (по убыванию):")
    # Параметр reverse передается, если это реализовано в вашем sort_by,
    # иначе используется стандартная стратегия сортировки
    sorted_collection = filtered.sort_by(lambda x: -x.gpa)
    print(sorted_collection)

    print("\nШаг 3. Применение apply (преобразование в строки):")
    result = sorted_collection.apply(student_to_short_string)
    print_list(result)

    print("\nПолная цепочка одной строкой кода:")
    chain_result = (
        collection
        .filter_by(is_bachelor)
        .sort_by(by_gpa)
        .apply(student_to_short_string)
    )
    print_list(chain_result)


def scenario_2_replace_strategy(collection: StudentCollection) -> None:
    """Сценарий 2: замена стратегии и демонстрация гибкости."""
    print_title("СЦЕНАРИЙ 2: Замена стратегий сортировки и фильтрации")

    print("\nСтратегия сортировки 1: По ФИО:")
    print(collection.sort_by(by_fio))

    print("\nСтратегия сортировки 2: По GPA:")
    print(collection.sort_by(by_gpa))

    print("\nСтратегия сортировки 3 (Мульти-атрибут): По Группе + GPA:")
    print(collection.sort_by(by_group_and_gpa))

    print("\nИспользование фабрики функций (Фильтр GPA >= 4.5):")
    gpa_4_5_filter = make_gpa_filter(4.5)
    print(collection.filter_by(gpa_4_5_filter))

    print("\nСравнение: Один результат через lambda и именованную функцию:")
    res_named = collection.filter_by(is_excellent)
    res_lambda = collection.filter_by(lambda x: x.gpa >= 4.8)
    print(f"Результаты совпадают? {str(res_named) == str(res_lambda)}")


def scenario_3_callable_object_strategy(collection: StudentCollection) -> None:
    """Сценарий 3: демонстрация callable-объекта как стратегии."""
    print_title("СЦЕНАРИЙ 3: Callable-объект как динамическая стратегия")

    print("\nCallable-стратегия: ShortInfoStrategy")
    short_strategy = ShortInfoStrategy()
    print_list(collection.apply(short_strategy))

    print("\nCallable-стратегия с состоянием (Бонус к GPA +0.15):")
    bonus_strategy = GpaBonusStrategy(0.15)
    print_list(collection.apply(bonus_strategy))


def main() -> None:
    """Главная функция запуска демонстрации."""
    collection = create_demo_collection()

    # Демонстрация базовых filter/map из ТЗ
    demonstrate_builtins(collection)

    # Три обязательных сценария из ТЗ на "5"
    scenario_1_full_chain(collection)
    scenario_2_replace_strategy(collection)
    scenario_3_callable_object_strategy(collection)


if __name__ == "__main__":
    main()
