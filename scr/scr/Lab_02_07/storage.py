# storage.py
"""Модуль для сохранения и загрузки коллекции в JSON-файл."""

import json
from pathlib import Path
from typing import List, Any

from exceptions import SaveLoadError


def student_to_dict(student: Any) -> dict:
    """
    Преобразует студента в словарь для JSON.

    Args:
        student: Объект студента

    Returns:
        Словарь с данными студента
    """
    return {
        "type": student.__class__.__name__,
        "fio": student.fio,
        "birthdate": student.birthdate_raw.strftime("%Y-%m-%d"),  # ГГГГ-ММ-ДД
        "group": student.group,
        "gpa": student.gpa,
        "status": student.status.value,
        "specialization": getattr(student, "specialization", None),
        "has_thesis": getattr(student, "has_thesis", None),
        "research_area": getattr(student, "research_area", None),
        "supervisor": getattr(student, "supervisor", None),
        "papers_count": getattr(student, "papers_count", None)
    }


def dict_to_student(data: dict) -> Any:
    """
    Восстанавливает студента из словаря.

    Args:
        data: Словарь с данными студента

    Returns:
        Восстановленный объект студента

    Raises:
        ValueError: Если тип студента неизвестен
    """
    import sys
    from pathlib import Path

    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent

    lab_02_02_path = project_root / "Lab_02_02"
    lab_02_03_path = project_root / "Lab_02_03"

    sys.path.insert(0, str(lab_02_02_path))
    sys.path.insert(0, str(lab_02_03_path))

    from model import Student
    from base import BachelorStudent, MasterStudent

    # Дата уже в правильном формате ГГГГ-ММ-ДД из JSON
    birthdate = data["birthdate"]  # строка вида "2005-05-15"

    if data["type"] == "Student":
        return Student(
            data["fio"], birthdate, data["group"], data["gpa"]
        )
    elif data["type"] == "BachelorStudent":
        return BachelorStudent(
            data["fio"], birthdate, data["group"], data["gpa"],
            data["specialization"], data["has_thesis"]
        )
    elif data["type"] == "MasterStudent":
        return MasterStudent(
            data["fio"], birthdate, data["group"], data["gpa"],
            data["research_area"], data["supervisor"]
        )
    else:
        raise ValueError(f"Неизвестный тип студента: {data['type']}")


def save(collection: Any, filepath: str) -> None:
    """
    Сохранить коллекцию в JSON-файл.

    Args:
        collection: Коллекция студентов (должна иметь метод get_all())
        filepath: Путь к файлу для сохранения

    Raises:
        SaveLoadError: При ошибке сохранения
    """
    try:
        students = collection.get_all()
        data = [student_to_dict(s) for s in students]

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        raise SaveLoadError(f"Ошибка сохранения данных: {e}")


def load(filepath: str) -> List[Any]:
    """
    Загрузить объекты из JSON-файла.

    Args:
        filepath: Путь к файлу для загрузки

    Returns:
        list: Список восстановленных студентов

    Raises:
        SaveLoadError: При ошибке загрузки
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return []

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        students = []
        for item in data:
            try:
                student = dict_to_student(item)
                students.append(student)
            except Exception as e:
                print(f"⚠️ Пропущен некорректный объект: {e}")

        return students

    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise SaveLoadError(f"Ошибка чтения JSON: {e}")
    except Exception as e:
        raise SaveLoadError(f"Ошибка загрузки данных: {e}")