# demo.py (сокращенная версия - по 3 студента в сценарии)
from model import Student, StudentStatus
from collection import StudentCollection


def print_separator(title: str = "", char: str = "=", length: int = 80):
    """Вспомогательная функция для вывода разделителей"""
    if title:
        print(f"\n{char * length}")
        print(f" {title}")
        print(f"{char * length}")
    else:
        print(f"\n{char * length}")


def print_collection_info(collection: StudentCollection, name: str = "Коллекция"):
    """Вывести информацию о коллекции"""
    print(f"\n {name}:")
    print(collection)


def scenario_1_basic_operations():
    """СЦЕНАРИЙ 1: Базовые операции с коллекцией"""
    print_separator("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ С КОЛЛЕКЦИЕЙ", "=")

    # Создание 3 студентов
    print("\n Создаем группу студентов:")
    students = [
        Student("Алексеев Алексей Алексеевич", "2006-03-15", "ИН-23-1", 4.2),
        Student("Борисова Божена Борисовна", "2006-07-22", "ИН-23-1", 4.7),
        Student("Васильев Василий Васильевич", "2005-11-10", "ИН-23-1", 3.8),
    ]

    collection = StudentCollection()
    for student in students:
        collection.add(student)
        print(f"   ✅ Добавлен: {student.fio}")

    # Демонстрация len()
    print_separator(" ДЕМОНСТРАЦИЯ len()", "-")
    print(f"Количество студентов в коллекции: {len(collection)}")

    # Демонстрация индексации
    print_separator(" ДЕМОНСТРАЦИЯ ИНДЕКСАЦИИ", "-")
    print(f"Первый студент (collection[0]): {collection[0].fio}")
    print(f"Второй студент (collection[1]): {collection[1].fio}")
    print(f"Последний студент (collection[-1]): {collection[-1].fio}")

    # Демонстрация срезов
    print(f"\nСрез collection[0:2]:")
    for student in collection[0:2]:
        print(f"   - {student.fio}")

    # Демонстрация итерации
    print_separator(" ДЕМОНСТРАЦИЯ ИТЕРАЦИИ", "-")
    for i, student in enumerate(collection, 1):
        print(f"   {i}. {student.fio} - {student.group} (курс {student.course})")

    # Демонстрация удаления по индексу
    print_separator("🗑 ДЕМОНСТРАЦИЯ remove_at(index)", "-")
    print(f"До удаления: {len(collection)} студентов")
    removed = collection.remove_at(1)  # Удаляем Борисову
    if removed:
        print(f"Удален студент: {removed.fio}")
    print(f"После удаления: {len(collection)} студентов")

    # Показываем итоговую коллекцию
    print_collection_info(collection, "ИТОГОВАЯ КОЛЛЕКЦИЯ")

    return collection


def scenario_2_sorting_and_filtering():
    """СЦЕНАРИЙ 2: Сортировка и фильтрация коллекции"""
    print_separator("СЦЕНАРИЙ 2: СОРТИРОВКА И ФИЛЬТРАЦИЯ", "=")

    # Создаем 3 студентов с разной успеваемостью
    print("\n Создаем группу студентов с разной успеваемостью:")
    students_data = [
        ("Волков Владимир Владимирович", "2004-05-10", "ЭН-22-1", 4.9),
        ("Кузнецова Ксения Константиновна", "2005-08-25", "ЭН-22-1", 3.2),
        ("Морозов Михаил Максимович", "2004-12-03", "ЭН-22-2", 2.8),
    ]

    collection = StudentCollection()
    for fio, birthdate, group, gpa in students_data:
        student = Student(fio, birthdate, group, gpa)
        collection.add(student)
        print(f"   ✅ Добавлен: {fio[:35]:35} | {group} | GPA: {gpa}")

    print_collection_info(collection, "ИСХОДНАЯ КОЛЛЕКЦИЯ")

    # 1. Сортировка по ФИО
    print_separator(" СОРТИРОВКА ПО ФИО", "-")
    collection.sort_by_fio()
    print_collection_info(collection, "ПОСЛЕ СОРТИРОВКИ ПО ФИО")

    # 2. Сортировка по GPA (по убыванию)
    print_separator(" СОРТИРОВКА ПО GPA", "-")
    collection.sort_by_gpa(reverse=True)
    print_collection_info(collection, "ЛУЧШИЕ СТУДЕНТЫ В НАЧАЛЕ")

    # 3. Фильтрация
    print_separator(" ФИЛЬТРАЦИЯ КОЛЛЕКЦИИ", "-")

    # Отличники
    excellent = collection.get_excellent_students(threshold=4.5)
    print(f"\n🏆 ОТЛИЧНИКИ (GPA >= 4.5): {len(excellent)} студентов")
    for student in excellent:
        print(f"    {student.fio} - GPA: {student.gpa:.2f}")

    # Неуспевающие
    failing = collection.get_failing_students(threshold=3.0)
    print(f"\n⚠ НЕУСПЕВАЮЩИЕ (GPA < 3.0): {len(failing)} студентов")
    for student in failing:
        print(f"   ❌ {student.fio} - GPA: {student.gpa:.2f}")

    # По группам
    print(f"\n ФИЛЬТРАЦИЯ ПО ГРУППАМ:")
    group1 = collection.get_by_group("ЭН-22-1")
    group2 = collection.get_by_group("ЭН-22-2")
    print(f"   Группа ЭН-22-1: {len(group1)} студентов")
    print(f"   Группа ЭН-22-2: {len(group2)} студентов")

    return collection


