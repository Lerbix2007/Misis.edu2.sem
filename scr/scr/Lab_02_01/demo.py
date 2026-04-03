from model import Student, StudentStatus
from datetime import datetime


def print_separator(title: str, char: str = "=") -> None:
    """Выводит разделитель с заголовком"""
    print(f"\n{char * 60}")
    print(f" {title}")
    print(f"{char * 60}")


def main():
    """Основная функция демонстрации"""

    print_separator("СОЗДАНИЕ СТУДЕНТОВ")

    student1 = Student(
        fio="Иванов Иван Петрович",
        birthdate="2003-05-15",
        group="БИВТ-21-1",
        gpa=4.56
    )
    print("✅ Создан студент 1:")
    print(student1)

    student2 = Student(
        fio="Петрова Анна Сергеевна",
        birthdate="2004-03-20",
        group="ИВТ-20-2",
        gpa=4.89
    )
    print("\n✅ Создан студент 2:")
    print(student2)

    print_separator("ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ (ОТДЕЛЬНЫЙ МОДУЛЬ)")

    test_cases = [
        ("ФИО слишком короткое", "Ив", "2000-01-01", "БИВТ-21-1", 4.5),
        ("ФИО с цифрами", "Иванов123", "2000-01-01", "БИВТ-21-1", 4.5),
        ("Группа неверного формата", "Иванов Иван", "2000-01-01", "ГРП101", 4.5),
        ("GPA выше 5", "Иванов Иван", "2000-01-01", "БИВТ-21-1", 5.5),
        ("Дата в будущем", "Иванов Иван", "2026-01-01", "БИВТ-21-1", 4.5),
        ("Возраст меньше 16", "Иванов Иван", "2015-01-01", "БИВТ-21-1", 4.5),
    ]

    for description, fio, birthdate, group, gpa in test_cases:
        print(f"\n Тест: {description}")
        try:
            Student(fio=fio, birthdate=birthdate, group=group, gpa=gpa)
            print(f"   ❌ Ошибка: тест должен был провалиться")
        except ValueError as e:
            print(f"   ✅ Валидация сработала: {e}")

    print_separator("ДЕМОНСТРАЦИЯ МЕТОДОВ ИЗМЕНЕНИЯ СОСТОЯНИЯ")

    # Создаем студента для демонстрации
    demo_student = Student(
        fio="Сидоров Петр Алексеевич",
        birthdate="2006-12-01",
        group="ПМИ-22-3",
        gpa=4.2
    )
    print("Исходный студент:")
    print(demo_student)

    print("\n🔹 1. Попытка повысить курс (успешно):")
    demo_student.upgrade_course()
    print(f"   Текущий курс: {demo_student.course}")

    print("\n🔹 2. Отправляем в академический отпуск:")
    demo_student.take_academic_leave()
    print(f"   Статус: {demo_student.status.value}")

    print("\n🔹 3. Попытка повысить курс в отпуске (ДОЛЖНА БЫТЬ ОШИБКА):")
    try:
        demo_student.upgrade_course()
    except ValueError as e:
        print(f"   ❌ Ошибка (ожидаемо): {e}")

    print("\n🔹 4. Активируем студента обратно:")
    demo_student.activate()
    print(f"   Статус: {demo_student.status.value}")

    print("\n🔹 Повышаем курс до максимума:")
    for _ in range(Student.MAX_COURSE):
        if demo_student.course >= Student.MAX_COURSE:
            break
        demo_student.upgrade_course()
    print(f"   Финальный курс: {demo_student.course}")

    print("\n🔹 6. Попытка повысить курс выше {Student.MAX_COURSE}:")
    try:
        demo_student.upgrade_course()
    except ValueError as e:
        print(f"   ❌ Ошибка (ожидаемо): {e}")

    print("\n🔹 7. Выпускаем студента:")
    demo_student.graduate()
    print(f"   Статус: {demo_student.status.value}")

    print("\n🔹 8. Попытка изменить GPA выпускника (ДОЛЖНА БЫТЬ ОШИБКА):")
    try:
        demo_student.add_points(0.5)
    except ValueError as e:
        print(f"   ❌ Ошибка (ожидаемо): {e}")

    print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С ОТЧИСЛЕНИЕМ")

    expelled_student = Student(
        fio="Васильев Василий",
        birthdate="2004-07-20",
        group="БИВТ-21-3",
        gpa=2.5
    )
    print("Создан студент с низким GPA:")
    print(expelled_student)

    print("\n🔹 Отчисляем студента за неуспеваемость:")
    expelled_student.expel(reason="Академическая неуспеваемость")
    print(f"   Статус: {expelled_student.status.value}")

    print("\n🔹 Попытка повысить курс отчисленного (ДОЛЖНА БЫТЬ ОШИБКА):")
    try:
        expelled_student.upgrade_course()
    except ValueError as e:
        print(f"   ❌ Ошибка (ожидаемо): {e}")

    print_separator("ДЕМОНСТРАЦИЯ АТРИБУТОВ КЛАССА")

    print(f" Университет: {Student.university_name}")
    print(f" Всего студентов: {Student.total_students}")
    print(f" Максимальный курс: {Student.MAX_COURSE}")

    print_separator("ДЕМОНСТРАЦИЯ БИЗНЕС-МЕТОДОВ")

    test_student = Student(
        fio="Тестовый Студент",
        birthdate="2003-01-15",
        group="БИВТ-21-4",
        gpa=4.35
    )

    print(f"Возраст: {test_student.get_age()} лет")
    print(f"Буквенная оценка: {test_student.get_gpa_grade()}")
    print(f"Студенческий билет: {test_student.get_student_card()}")

    print_separator("ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")

    print("__str__:")
    print(test_student)

    print("\n__repr__:")
    print(repr(test_student))

    student_copy = Student(
        fio="Тестовый Студент",
        birthdate="2003-01-15",
        group="ДРУГАЯ-99-9",
        gpa=3.0
    )
    print(f"\n__eq__: {test_student == student_copy}")

    print_separator("ИТОГОВАЯ СТАТИСТИКА")
    print(f"👥 Всего создано студентов: {Student.total_students}")


if __name__ == "__main__":
    main()