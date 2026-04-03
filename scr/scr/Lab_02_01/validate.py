import re
from datetime import datetime
from typing import Union


def validate_fio(value: str) -> str:
    """
    Валидация ФИО студента

    Args:
        value: ФИО для проверки

    Returns:
        Очищенное и нормализованное ФИО

    Raises:
        ValueError: если ФИО не соответствует требованиям
    """
    if not isinstance(value, str):
        raise ValueError("ФИО должно быть строкой")

    value = value.strip()
    if not value:
        raise ValueError("ФИО не может быть пустым")

    if len(value) < 3:
        raise ValueError("ФИО должно содержать минимум 3 символа")

    words = value.split()
    if len(words) < 2:
        raise ValueError("ФИО должно содержать минимум имя и фамилию")

    # Проверка на недопустимые символы (только буквы, пробелы, дефисы)
    if not re.match(r'^[А-Яа-яЁёA-Za-z\s-]+$', value):
        raise ValueError("ФИО может содержать только буквы, пробелы и дефисы")

    return value


def validate_birthdate(value: str, min_age: int = 16, max_age: int = 100) -> datetime.date:
    """
    Валидация даты рождения

    Args:
        value: Дата рождения в формате ГГГГ-ММ-ДД
        min_age: Минимальный допустимый возраст
        max_age: Максимальный допустимый возраст

    Returns:
        Объект date

    Raises:
        ValueError: если дата не соответствует требованиям
    """
    try:
        birth_date = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Некорректная дата рождения: {value}. Используйте формат ГГГГ-ММ-ДД") from e

    # Проверка: дата не может быть в будущем
    today = datetime.now().date()
    if birth_date > today:
        raise ValueError("Дата рождения не может быть в будущем")

    # Вычисляем возраст
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    # Проверка минимального возраста
    if age < min_age:
        raise ValueError(f"Студент должен быть не младше {min_age} лет (текущий возраст: {age})")

    # Проверка максимального возраста
    if age > max_age:
        raise ValueError(f"Некорректный возраст: {age} лет (максимум {max_age})")

    return birth_date


def validate_group(value: str) -> str:
    """
    Валидация номера группы

    Args:
        value: Номер группы

    Returns:
        Очищенный и нормализованный номер группы

    Raises:
        ValueError: если группа не соответствует формату
    """
    if not isinstance(value, str):
        raise ValueError("Группа должна быть строкой")

    value = value.strip().upper()
    if not value:
        raise ValueError("Группа не может быть пустой")

    # Формат: БИВТ-21-1, ИВТ-20-2, ПМИ-22-3
    if not re.match(r'^[А-Я]{2,6}-\d{2}-\d$', value):
        raise ValueError(
            f"Неверный формат группы: '{value}'. "
            f"Ожидается формат 'БИВТ-21-1' (2-6 букв, дефис, 2 цифры, дефис, 1 цифра)"
        )

    return value


def validate_gpa(value: Union[int, float]) -> float:
    """
    Валидация среднего балла GPA

    Args:
        value: Средний балл

    Returns:
        Нормализованное значение GPA

    Raises:
        ValueError: если GPA не соответствует требованиям
    """
    if not isinstance(value, (int, float)):
        raise ValueError("Средний балл должен быть числом")

    gpa_value = float(value)

    if gpa_value < 0 or gpa_value > 5:
        raise ValueError(f"Средний балл должен быть от 0 до 5 (получено: {gpa_value})")

    if round(gpa_value, 2) != gpa_value:
        raise ValueError("Средний балл должен иметь не более 2 знаков после запятой")

    return gpa_value


def validate_course_upgrade(current_course: int, max_course: int = 4) -> int:
    """
    Валидация повышения курса

    Args:
        current_course: Текущий курс
        max_course: Максимальный допустимый курс

    Returns:
        Новый курс

    Raises:
        ValueError: если повышение невозможно
    """
    if not isinstance(current_course, int):
        raise ValueError("Курс должен быть целым числом")

    if current_course < 0:
        raise ValueError(f"Некорректный курс: {current_course}")

    new_course = current_course + 1

    if new_course > max_course:
        raise ValueError(f"Нельзя повысить курс выше {max_course} (текущий: {current_course})")

    return new_course