from model import Student


def print_separator(title: str, char: str = "=") -> None:
    """Выводит разделитель с заголовком"""
    print(f"\n{char * 60}")
    print(f" {title}")
    print(f"{char * 60}")


def main():
    """Основная функция демонстрации"""

    print_separator("ДЕМОНСТРАЦИЯ АТРИБУТОВ КЛАССА")

    # Доступ к атрибуту класса через класс
    print(f" Университет (через класс): {Student.university_name}")
    print(f" Всего студентов (через класс): {Student.total_students}")

    # Создание студентов
    print_separator("СОЗДАНИЕ СТУДЕНТОВ")

    student1 = Student(
        fio="Иванов Иван Петрович",
        birthdate="2003-05-15",
        group="БИВТ-21-1",
        gpa=4.56
    )
    print("✅ Создан студент 1:")
    print(student1)

    print_separator("ДОСТУП К АТРИБУТАМ КЛАССА ЧЕРЕЗ ЭКЗЕМПЛЯР")

    # Доступ к атрибуту класса через экземпляр
    print(f"Университет (через экземпляр): {student1.university_name}")
    print(f"Всего студентов (через экземпляр): {student1.total_students}")

    # Создание второго студента
    student2 = Student(
        fio="Петрова Анна Сергеевна",
        birthdate="2004-03-20",
        group="ИВТ-20-2",
        gpa=4.89
    )
    print("\n✅ Создан студент 2:")
    print(student2)

    print_separator("ПРОВЕРКА АТРИБУТА КЛАССА ПОСЛЕ СОЗДАНИЯ СТУДЕНТОВ")

    print(f"Всего студентов (через класс): {Student.total_students}")
    print(f"Всего студентов (через student1): {student1.total_students}")
    print(f"Всего студентов (через student2): {student2.total_students}")

    print_separator("ДЕМОНСТРАЦИЯ __repr__")

    print("repr(student1):")
    print(repr(student1))
    print("\nrepr(student2):")
    print(repr(student2))

    print_separator("ДЕМОНСТРАЦИЯ СЕТТЕРОВ С ВАЛИДАЦИЕЙ")

    print("🔹 Изменение GPA через сеттер:")
    print(f"   Текущий GPA: {student1.gpa}")
    student1.gpa = 4.75
    print(f"   Новый GPA после изменения: {student1.gpa}")

    print("\n🔹 Изменение группы через сеттер:")
    print(f"   Текущая группа: {student1.group}")
    student1.group = "БИВТ-22-2"
    print(f"   Новая группа: {student1.group}")

    print("\n🔹 Изменение ФИО через сеттер:")
    print(f"   Текущее ФИО: {student1.fio}")
    student1.fio = "Маки Дзенин обновлено)"
    print(f"   Новое ФИО: {student1.fio}")

    print_separator("ПРОВЕРКА РАБОТЫ ОГРАНИЧЕНИЙ (TRY/EXCEPT)")

    test_cases = [
        ("ФИО слишком короткое", "Ив", "", ""),
        ("ФИО без фамилии", "Иван", "", ""),
        ("Группа неверного формата", "Иванов Иван", "2000-01-01", "ГРП101", 4.5),
        ("GPA слишком низкий", "Иванов Иван", "2000-01-01", "БИВТ-21-1", 1.5),
        ("GPA слишком высокий", "Иванов Иван", "2000-01-01", "БИВТ-21-1", 5.5),
        ("GPA с тремя знаками", "Иванов Иван", "2000-01-01", "БИВТ-21-1", 4.567),
        ("Дата в будущем", "Иванов Иван", "2027-01-01", "БИВТ-21-1", 4.5),
        ("Возраст меньше 16", "Иванов Иван", "2015-01-01", "БИВТ-21-1", 4.5),
    ]

    for description, fio, birthdate, group, *gpa in test_cases:
        print(f"\nТест: {description}")
        try:
            if gpa:
                Student(fio=fio, birthdate=birthdate, group=group, gpa=gpa[0])
            else:
                Student(fio=fio, birthdate=birthdate, group=group, gpa=4.5)
            print(f"   ✅ Успех (не должно было случиться!)")
        except ValueError as e:
            print(f"   ❌ Ошибка (ожидаемо): {e}")

    print_separator("ДЕМОНСТРАЦИЯ ВТОРОГО БИЗНЕС-МЕТОДА (get_gpa_grade)")

    test_gpas = [2.3, 3.2, 4.1, 4.9, 5.0]
    for i, gpa_value in enumerate(test_gpas, 1):
        try:
            temp_student = Student(
                fio=f"Тестов Тест{i}",
                birthdate="2000-01-01",
                group="БИВТ-21-1",
                gpa=gpa_value
            )
            print(f"   GPA: {gpa_value:.2f} → Оценка: {temp_student.get_gpa_grade()}")
        except ValueError as e:
            print(f"   GPA: {gpa_value:.2f} → Ошибка: {e}")

    print_separator("ДЕМОНСТРАЦИЯ ВСЕХ ВОЗМОЖНОСТЕЙ")

    # Создаем показательного студента
    best_student = Student(
        fio="Смирнова Екатерина Алексеевна",
        birthdate="2003-11-07",
        group="БИВТ-20-1",
        gpa=4.98
    )

    print("🏆 Лучший студент:")
    print(best_student)

    print("\n Детальная информация:")
    print(f"   • Возраст: {best_student.get_age()} лет")
    print(f"   • Курс: {best_student.course}")
    print(f"   • Буквенная оценка: {best_student.get_gpa_grade()}")
    print(f"   • Студенческий билет: {best_student.get_student_card()}")

    print_separator("ИЗМЕНЕНИЕ АТРИБУТА КЛАССА")

    print(f" Текущий университет: {Student.university_name}")
    Student.university_name = "МГТУ им. Баумана"
    print(f" Новый университет (после изменения): {Student.university_name}")

    # Проверяем, что изменилось у всех студентов
    print(f" У student1: {student1.university_name}")
    print(f" У best_student: {best_student.university_name}")

    print_separator("ИТОГОВАЯ СТАТИСТИКА")

    print(f" Всего создано студентов: {Student.total_students}")
    print(f" Демонстрация завершена")


if __name__ == "__main__":
    main()