def scenario_3_complex_workflow():
    """СЦЕНАРИЙ 3: Сложный рабочий процесс"""
    print_separator("СЦЕНАРИЙ 3: СЛОЖНЫЙ РАБОЧИЙ ПРОЦЕСС", "=")

    # Создаем 3 студентов разных курсов
    print("\n Создаем студентов разных курсов:")
    students = [
        Student("Тихонов Тимофей Тихонович", "2006-03-10", "ФИ-23-1", 4.5),  # 1 курс
        Student("Харитонова Христина Христофоровна", "2003-01-25", "ФИ-20-1", 4.9),  # 4 курс
        Student("Цветков Цезарь Цезаревич", "2005-09-05", "ФИ-22-2", 2.5),  # 2 курс (слабый)
    ]

    collection = StudentCollection()
    for student in students:
        collection.add(student)
        print(f"   ✅ Добавлен: {student.fio} ({student.course} курс, GPA: {student.gpa})")

    print_collection_info(collection, "ИСХОДНАЯ КОЛЛЕКЦИЯ")

    # Сводка до изменений
    collection.display_summary()

    # Симуляция учебного процесса
    print_separator("🎓 СИМУЛЯЦИЯ УЧЕБНОГО ПРОЦЕССА", "-")

    # 1. Отчисляем неуспевающего студента
    print("\n1️⃣ Отчисляем студента с низким GPA:")
    failing_students = collection.get_failing_students(threshold=3.0)
    for student in failing_students:
        print(f"   Отчисляем: {student.fio} (GPA: {student.gpa:.2f})")
        student.expel("Академическая неуспеваемость")

    # 2. Выпускаем студента 4 курса
    print("\n2️⃣ Выпускаем студента 4 курса:")
    fourth_course = collection.get_by_course(4)
    for student in fourth_course:
        if student.gpa >= 3.0:
            print(f"   Выпускаем: {student.fio} (GPA: {student.gpa:.2f})")
            student.graduate()

    # 3. Повышаем курс активному студенту
    print("\n3️⃣ Повышаем курс активному студенту:")
    for student in collection:
        if student.is_active and student.course < Student.MAX_COURSE:
            print(f"   {student.fio} переведен на {student.course + 1} курс")
            student.upgrade_course()

    # Финальный анализ
    print_separator(" ФИНАЛЬНЫЙ АНАЛИЗ КОЛЛЕКЦИИ", "-")
    collection.display_summary()

    # Детализация по статусам
    print("\n ДЕТАЛИЗАЦИЯ ПО СТАТУСАМ:")

    active = collection.get_active()
    print(f"\n🟢 АКТИВНЫЕ СТУДЕНТЫ ({len(active)}):")
    for student in active:
        print(f"   - {student.fio} | {student.course} курс | GPA: {student.gpa:.2f}")

    graduated = collection.get_graduated()
    print(f"\n🎓 ВЫПУЩЕННЫЕ СТУДЕНТЫ ({len(graduated)}):")
    for student in graduated:
        print(f"   - {student.fio} | GPA: {student.gpa:.2f}")

    expelled = collection.get_expelled()
    print(f"\n❌ ОТЧИСЛЕННЫЕ СТУДЕНТЫ ({len(expelled)}):")
    for student in expelled:
        print(f"   - {student.fio} | GPA: {student.gpa:.2f}")

    return collection


def main():
    """Главная функция демонстрации"""
    print("\n" + "=" * 80)
    print("🏫 КОЛЛЕКЦИЯ СТУДЕНТОВ - ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ")
    print("=" * 80)

    # Запуск всех сценариев
    scenario_1_basic_operations()
    scenario_2_sorting_and_filtering()
    scenario_3_complex_workflow()

    # Финальное сообщение
    print_separator(" ВСЕ СЦЕНАРИИ УСПЕШНО ЗАВЕРШЕНЫ", "=")
    print("\n✅ Реализовано:")
    print("   • Индексация коллекции (__getitem__)")
    print("   • Удаление по индексу (remove_at)")
    print("   • Сортировка (sort, sort_by_*)")
    print("   • Фильтрация с возвратом новых коллекций (get_*)")
    print("   • Магические методы (__len__, __iter__, __getitem__)")
    print("   • 3 сценария использования")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()