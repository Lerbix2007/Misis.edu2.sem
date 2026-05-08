from interfaces import Printable, Comparable, ScholarshipInfo
from models import (
    ContractStudent,
    ContractBachelorStudent,
    ContractMasterStudent,
    InterfaceStudentCollection
)


def print_all(items: list[Printable]) -> None:
    """Полиморфный вывод через интерфейс Printable"""
    for item in items:
        print(item.to_string())


def print_scholarships(items: list[ScholarshipInfo]) -> None:
    """Полиморфный вывод стипендий через интерфейс ScholarshipInfo"""
    for item in items:
        print(item.scholarship_info())


def print_sorted(items: list[Comparable]) -> None:
    """Полиморфная сортировка через интерфейс Comparable"""
    sorted_items = sorted(
        items,
        key=lambda item: item.get_compare_value(),
        reverse=True
    )

    for item in sorted_items:
        print(f"{item.to_string()} | рейтинг: {item.get_compare_value():.2f}")


def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №4")
    print("ИНТЕРФЕЙСЫ, КОЛЛЕКЦИИ И ПОЛИМОРФИЗМ")
    print("=" * 70)

    student = ContractStudent(
        "Студент Адам",
        "2005-05-10",
        "БИВТ-25-6",
        4.2
    )

    bachelor = ContractBachelorStudent(
        "Анна Иванова",
        "2004-08-15",
        "ИВТ-25-6",
        4.7,
        specialization="Прикладная математика",
        has_thesis=True
    )

    master = ContractMasterStudent(
        "Дмитрий Петров",
        "2002-03-20",
        "БИВТ-25-1",
        4.9,
        research_area="Машинное обучение",
        supervisor="Проф. Соколов"
    )

    master.publish_paper("AI Conference 2025")
    master.publish_paper("Data Science Forum")

    collection = InterfaceStudentCollection()
    collection.add(student)
    collection.add(bachelor)
    collection.add(master)

    print("\n1. ЕДИНЫЙ СПИСОК ОБЪЕКТОВ РАЗНЫХ ТИПОВ")
    print("-" * 70)
    for item in collection:
        print(f"{item.fio} — {type(item).__name__}")

    print("\n2. СЦЕНАРИЙ №1: ВЫВОД ЧЕРЕЗ Printable")
    print("-" * 70)
    printable_collection = collection.get_printable()
    print_all(printable_collection.get_all())

    print("\n3. СЦЕНАРИЙ №2: СТИПЕНДИИ ЧЕРЕЗ ScholarshipInfo")
    print("-" * 70)
    scholarship_collection = collection.get_scholarship_items()
    print_scholarships(scholarship_collection.get_all())

    print("\n4. СЦЕНАРИЙ №3: СОРТИРОВКА ЧЕРЕЗ Comparable")
    print("-" * 70)
    comparable_collection = collection.get_comparable()
    print_sorted(comparable_collection.get_all())

    print("\n5. ПРОВЕРКА isinstance(obj, Printable)")
    print("-" * 70)
    for item in collection:
        print(f"{item.fio}: {isinstance(item, Printable)}")

    print("\n6. СОРТИРОВКА ВНУТРИ КОЛЛЕКЦИИ")
    print("-" * 70)
    sorted_collection = collection.sort_by_compare_value()

    for item in sorted_collection:
        print(f"{item.fio}: рейтинг {item.get_compare_value():.2f}")


if __name__ == "__main__":
    main()