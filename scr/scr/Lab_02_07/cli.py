# cli.py
"""Консольный интерфейс. Только ввод/вывод, без бизнес-логики."""

from typing import Optional, List
from app import StudentApp


class ConsoleInterface:
    """
    Консольный интерфейс. Все операции делегируются app.py.
    """

    def __init__(self, app: StudentApp) -> None:

        self._app: StudentApp = app

    # ============================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ============================================================

    def _print_menu(self) -> None:
        """Вывести главное меню."""
        print("\n" + "=" * 70)
        print("📚 ГЛАВНОЕ МЕНЮ - УПРАВЛЕНИЕ СТУДЕНТАМИ")
        print("=" * 70)
        print("┌─────┬────────────────────────────────────────────────────────────┐")
        print("│ №   │ Действие                                                   │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 1   │ Добавить обычного студента                                 │")
        print("│ 2   │ Добавить бакалавра                                         │")
        print("│ 3   │ Добавить магистра                                          │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 4   │ Показать всех студентов (таблица)                          │")
        print("│ 5   │ Показать краткую информацию                                │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 6   │ Найти по ФИО                                               │")
        print("│ 7   │ Найти по группе                                            │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 8   │ Фильтр: отличники (GPA >= 4.8)                             │")
        print("│ 9   │ Фильтр: по диапазону GPA                                   │")
        print("│ 10  │ Фильтр: по курсу                                           │")
        print("│ 11  │ Фильтр: активные студенты                                  │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 12  │ Сортировать по ФИО                                         │")
        print("│ 13  │ Сортировать по GPA                                         │")
        print("│ 14  │ Сортировать по курсу                                       │")
        print("│ 15  │ Сортировать по возрасту                                    │")
        print("│ 16  │ Сортировать по группе                                      │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 17  │ Удалить студента по индексу                                │")
        print("│ 18  │ Очистить коллекцию                                         │")
        print("├─────┼────────────────────────────────────────────────────────────┤")
        print("│ 0   │ Выход (с сохранением)                                      │")
        print("└─────┴────────────────────────────────────────────────────────────┘")

    def _get_int_input(self, prompt: str) -> Optional[int]:
        """
        Получить целочисленный ввод с обработкой ошибок.

        Args:
            prompt: Приглашение для ввода

        Returns:
            Целое число или None при ошибке
        """
        user_input = input(prompt).strip()  # сначала получаем строку
        if not user_input:
            print("❌ Ошибка: ввод не может быть пустым")
            return None

        try:
            return int(user_input)
        except ValueError:
            print(f"❌ Ошибка: '{user_input}' не является целым числом")
            return None

    def _get_float_input(self, prompt: str) -> Optional[float]:
        """
        Получить вещественное число с обработкой ошибок.

        Args:
            prompt: Приглашение для ввода

        Returns:
            Число float или None при ошибке
        """
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите число (например, 4.5)")
            return None

    def _get_yes_no(self, prompt: str) -> bool:
        """
        Получить подтверждение (да/нет).

        Args:
            prompt: Приглашение для ввода

        Returns:
            True если 'да', False если 'нет'
        """
        answer = input(prompt).strip().lower()
        return answer in ['да', 'yes', 'y', 'д']

    def _print_students_table(self, students: List, title: str = "") -> None:
        """
        Вывести список студентов в виде таблицы.

        Args:
            students: Список студентов
            title: Заголовок перед таблицей
        """
        if not students:
            print("📦 Нет студентов для отображения")
            return

        if title:
            print(f"\n{title}")

        print("┌─────┬────────────────────────────────┬──────────────┬───────┬───────┬────────┐")
        print("│ №   │ ФИО                            │ Группа       │ GPA   │ Курс  │ Статус │")
        print("├─────┼────────────────────────────────┼──────────────┼───────┼───────┼────────┤")

        for i, student in enumerate(students):
            status_icon = "🟢" if student.is_active else "⚪"
            print(
                f"│ {i:3d} │ {student.fio:30s} │ {student.group:12s} │ {student.gpa:5.2f} │ {student.course:5d} │ {status_icon}      │")

        print("└─────┴────────────────────────────────┴──────────────┴───────┴───────┴────────┘")

    def _input_student_data(self) -> dict:
        """
        Ввод общих данных для студента.

        Returns:
            Словарь с данными студента или пустой словарь при ошибке
        """
        fio = input("Введите ФИО: ").strip()
        if not fio:
            print("❌ ФИО не может быть пустым")
            return {}

        birthdate = input("Введите дату рождения (ГГГГ-ММ-ДД): ").strip()
        group = input("Введите группу (например, БИВТ-25-1): ").strip()

        gpa = self._get_float_input("Введите средний балл (GPA): ")
        if gpa is None:
            return {}

        return {
            "fio": fio,
            "birthdate": birthdate,
            "group": group,
            "gpa": gpa
        }

    # ============================================================
    # ОБРАБОТЧИКИ КОМАНД
    # ============================================================

    def _handle_add_regular(self) -> None:
        """Добавить обычного студента."""
        print("\n➡️ ДОБАВЛЕНИЕ ОБЫЧНОГО СТУДЕНТА")
        data = self._input_student_data()
        if data:
            success, message = self._app.add_student("student", **data)
            print(message)

    def _handle_add_bachelor(self) -> None:
        """Добавить бакалавра."""
        print("\n➡️ ДОБАВЛЕНИЕ БАКАЛАВРА")
        data = self._input_student_data()
        if not data:
            return

        specialization = input("Введите специализацию: ").strip()
        has_thesis = self._get_yes_no("Диплом защищён? (да/нет): ")

        success, message = self._app.add_student(
            "bachelor",
            **data,
            specialization=specialization,
            has_thesis=has_thesis
        )
        print(message)

    def _handle_add_master(self) -> None:
        """Добавить магистра."""
        print("\n➡️ ДОБАВЛЕНИЕ МАГИСТРА")
        data = self._input_student_data()
        if not data:
            return

        research_area = input("Введите область исследований: ").strip()
        supervisor = input("Введите научного руководителя: ").strip()

        success, message = self._app.add_student(
            "master",
            **data,
            research_area=research_area,
            supervisor=supervisor
        )
        print(message)

    def _handle_show_all(self) -> None:
        """Показать всех студентов (таблица)."""
        print("\n➡️ ВСЕ СТУДЕНТЫ")
        if self._app.is_empty():
            print("📦 Коллекция пуста")
        else:
            print(self._app.get_table_string())

    def _handle_show_short_info(self) -> None:
        """Показать краткую информацию."""
        print("\n➡️ КРАТКАЯ ИНФОРМАЦИЯ")
        if self._app.is_empty():
            print("📦 Коллекция пуста")
            return

        info_list = self._app.get_short_info_list()
        for line in info_list:
            print(f"   • {line}")

    def _handle_find_by_fio(self) -> None:
        """Поиск по ФИО."""
        print("\n➡️ ПОИСК ПО ФИО")
        query = input("Введите часть ФИО для поиска: ").strip()
        results, message = self._app.find_by_fio(query)
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_find_by_group(self) -> None:
        """Поиск по группе."""
        print("\n➡️ ПОИСК ПО ГРУППЕ")
        query = input("Введите номер группы: ").strip()
        results, message = self._app.find_by_group(query)
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_filter_excellent(self) -> None:
        """Фильтр отличников."""
        print("\n➡️ ФИЛЬТР: ОТЛИЧНИКИ (GPA >= 4.8)")
        results, message = self._app.filter_by_excellent()
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_filter_gpa_range(self) -> None:
        """Фильтр по диапазону GPA."""
        print("\n➡️ ФИЛЬТР ПО ДИАПАЗОНУ GPA")
        min_gpa = self._get_float_input("Введите минимальный GPA: ")
        if min_gpa is None:
            return
        max_gpa = self._get_float_input("Введите максимальный GPA: ")
        if max_gpa is None:
            return

        results, message = self._app.filter_by_gpa_range(min_gpa, max_gpa)
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_filter_by_course(self) -> None:
        """Фильтр по курсу."""
        print("\n➡️ ФИЛЬТР ПО КУРСУ")
        course = self._get_int_input("Введите номер курса (1-4): ")
        if course is None:
            return

        results, message = self._app.filter_by_course(course)
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_filter_active(self) -> None:
        """Фильтр активных студентов."""
        print("\n➡️ ФИЛЬТР: АКТИВНЫЕ СТУДЕНТЫ")
        results, message = self._app.filter_by_active()
        print(message)
        if results:
            self._print_students_table(results)

    def _handle_sort(self, sort_func, sort_name: str) -> None:
        """Общий обработчик сортировки."""
        print(f"\n➡️ СОРТИРОВКА: {sort_name}")
        if self._app.is_empty():
            print("📦 Коллекция пуста")
            return
        message = sort_func()
        print(message)
        self._handle_show_all()

    def _handle_sort_by_fio(self) -> None:
        self._handle_sort(self._app.sort_by_fio, "ПО ФИО")

    def _handle_sort_by_gpa(self) -> None:
        self._handle_sort(self._app.sort_by_gpa, "ПО GPA")

    def _handle_sort_by_course(self) -> None:
        self._handle_sort(self._app.sort_by_course, "ПО КУРСУ")

    def _handle_sort_by_age(self) -> None:
        self._handle_sort(self._app.sort_by_age, "ПО ВОЗРАСТУ")

    def _handle_sort_by_group(self) -> None:
        self._handle_sort(self._app.sort_by_group, "ПО ГРУППЕ")

    def _handle_remove(self) -> None:
        """Удаление студента по индексу."""
        print("\n➡️ УДАЛЕНИЕ СТУДЕНТА")
        if self._app.is_empty():
            print("📦 Коллекция пуста, нечего удалять")
            return

        print(self._app.get_table_string())
        index = self._get_int_input("Введите индекс студента для удаления: ")
        if index is None:
            return

        confirm = self._get_yes_no(f"Удалить студента с индексом {index}? (да/нет): ")
        success, message, _ = self._app.remove_student(index, confirm)
        print(message)

    def _handle_clear(self) -> None:
        """Очистить коллекцию."""
        print("\n➡️ ОЧИСТКА КОЛЛЕКЦИИ")
        confirm = self._get_yes_no("Вы уверены, что хотите очистить всю коллекцию? (да/нет): ")
        success, message = self._app.clear_collection(confirm)
        print(message)

    # ============================================================
    # ЗАПУСК
    # ============================================================

    def run(self) -> None:
        """Запуск основного цикла приложения."""
        print("\n" + "=" * 70)
        print("🏫 СИСТЕМА УПРАВЛЕНИЯ СТУДЕНТАМИ")
        print("=" * 70)
        print("Добро пожаловать!")

        while True:
            self._print_menu()
            choice = self._get_int_input("Выберите пункт меню: ")

            if choice is None:
                continue

            if choice == 0:
                print("\n👋 До свидания!")
                break
            elif choice == 1:
                self._handle_add_regular()
            elif choice == 2:
                self._handle_add_bachelor()
            elif choice == 3:
                self._handle_add_master()
            elif choice == 4:
                self._handle_show_all()
            elif choice == 5:
                self._handle_show_short_info()
            elif choice == 6:
                self._handle_find_by_fio()
            elif choice == 7:
                self._handle_find_by_group()
            elif choice == 8:
                self._handle_filter_excellent()
            elif choice == 9:
                self._handle_filter_gpa_range()
            elif choice == 10:
                self._handle_filter_by_course()
            elif choice == 11:
                self._handle_filter_active()
            elif choice == 12:
                self._handle_sort_by_fio()
            elif choice == 13:
                self._handle_sort_by_gpa()
            elif choice == 14:
                self._handle_sort_by_course()
            elif choice == 15:
                self._handle_sort_by_age()
            elif choice == 16:
                self._handle_sort_by_group()
            elif choice == 17:
                self._handle_remove()
            elif choice == 18:
                self._handle_clear()
            else:
                print("❌ Ошибка: неверный пункт меню. Выберите число от 0 до 18.")