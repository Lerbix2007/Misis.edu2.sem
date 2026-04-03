# student_collection.py (финальная версия с индексацией, сортировкой и фильтрацией)
from typing import List, Optional, Iterator, Callable, Any
from model import Student, StudentStatus


class StudentCollection:


    def __init__(self, items: Optional[List[Student]] = None):
        """
        Инициализация коллекции

        Args:
            items: Начальный список студентов
        """
        self._items: List[Student] = []
        if items:
            for item in items:
                self.add(item)

    def add(self, item: Student) -> None:
        """
        Добавить объект Student в коллекцию

        Args:
            item: Объект типа Student

        Raises:
            TypeError: Если добавляемый объект не является экземпляром Student
            ValueError: Если студент с таким ФИО и датой рождения уже существует
        """
        if not isinstance(item, Student):
            raise TypeError(f"Можно добавлять только объекты типа Student. Получен: {type(item).__name__}")

        # Проверка на дубликат (по ФИО и дате рождения)
        for existing in self._items:
            if existing.fio == item.fio and existing.birthdate == item.birthdate:
                raise ValueError(
                    f"Нельзя добавить дубликат: студент '{item.fio}' (родился: {item.birthdate}) уже существует"
                )

        self._items.append(item)

    def add_all(self, items: List[Student]) -> None:
        """
        Добавить несколько студентов в коллекцию

        Args:
            items: Список студентов для добавления
        """
        for item in items:
            self.add(item)

    def remove(self, item: Student) -> bool:
        """
        Удалить объект Student из коллекции

        Args:
            item: Объект типа Student для удаления

        Returns:
            bool: True если объект найден и удален, False если не найден
        """
        if not isinstance(item, Student):
            raise TypeError(f"Можно удалять только объекты типа Student")

        try:
            index = self._items.index(item)
            self._items.pop(index)
            return True
        except ValueError:
            return False

    def remove_at(self, index: int) -> Optional[Student]:
        """
        Удалить объект по индексу

        Args:
            index: Индекс элемента для удаления

        Returns:
            Optional[Student]: Удаленный студент или None если индекс невалидный
        """
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def get_all(self) -> List[Student]:
        """
        Получить список всех объектов в коллекции

        Returns:
            List[Student]: Копия списка объектов
        """
        return self._items.copy()

    # === МЕТОДЫ ПОИСКА ===

    def find_by_fio(self, fio: str, exact_match: bool = False) -> List[Student]:
        """Найти студентов по ФИО"""
        if exact_match:
            return [student for student in self._items if student.fio == fio]
        else:
            return [student for student in self._items if fio.lower() in student.fio.lower()]

    def find_by_group(self, group: str, exact_match: bool = True) -> List[Student]:
        """Найти студентов по группе"""
        if exact_match:
            return [student for student in self._items if student.group == group]
        else:
            return [student for student in self._items if group.lower() in student.group.lower()]

    def find_by_gpa_range(self, min_gpa: float, max_gpa: float) -> List[Student]:
        """Найти студентов в диапазоне GPA"""
        return [student for student in self._items if min_gpa <= student.gpa <= max_gpa]

    def find_by_course(self, course: int) -> List[Student]:
        """Найти студентов по курсу"""
        return [student for student in self._items if student.course == course]

    def find_by_status(self, status) -> List[Student]:
        """Найти студентов по статусу"""
        return [student for student in self._items if student.status == status]

    # === МЕТОДЫ СОРТИРОВКИ ===

    def sort(self, key: Optional[Callable[[Student], Any]] = None, reverse: bool = False) -> None:
        """
        Универсальная сортировка коллекции

        Args:
            key: Функция для получения ключа сортировки
            reverse: Если True, сортировка в обратном порядке
        """
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)

    def sort_by_fio(self, reverse: bool = False) -> None:
        """Сортировка по ФИО"""
        self._items.sort(key=lambda s: s.fio, reverse=reverse)

    def sort_by_gpa(self, reverse: bool = True) -> None:
        """Сортировка по GPA (по умолчанию по убыванию)"""
        self._items.sort(key=lambda s: s.gpa, reverse=reverse)

    def sort_by_course(self, reverse: bool = False) -> None:
        """Сортировка по курсу"""
        self._items.sort(key=lambda s: s.course, reverse=reverse)

    def sort_by_age(self, reverse: bool = False) -> None:
        """Сортировка по возрасту"""
        self._items.sort(key=lambda s: s.get_age(), reverse=reverse)

    def sort_by_group(self, reverse: bool = False) -> None:
        """Сортировка по группе"""
        self._items.sort(key=lambda s: s.group, reverse=reverse)

    def sort_by_birthdate(self, reverse: bool = False) -> None:
        """Сортировка по дате рождения"""
        self._items.sort(key=lambda s: s.birthdate_raw, reverse=reverse)

    # === МЕТОДЫ ФИЛЬТРАЦИИ (ВОЗВРАЩАЮТ НОВУЮ КОЛЛЕКЦИЮ) ===

    def get_active(self) -> 'StudentCollection':
        """
        Получить коллекцию активных студентов

        Returns:
            StudentCollection: Новая коллекция с активными студентами
        """
        active_students = [s for s in self._items if s.is_active]
        return StudentCollection(active_students)

    def get_on_academic_leave(self) -> 'StudentCollection':
        """
        Получить коллекцию студентов в академическом отпуске

        Returns:
            StudentCollection: Новая коллекция со студентами в академ. отпуске
        """
        leave_students = [s for s in self._items if s.status == StudentStatus.ACADEMIC_LEAVE]
        return StudentCollection(leave_students)

    def get_graduated(self) -> 'StudentCollection':
        """
        Получить коллекцию выпущенных студентов

        Returns:
            StudentCollection: Новая коллекция с выпущенными студентами
        """
        graduated_students = [s for s in self._items if s.status == StudentStatus.GRADUATED]
        return StudentCollection(graduated_students)

    def get_expelled(self) -> 'StudentCollection':
        """
        Получить коллекцию отчисленных студентов

        Returns:
            StudentCollection: Новая коллекция с отчисленными студентами
        """
        expelled_students = [s for s in self._items if s.status == StudentStatus.EXPELLED]
        return StudentCollection(expelled_students)

    def get_excellent_students(self, threshold: float = 4.8) -> 'StudentCollection':
        """
        Получить коллекцию отличников (GPA >= threshold)

        Args:
            threshold: Пороговое значение GPA для отличников

        Returns:
            StudentCollection: Новая коллекция с отличниками
        """
        excellent = [s for s in self._items if s.gpa >= threshold]
        return StudentCollection(excellent)

    def get_good_students(self, min_gpa: float = 4.0, max_gpa: float = 4.8) -> 'StudentCollection':
        """
        Получить коллекцию хорошистов

        Args:
            min_gpa: Минимальный GPA для хорошистов
            max_gpa: Максимальный GPA для хорошистов

        Returns:
            StudentCollection: Новая коллекция с хорошистами
        """
        good = [s for s in self._items if min_gpa <= s.gpa < max_gpa]
        return StudentCollection(good)

    def get_satisfactory_students(self, min_gpa: float = 3.0, max_gpa: float = 4.0) -> 'StudentCollection':
        """
        Получить коллекцию троечников

        Returns:
            StudentCollection: Новая коллекция с удовлетворительной успеваемостью
        """
        satisfactory = [s for s in self._items if min_gpa <= s.gpa < max_gpa]
        return StudentCollection(satisfactory)

    def get_failing_students(self, threshold: float = 3.0) -> 'StudentCollection':
        """
        Получить коллекцию неуспевающих студентов (GPA < threshold)

        Args:
            threshold: Пороговое значение GPA

        Returns:
            StudentCollection: Новая коллекция с неуспевающими студентами
        """
        failing = [s for s in self._items if s.gpa < threshold]
        return StudentCollection(failing)

    def get_by_course(self, course: int) -> 'StudentCollection':
        """
        Получить коллекцию студентов указанного курса

        Args:
            course: Номер курса

        Returns:
            StudentCollection: Новая коллекция со студентами курса
        """
        course_students = [s for s in self._items if s.course == course]
        return StudentCollection(course_students)

    def get_by_group(self, group: str) -> 'StudentCollection':
        """
        Получить коллекцию студентов указанной группы

        Args:
            group: Номер группы

        Returns:
            StudentCollection: Новая коллекция со студентами группы
        """
        group_students = [s for s in self._items if s.group == group]
        return StudentCollection(group_students)

    def get_by_gpa_range(self, min_gpa: float, max_gpa: float) -> 'StudentCollection':
        """
        Получить коллекцию студентов с GPA в заданном диапазоне

        Args:
            min_gpa: Минимальный GPA
            max_gpa: Максимальный GPA

        Returns:
            StudentCollection: Новая коллекция с подходящими студентами
        """
        range_students = [s for s in self._items if min_gpa <= s.gpa <= max_gpa]
        return StudentCollection(range_students)

    # === МАГИЧЕСКИЕ МЕТОДЫ ===

    def __len__(self) -> int:
        """Вернуть количество элементов в коллекции"""
        return len(self._items)

    def __iter__(self) -> Iterator[Student]:
        """Вернуть итератор для обхода коллекции"""
        return iter(self._items)

    def __getitem__(self, index):
        """
        Поддержка индексации и срезов коллекции

        Args:
            index: Индекс или срез (поддерживает отрицательные индексы)

        Returns:
            Student или новая коллекция при срезе
        """
        if isinstance(index, slice):
            return StudentCollection(self._items[index])
        if isinstance(index, int):
            # Преобразуем отрицательный индекс в положительный
            if index < 0:
                index = len(self._items) + index
            if 0 <= index < len(self._items):
                return self._items[index]
            raise IndexError(f"Индекс {index} вне диапазона (0..{len(self._items) - 1})")
        raise TypeError(f"Неподдерживаемый тип индекса: {type(index)}")

    def __setitem__(self, index: int, value: Student) -> None:
        """Поддержка изменения элемента по индексу"""
        if not isinstance(value, Student):
            raise TypeError(f"Можно устанавливать только объекты типа Student")

        # Проверка на дубликат при замене
        for i, existing in enumerate(self._items):
            if i != index and existing.fio == value.fio and existing.birthdate == value.birthdate:
                raise ValueError(f"Студент с ФИО '{value.fio}' уже существует в коллекции")

        if 0 <= index < len(self._items):
            self._items[index] = value
        else:
            raise IndexError(f"Индекс {index} вне диапазона")

    def __contains__(self, item) -> bool:
        """Проверить, содержится ли объект в коллекции"""
        if not isinstance(item, Student):
            return False
        return item in self._items

    def __add__(self, other: 'StudentCollection') -> 'StudentCollection':
        """
        Объединение двух коллекций (оператор +)

        Returns:
            StudentCollection: Новая коллекция, содержащая элементы обеих коллекций
        """
        if not isinstance(other, StudentCollection):
            raise TypeError(f"Нельзя объединить StudentCollection с {type(other)}")

        new_collection = StudentCollection(self._items)
        for student in other._items:
            new_collection.add(student)
        return new_collection

    def __str__(self) -> str:
        """Строковое представление коллекции"""
        if not self._items:
            return "📦 Коллекция студентов пуста"

        result = f"📦 Коллекция студентов (всего: {len(self._items)})\n"
        result += "═" * 70 + "\n"
        for i, student in enumerate(self._items, 1):
            status_icon = "🟢" if student.is_active else "⚪"
            result += f"{i}. {status_icon} {student.fio} | {student.group} | {student.course} курс | GPA: {student.gpa:.2f} | {student.status.value}\n"
        result += "═" * 70
        return result

    def __repr__(self) -> str:
        """Подробное представление коллекции"""
        return f"StudentCollection(items={len(self._items)} студентов)"

    def display_detailed(self) -> None:
        """Вывести подробную информацию о всех студентах"""
        if not self._items:
            print("📦 Коллекция студентов пуста")
            return

        print(f"\n{'=' * 70}")
        print(f"📚 ПОДРОБНАЯ ИНФОРМАЦИЯ О СТУДЕНТАХ (всего: {len(self._items)})")
        print(f"{'=' * 70}")
        for i, student in enumerate(self._items, 1):
            print(f"\n[{i}] {student}")
            print("-" * 70)

    def display_summary(self) -> None:
        """Вывести краткую сводку по коллекции"""
        if not self._items:
            print("📦 Коллекция студентов пуста")
            return

        active_count = len(self.get_active())
        graduated_count = len(self.get_graduated())
        expelled_count = len(self.get_expelled())
        leave_count = len(self.get_on_academic_leave())

        avg_gpa = sum(s.gpa for s in self._items) / len(self._items)

        print(f"\n{'=' * 50}")
        print(f"📊 СВОДКА ПО КОЛЛЕКЦИИ")
        print(f"{'=' * 50}")
        print(f"📚 Всего студентов: {len(self._items)}")
        print(f"🟢 Активных: {active_count}")
        print(f"🎓 Выпущенных: {graduated_count}")
        print(f"❌ Отчисленных: {expelled_count}")
        print(f"📚 В академ. отпуске: {leave_count}")
        print(f"⭐ Средний GPA: {avg_gpa:.2f}")
        print(f"{'=' * 50}")