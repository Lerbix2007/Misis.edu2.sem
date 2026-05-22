"""
Модуль содержит стратегии сортировки, фильтрации и функции-обработчики
для коллекции студентов.
"""

from typing import Any

# ============================================================
# ФУНКЦИИ-ФИЛЬТРЫ (Минимум 2 + Фабрика)
# ============================================================

def is_excellent(student: Any) -> bool:
    """
    Проверяет, является ли студент отличником.

    Args:
        student: Объект студента.

    Returns:
        True, если GPA не ниже 4.8, иначе False.
    """
    return student.gpa >= 4.8


def is_bachelor(student: Any) -> bool:
    """
    Фильтрация по типу объекта (Проверка на бакалавра).

    Args:
        student: Объект студента.

    Returns:
        True, если объект относится к бакалаврам (или содержит букву 'Б' в группе).
    """
    # Если в системе используются классы из base.py:
    # return isinstance(student, BachelorStudent)
    # Универсальный вариант для демонстрации по названию группы:
    return "Б" in student.group


def make_gpa_filter(min_gpa: float):
    """
    Фабрика функций: создает фильтр для студентов с GPA выше заданного.

    Args:
        min_gpa: Минимальный средний балл.

    Returns:
        Функцию-предикат для фильтрации.
    """
    def gpa_filter(student: Any) -> bool:
        return student.gpa >= min_gpa
    return gpa_filter


# ============================================================
# СТРАТЕГИИ СОРТИРОВКИ (Минимум 3)
# ============================================================

def by_fio(student: Any) -> str:
    """
    Стратегия сортировки по ФИО в алфавитном порядке (без учета регистра).

    Args:
        student: Объект студента.

    Returns:
        ФИО студента в нижнем регистре.
    """
    return student.fio.lower()


def by_gpa(student: Any) -> float:
    """
    Стратегия сортировки по среднему баллу (GPA).

    Args:
        student: Объект студента.

    Returns:
        GPA студента.
    """
    return student.gpa


def by_group_and_gpa(student: Any) -> tuple:
    """
    Стратегия сортировки по двум атрибутам: сначала по группе, затем по GPA.

    Args:
        student: Объект студента.

    Returns:
        Кортеж (группа, GPA) для комплексной сортировки.
    """
    return (student.group, student.gpa)


# ============================================================
# ФУНКЦИИ-ОБРАБОТЧИКИ ДЛЯ MAP / APPLY
# ============================================================

def student_to_short_string(student: Any) -> str:
    """
    Преобразует объект студента в короткую информационную строку.

    Args:
        student: Объект студента.

    Returns:
        Краткая информация о студенте.
    """
    return f"{student.fio} | {student.group} | GPA: {student.gpa:.2f}"


# ============================================================
# CALLABLE-ОБЪЕКТЫ КАК СТРАТЕГИИ (Паттерн Стратегия)
# ============================================================

class ShortInfoStrategy:
    """
    Callable-стратегия для получения краткой сводки о студенте.
    """
    def __call__(self, student: Any) -> str:
        return f"{student.fio} — {student.gpa:.2f}"


class GpaBonusStrategy:
    """
    Callable-стратегия для вычисления GPA с учетом индивидуального бонуса.
    Применяется без изменения исходных данных объекта.
    """
    def __init__(self, bonus: float):
        self.bonus = bonus

    def __call__(self, student: Any) -> str:
        new_gpa = min(round(student.gpa + self.bonus, 2), 5.0)
        return f"{student.fio}: {student.gpa:.2f} → {new_gpa:.2f}"
