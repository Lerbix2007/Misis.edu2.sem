# exceptions.py
"""Модуль с пользовательскими исключениями для предметной области."""


class StudentNotFoundError(Exception):
    """Студент не найден в коллекции."""
    pass


class DuplicateStudentError(Exception):
    """Студент с таким ФИО и датой рождения уже существует."""
    pass


class InvalidStudentDataError(Exception):
    """Некорректные данные студента."""
    pass


class InvalidIndexError(Exception):
    """Некорректный индекс в коллекции."""
    pass


class EmptyCollectionError(Exception):
    """Коллекция пуста."""
    pass


class SaveLoadError(Exception):
    """Ошибка при сохранении или загрузке данных."""
    pass