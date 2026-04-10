# model.py
from datetime import datetime
from enum import Enum
from typing import Optional, Union


class StudentStatus(Enum):
    ACTIVE = "Активный"
    ACADEMIC_LEAVE = "Академический отпуск"
    GRADUATED = "Выпущен"
    EXPELLED = "Отчислен"
    TRANSFERRED = "Переведен"


class Student:
    """Базовый класс студента (модель сущности)"""

    university_name = "МИСИС"
    total_students = 0
    MAX_COURSE = 4

    def __init__(self, fio: str, birthdate: str, group: str, gpa: float):
        self._fio = self._validate_fio(fio)
        self._birthdate = self._validate_birthdate(birthdate)
        self._group = self._validate_group(group)
        self._gpa = self._validate_gpa(gpa)
        self._course = self._calculate_course()
        self._status = StudentStatus.ACTIVE
        Student.total_students += 1

    # --- Приватные валидаторы (упрощённые, но можно заменить на импорт из validate.py) ---
    def _validate_fio(self, fio: str) -> str:
        if not isinstance(fio, str) or len(fio.strip()) < 5:
            raise ValueError("ФИО должно быть строкой длиной не менее 5 символов")
        return fio.strip()

    def _validate_birthdate(self, birthdate: str) -> datetime.date:
        try:
            date = datetime.strptime(birthdate, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Дата рождения должна быть в формате ГГГГ-ММ-ДД")
        age = self._calculate_age(date)
        if not (16 <= age <= 100):
            raise ValueError("Возраст должен быть от 16 до 100 лет")
        return date

    def _validate_group(self, group: str) -> str:
        if not isinstance(group, str) or len(group) < 3:
            raise ValueError("Название группы должно быть не короче 3 символов")
        return group.strip()

    def _validate_gpa(self, gpa: float) -> float:
        gpa = float(gpa)
        if not (0 <= gpa <= 5):
            raise ValueError("GPA должен быть в диапазоне 0..5")
        return gpa

    def _calculate_age(self, birth_date: datetime.date) -> int:
        today = datetime.now().date()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    def _calculate_course(self) -> int:
        age = self.get_age()
        if age < 17:
            return 0
        elif 17 <= age <= 18:
            return 1
        elif 18 <= age <= 19:
            return 2
        elif 19 <= age <= 20:
            return 3
        elif 20 <= age <= 21:
            return 4
        else:
            return 5

    # --- Геттеры ---
    @property
    def fio(self) -> str:
        return self._fio

    @property
    def birthdate(self) -> str:
        return self._birthdate.strftime("%d.%m.%Y")

    @property
    def birthdate_raw(self) -> datetime.date:
        return self._birthdate

    @property
    def group(self) -> str:
        return self._group

    @property
    def gpa(self) -> float:
        return self._gpa

    @property
    def course(self) -> int:
        self._course = self._calculate_course()
        return self._course

    @property
    def status(self) -> StudentStatus:
        return self._status

    @property
    def is_active(self) -> bool:
        return self._status == StudentStatus.ACTIVE

    # --- Сеттеры ---
    @fio.setter
    def fio(self, value: str):
        self._fio = self._validate_fio(value)

    @birthdate.setter
    def birthdate(self, value: str):
        self._birthdate = self._validate_birthdate(value)

    @group.setter
    def group(self, value: str):
        self._group = self._validate_group(value)

    @gpa.setter
    def gpa(self, value: Union[int, float]):
        self._gpa = self._validate_gpa(value)

    # --- Бизнес-методы ---
    def get_age(self) -> int:
        return self._calculate_age(self._birthdate)

    def get_gpa_grade(self) -> str:
        if self._gpa >= 4.8:
            return "A (Отлично)"
        elif self._gpa >= 4.0:
            return "B (Хорошо)"
        elif self._gpa >= 3.0:
            return "C (Удовлетворительно)"
        else:
            return "F (Неудовлетворительно)"

    # *** ОБЩИЙ ИНТЕРФЕЙС (полиморфный метод) ***
    def get_scholarship_amount(self) -> int:
        """Базовая стипендия (для обычного студента)"""
        if self._gpa >= 4.5:
            return 2000
        elif self._gpa >= 4.0:
            return 1500
        elif self._gpa >= 3.0:
            return 1000
        else:
            return 0

    def get_student_card(self) -> str:
        import hashlib
        hash_input = f"{self._fio}{self._birthdate}".encode()
        student_id = hashlib.md5(hash_input).hexdigest()[:8].upper()
        return f"СТУД-{self._group[:4]}-{student_id}"

    # --- Методы изменения статуса (упрощённые для демонстрации) ---
    def activate(self):
        if self._status in (StudentStatus.GRADUATED, StudentStatus.EXPELLED):
            raise ValueError("Нельзя активировать выпущенного или отчисленного")
        self._status = StudentStatus.ACTIVE

    def graduate(self):
        if not self.is_active:
            raise ValueError("Только активный студент может быть выпущен")
        if self._course < Student.MAX_COURSE:
            raise ValueError("Нельзя выпустить студента младшего курса")
        self._status = StudentStatus.GRADUATED

    def expel(self, reason=""):
        if self._status == StudentStatus.GRADUATED:
            raise ValueError("Нельзя отчислить выпущенного")
        self._status = StudentStatus.EXPELLED

    def upgrade_course(self):
        if not self.is_active:
            raise ValueError("Только активный студент может переходить на следующий курс")
        if self._course >= Student.MAX_COURSE:
            raise ValueError("Максимальный курс достигнут")
        self._course += 1

    # --- Магические методы ---
    def __str__(self) -> str:
        status_icon = {
            StudentStatus.ACTIVE: "🟢",
            StudentStatus.ACADEMIC_LEAVE: "📚",
            StudentStatus.GRADUATED: "🎓",
            StudentStatus.EXPELLED: "❌",
        }.get(self._status, "⚪")
        return (
            f"┌─ СТУДЕНТ {'=' * 50}\n"
            f"│ {status_icon} ФИО: {self._fio}\n"
            f"│ 🎂 Дата рождения: {self.birthdate} ({self.get_age()} лет)\n"
            f"│ 📚 Группа: {self._group} (курс: {self.course})\n"
            f"│ 📊 GPA: {self._gpa:.2f} → {self.get_gpa_grade()}\n"
            f"│ 🆔 Студбилет: {self.get_student_card()}\n"
            f"│ 🏫 Университет: {Student.university_name}\n"
            f"│ 📍 Статус: {self._status.value}\n"
            f"└─{'─' * 60}"
        )

    def __repr__(self):
        return f"Student(fio='{self._fio}', group='{self._group}', gpa={self._gpa})"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self._fio == other._fio and self._birthdate == other._birthdate