from datetime import datetime
from typing import Optional, Union

class Student:

    # АТРИБУТ КЛАССА - общий для всех студентов
    university_name = "МИСИС"
    total_students = 0

    def __init__(self, fio: str, birthdate: str, group: str, gpa: float):
        """
        Конструктор с проверкой данных
            fio: ФИО студента (не пустое, минимум 3 символа)
            birthdate: Дата рождения в формате ГГГГ-ММ-ДД (не будущее)
            group: Название группы (не пустое, соответствует формату)
            gpa: Средний балл (от 2.0 до 5.0)
        """
        # Используем сеттеры для всех полей (единая валидация)
        self.fio = fio
        self.birthdate = birthdate
        self.group = group
        self.gpa = gpa

        # Приватное поле для курса студента (будет вычисляться)
        self._course = self._calculate_course()

        # Увеличиваем счетчик студентов (атрибут класса)
        Student.total_students += 1

    # === СВОЙСТВА (GETTERS) ===

    @property
    def fio(self) -> str:
        """Геттер для ФИО"""
        return self._fio

    @property
    def birthdate(self) -> str:
        """Геттер для даты рождения в строковом формате"""
        return self._birthdate.strftime("%d.%m.%Y")

    @property
    def birthdate_raw(self) -> datetime.date:
        """Геттер для даты рождения как объекта date (для внутренних расчетов)"""
        return self._birthdate

    @property
    def group(self) -> str:
        """Геттер для группы"""
        return self._group

    @property
    def gpa(self) -> float:
        """Геттер для среднего балла"""
        return self._gpa

    @property
    def course(self) -> int:
        """Геттер для курса (вычисляется автоматически)"""
        self._course = self._calculate_course()  # Обновляем при каждом обращении
        return self._course

    # === СЕТТЕРЫ С ВАЛИДАЦИЕЙ ===

    @fio.setter
    def fio(self, value: str) -> None:
        """Сеттер для ФИО с расширенной валидацией"""
        if not isinstance(value, str):
            raise ValueError("ФИО должно быть строкой")

        value = value.strip()
        if not value:
            raise ValueError("ФИО не может быть пустым")

        if len(value) < 3:
            raise ValueError("ФИО должно содержать минимум 3 символа")

        if len(value.split()) < 2:
            raise ValueError("ФИО должно содержать минимум имя и фамилию")

        self._fio = value

    @birthdate.setter
    def birthdate(self, value: str) -> None:
        """Сеттер для даты рождения с валидацией"""
        try:
            birth_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Некорректная дата рождения: {value}. Используйте формат ГГГГ-ММ-ДД") from e

        # Проверка: дата не может быть в будущем
        today = datetime.now().date()
        if birth_date > today:
            raise ValueError("Дата рождения не может быть в будущем")

        # Проверка: возраст не может быть меньше 16 лет
        age = self._calculate_age_from_date(birth_date)
        if age < 16:
            raise ValueError(f"Студент должен быть не младше 16 лет (текущий возраст: {age})")

        # Проверка: возраст не может быть больше 100 лет
        if age > 100:
            raise ValueError(f"Некорректный возраст: {age} лет")

        self._birthdate = birth_date

    @group.setter
    def group(self, value: str) -> None:
        """Сеттер для группы с валидацией формата"""
        if not isinstance(value, str):
            raise ValueError("Группа должна быть строкой")

        value = value.strip().upper()
        if not value:
            raise ValueError("Группа не может быть пустой")

        # Проверка формата группы: БИВТ-21-1, ИВТ-20-2, etc.
        import re
        if not re.match(r'^[А-Я]{2,6}-\d{2}-\d$', value):
            raise ValueError("Группа должна быть в формате 'БИВТ-21-1' (буквы-год-номер)")

        self._group = value

    @gpa.setter
    def gpa(self, value: Union[int, float]) -> None:
        """Сеттер для среднего балла с валидацией"""
        if not isinstance(value, (int, float)):
            raise ValueError("Средний балл должен быть числом")

        # Приводим к float
        gpa_value = float(value)

        # Проверка диапазона (в российских вузах обычно 2-5)
        if gpa_value < 2.0:
            raise ValueError("Средний балл не может быть ниже 2.0 (неудовлетворительно)")
        if gpa_value > 5.0:
            raise ValueError("Средний балл не может быть выше 5.0")

        # Проверка на точность (не более 2 знаков после запятой)
        if round(gpa_value, 2) != gpa_value:
            raise ValueError("Средний балл должен иметь не более 2 знаков после запятой")

        self._gpa = gpa_value

    # === ПРИВАТНЫЕ МЕТОДЫ ===

    def _calculate_age_from_date(self, birth_date: datetime.date) -> int:
        """Вычисляет возраст на основе даты рождения"""
        today = datetime.now().date()
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def _calculate_course(self) -> int:
        """
        Вычисляет текущий курс студента на основе даты поступления
        Предполагаем, что студенты поступают в 17-18 лет и учатся 4 года
        """
        age = self.get_age()

        # Примерная логика: 1 курс - 17-18 лет, 2 курс - 18-19, etc.
        if age < 17:
            return 0  # еще не студент (абитуриент)
        elif 17 <= age <= 18:
            return 1
        elif 18 <= age <= 19:
            return 2
        elif 19 <= age <= 20:
            return 3
        elif 20 <= age <= 21:
            return 4
        else:
            return 5  # выпускник или магистр

    # === БИЗНЕС-МЕТОДЫ ===

    def get_age(self) -> int:
        """
        Бизнес-метод 1: вычисляет возраст студента на текущую дату

        Returns:
            Возраст в годах
        """
        return self._calculate_age_from_date(self._birthdate)

    def get_gpa_grade(self) -> str:
        """
        Бизнес-метод 2: возвращает буквенную оценку на основе GPA

        Returns:
            Буквенная оценка (A, B, C, D, F)
        """
        if self._gpa >= 4.8:
            return "A (Отлично)"
        elif self._gpa >= 4.0:
            return "B (Хорошо)"
        elif self._gpa >= 3.0:
            return "C (Удовлетворительно)"
        elif self._gpa >= 2.0:
            return "D (Неудовлетворительно)"
        else:
            return "F (Провал)"

    def get_student_card(self) -> str:
        """
        Бизнес-метод 3 (дополнительный): генерирует студенческий билет
        """
        import hashlib
        # Генерируем уникальный номер на основе ФИО и даты
        hash_input = f"{self._fio}{self._birthdate}".encode()
        student_id = hashlib.md5(hash_input).hexdigest()[:8].upper()

        return f"СТУД-{self._group[:4]}-{student_id}"

    # === МАГИЧЕСКИЕ МЕТОДЫ ===

    def __str__(self) -> str:
        """
        Строковое представление для пользователей (красивое форматирование)
        """
        age = self.get_age()
        grade = self.get_gpa_grade()

        return (
            f"┌─ СТУДЕНТ {'=' * 50}\n"
            f"│  ФИО: {self._fio}\n"
            f"│  Дата рождения: {self.birthdate} (возраст: {age} лет)\n"
            f"│  Группа: {self._group} (курс: {self.course})\n"
            f"│  Средний балл: {self._gpa:.2f} → {grade}\n"
            f"│  Студенческий билет: {self.get_student_card()}\n"
            f"│  Университет: {Student.university_name}\n"
            f"└─{'─' * 60}"
        )

    def __repr__(self) -> str:
        """
        Официальное строковое представление для разработчиков
        """
        return (
            f"Student("
            f"fio='{self._fio}', "
            f"birthdate='{self._birthdate.strftime('%Y-%m-%d')}', "
            f"group='{self._group}', "
            f"gpa={self._gpa:.2f}"
            f")"
        )

    def __eq__(self, other) -> bool:
        """
        Сравнение студентов по ФИО и дате рождения
        (считаем, что это уникальные характеристики)
        """
        if not isinstance(other, Student):
            return False

        return (self._fio == other._fio and
                self._birthdate == other._birthdate)

    def __del__(self):
        """Деструктор для уменьшения счетчика студентов"""
        Student.total_students = 4