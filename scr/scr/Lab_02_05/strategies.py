
def is_active(student) -> bool:
    return student.is_active


def is_excellent(student) -> bool:
    """
    Проверяет, является ли студент отличником.
    Args:
        student: объект студента
    Returns:
        True, если GPA не ниже 4.8
    """
    return student.gpa >= 4.8

# ============================================================
# СТРАТЕГИИ СОРТИРОВКИ
# ============================================================

def by_fio(student) -> str:

    return student.fio.lower()


def by_gpa(student) -> float:
    """
    Стратегия сортировки по GPA.

    Args:
        student: объект студента

    Returns:
        GPA студента
    """
    return student.gpa


# ============================================================
# ФУНКЦИИ-ОБРАБОТЧИКИ
# ============================================================

def student_to_short_string(student) -> str:
    """
    Преобразует студента в короткую строку.
    Args:
        student: объект студента
    Returns:
        Краткая информация о студенте
    """
    return f"{student.fio} | {student.group} | GPA: {student.gpa:.2f}"


# ============================================================
# CALLABLE-ОБЪЕКТЫ КАК СТРАТЕГИИ
# ============================================================

class ShortInfoStrategy:
    """
    Callable-стратегия для получения краткой информации о студенте.
    """

    def __call__(self, student) -> str:
        return f"{student.fio} — {student.gpa:.2f}"


class GpaBonusStrategy:
    """
    Callable-стратегия для расчёта GPA с бонусом.

    Стратегия не изменяет объект, а только показывает результат.
    """

    def __init__(self, bonus: float):
        self.bonus = bonus

    def __call__(self, student) -> str:
        new_gpa = min(round(student.gpa + self.bonus, 2), 5.0)
        return f"{student.fio}: {student.gpa:.2f} → {new_gpa:.2f}"