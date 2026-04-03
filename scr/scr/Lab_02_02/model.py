from datetime import datetime
from typing import Optional, Union
from enum import Enum
from pathlib import Path
import sys
current_file = Path(__file__).resolve()           # .../scr/Lab_02_02/model.py
project_root = current_file.parent.parent         # .../scr/

sys.path.insert(0, str(project_root))

# Импорт из Lab_02_01/validate.py
from Lab_02_01.validate import (
    validate_fio,
    validate_birthdate,
    validate_group,
    validate_gpa,
    validate_course_upgrade
)


class StudentStatus(Enum):
    """Статусы студента (логическое состояние)"""
    ACTIVE = "Активный"
    ACADEMIC_LEAVE = "Академический отпуск"
    GRADUATED = "Выпущен"
    EXPELLED = "Отчислен"
    TRANSFERRED = "Переведен"


class Student:
    """
    Класс студента с инкапсуляцией, валидацией и логическим состоянием
    """

    # АТРИБУТЫ КЛАССА
    university_name = "МИСИС"
    total_students = 0
    MAX_COURSE = 4  # Максимальный курс бакалавриата

    def __init__(self, fio: str, birthdate: str, group: str, gpa: float):
        """
        Конструктор с проверкой данных через внешний модуль валидации
        """
        # Валидация через вынесенные методы (НЕТ ДУБЛИРОВАНИЯ)
        self._fio = validate_fio(fio)
        self._birthdate = validate_birthdate(birthdate, min_age=16, max_age=100)
        self._group = validate_group(group)
        self._gpa = validate_gpa(gpa)

        # Вычисляемые поля
        self._course = self._calculate_course()

        # ЛОГИЧЕСКОЕ СОСТОЯНИЕ
        self._status = StudentStatus.ACTIVE  # Начальное состояние

        # Увеличиваем счетчик
        Student.total_students += 1

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
        Вычисляет текущий курс студента на основе даты рождения
        """
        age = self.get_age()

        if age < 17:
            return 0  # абитуриент
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

    # === СВОЙСТВА (GETTERS) ===

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
        """Геттер для статуса студента"""
        return self._status

    @property
    def is_active(self) -> bool:
        """Проверка, активен ли студент"""
        return self._status == StudentStatus.ACTIVE

    # === СЕТТЕРЫ (используют модуль валидации) ===

    @fio.setter
    def fio(self, value: str) -> None:
        """Использует validate_fio из внешнего модуля"""
        self._fio = validate_fio(value)

    @birthdate.setter
    def birthdate(self, value: str) -> None:
        """Использует validate_birthdate из внешнего модуля"""
        self._birthdate = validate_birthdate(value, min_age=16, max_age=100)

    @group.setter
    def group(self, value: str) -> None:
        """Использует validate_group из внешнего модуля"""
        self._group = validate_group(value)

    @gpa.setter
    def gpa(self, value: Union[int, float]) -> None:
        """Использует validate_gpa из внешнего модуля"""
        self._gpa = validate_gpa(value)

    # === МЕТОДЫ ИЗМЕНЕНИЯ СОСТОЯНИЯ ===

    def activate(self) -> None:
        """
        Активировать студента (перевести в активный статус)
        """
        if self._status == StudentStatus.GRADUATED:
            raise ValueError("Нельзя активировать выпущенного студента")

        if self._status == StudentStatus.EXPELLED:
            raise ValueError("Нельзя активировать отчисленного студента")

        print(f"✅ Студент {self._fio} активирован")
        self._status = StudentStatus.ACTIVE

    def take_academic_leave(self) -> None:
        """
        Отправить студента в академический отпуск
        """
        if not self.is_active:
            raise ValueError(f"Нельзя отправить в отпуск студента со статусом: {self._status.value}")

        if self._course >= Student.MAX_COURSE:
            raise ValueError("Студент на последнем курсе, академический отпуск невозможен")

        print(f"📚 Студент {self._fio} отправлен в академический отпуск")
        self._status = StudentStatus.ACADEMIC_LEAVE

    def graduate(self) -> None:
        """
        Выпустить студента
        """
        if not self.is_active:
            raise ValueError(f"Нельзя выпустить студента со статусом: {self._status.value}")

        if self._course < Student.MAX_COURSE:
            remaining = Student.MAX_COURSE - self._course
            raise ValueError(f"Нельзя выпустить студента {self._course} курса. Осталось {remaining} курсов")

        if self._gpa < 3.0:
            raise ValueError(f"Нельзя выпустить студента с GPA {self._gpa} (нужно минимум 3.0)")

        print(f"🎓 Студент {self._fio} выпущен!")
        self._status = StudentStatus.GRADUATED

    def expel(self, reason: str = "Не указана") -> None:
        """
        Отчислить студента

        Args:
            reason: Причина отчисления
        """
        if self._status == StudentStatus.GRADUATED:
            raise ValueError("Нельзя отчислить выпущенного студента")

        if self._status == StudentStatus.EXPELLED:
            raise ValueError("Студент уже отчислен")

        print(f"⚠️ Студент {self._fio} отчислен. Причина: {reason}")
        self._status = StudentStatus.EXPELLED

    def upgrade_course(self) -> None:
        """
        Повысить курс студента (перевести на следующий курс)
        ПОВЕДЕНИЕ ЗАВИСИТ ОТ СОСТОЯНИЯ
        """
        # ПРОВЕРКА СОСТОЯНИЯ - поведение ограничено
        if not self.is_active:
            raise ValueError(
                f"Нельзя повысить курс студента со статусом: {self._status.value}. "
                f"Только активные студенты могут переводиться на следующий курс"
            )
        if self._course >= Student.MAX_COURSE:
            raise ValueError(
                f"Нельзя повысить курс студента {self._fio}, так как он уже на {self._course} курсе. "
                f"Максимальный курс бакалавриата: {Student.MAX_COURSE}"
            )
        # Используем валидацию из модуля
        new_course = validate_course_upgrade(self._course, Student.MAX_COURSE)
        self._course = new_course
        print(f"📈 Студент {self._fio} переведен на {self._course} курс")

    def add_points(self, points: float) -> None:
        """
        Добавить баллы к GPA (поведение зависит от состояния)
        """
        # ПОВЕДЕНИЕ ЗАВИСИТ ОТ СОСТОЯНИЯ
        if self._status == StudentStatus.GRADUATED:
            raise ValueError("Нельзя изменять GPA выпущенного студента")

        if self._status == StudentStatus.EXPELLED:
            raise ValueError("Нельзя изменять GPA отчисленного студента")

        new_gpa = self._gpa + points
        # Валидация через модуль
        self._gpa = validate_gpa(new_gpa)
        print(f"⭐ GPA студента {self._fio} изменен: {self._gpa:.2f}")

    # === БИЗНЕС-МЕТОДЫ ===

    def get_age(self) -> int:
        """Вычисляет возраст студента"""
        return self._calculate_age_from_date(self._birthdate)

    def get_gpa_grade(self) -> str:
        """Переводит GPA в буквенную оценку"""
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
        """Генерирует номер студенческого билета"""
        import hashlib
        hash_input = f"{self._fio}{self._birthdate}".encode()
        student_id = hashlib.md5(hash_input).hexdigest()[:8].upper()
        return f"СТУД-{self._group[:4]}-{student_id}"

    # === МАГИЧЕСКИЕ МЕТОДЫ ===

    def __str__(self) -> str:
        status_icon = {
            StudentStatus.ACTIVE: "🟢",
            StudentStatus.ACADEMIC_LEAVE: "📚",
            StudentStatus.GRADUATED: "🎓",
            StudentStatus.EXPELLED: "❌",
            StudentStatus.TRANSFERRED: "🔄"
        }.get(self._status, "⚪")

        return (
            f"┌─ СТУДЕНТ {'=' * 50}\n"
            f"│ {status_icon} ФИО: {self._fio}\n"
            f"│ Дата рождения: {self.birthdate} (возраст: {self.get_age()} лет)\n"
            f"│ Группа: {self._group} (курс: {self.course})\n"
            f"│ Средний балл: {self._gpa:.2f} → {self.get_gpa_grade()}\n"
            f"│ Студенческий билет: {self.get_student_card()}\n"
            f"│ Университет: {Student.university_name}\n"
            f"│ Статус: {self._status.value}\n"
            f"└─{'─' * 60}"
        )

    def __repr__(self) -> str:
        return (
            f"Student("
            f"fio='{self._fio}', "
            f"birthdate='{self._birthdate.strftime('%Y-%m-%d')}', "
            f"group='{self._group}', "
            f"gpa={self._gpa:.2f}, "
            f"status='{self._status.value}'"
            f")"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Student):
            return False
        return (self._fio == other._fio and
                self._birthdate == other._birthdate)