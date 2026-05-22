
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Пути к предыдущим работам
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

lab_02_02_path = project_root / "Lab_02_02"
lab_02_05_path = project_root / "Lab_02_05"
lab_02_03_path = project_root / "Lab_02_03"


sys.path.insert(0, str(lab_02_02_path))
sys.path.insert(0, str(lab_02_05_path))
sys.path.insert(0, str(lab_02_03_path))

from collection import StudentCollection
from model import Student
from base import BachelorStudent, MasterStudent

from exceptions import (
    InvalidStudentDataError,
    InvalidIndexError,
    EmptyCollectionError
)


class StudentApp:
    """
    Слой бизнес-логики. CLI не имеет прямого доступа к коллекции.
    """

    def __init__(self, initial_students: Optional[List[Student]] = None) -> None:
        """
        Инициализация приложения.

        Args:
            initial_students: Начальный список студентов (из загрузки)
        """
        if initial_students:
            self._collection = StudentCollection(initial_students)
        else:
            self._collection = StudentCollection()

    # ============================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ============================================================

    def _create_student(self, student_type: str, **kwargs) -> Student:
        """
        Создание студента указанного типа.

        Args:
            student_type: Тип студента ("student", "bachelor", "master")
            **kwargs: Параметры студента

        Returns:
            Созданный объект студента

        Raises:
            InvalidStudentDataError: Если тип неизвестен
        """
        if student_type == "student":
            return Student(
                fio=kwargs["fio"],
                birthdate=kwargs["birthdate"],
                group=kwargs["group"],
                gpa=kwargs["gpa"]
            )
        elif student_type == "bachelor":
            return BachelorStudent(
                fio=kwargs["fio"],
                birthdate=kwargs["birthdate"],
                group=kwargs["group"],
                gpa=kwargs["gpa"],
                specialization=kwargs.get("specialization", "Общая"),
                has_thesis=kwargs.get("has_thesis", False)
            )
        elif student_type == "master":
            return MasterStudent(
                fio=kwargs["fio"],
                birthdate=kwargs["birthdate"],
                group=kwargs["group"],
                gpa=kwargs["gpa"],
                research_area=kwargs.get("research_area", "Общая"),
                supervisor=kwargs.get("supervisor", "Не назначен")
            )
        else:
            raise InvalidStudentDataError(f"Неизвестный тип студента: {student_type}")

    # ============================================================
    # ОСНОВНЫЕ ОПЕРАЦИИ
    # ============================================================

    def add_student(self, student_type: str, **kwargs) -> Tuple[bool, str]:
        """
        Добавить студента.

        Args:
            student_type: Тип студента ("student", "bachelor", "master")
            **kwargs: Параметры студента

        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        try:
            student = self._create_student(student_type, **kwargs)
            self._collection.add(student)
            return True, f"✅ Студент '{kwargs['fio']}' успешно добавлен"
        except ValueError as e:
            return False, f"❌ Ошибка валидации: {e}"
        except Exception as e:
            return False, f"❌ Непредвиденная ошибка: {e}"

    def remove_student(self, index: int, confirm: bool = False) -> Tuple[bool, str, Optional[Student]]:
        """
        Удалить студента по индексу.

        Args:
            index: Индекс студента
            confirm: Подтверждение удаления

        Returns:
            Tuple[bool, str, Optional[Student]]: (успех, сообщение, удалённый студент)
        """
        if not confirm:
            return False, "⚠️ Требуется подтверждение удаления", None

        try:
            if len(self._collection) == 0:
                return False, "❌ Коллекция пуста", None

            if index < 0 or index >= len(self._collection):
                return False, f"❌ Индекс {index} вне диапазона (0..{len(self._collection) - 1})", None

            removed = self._collection.remove_at(index)
            if removed is None:
                return False, "❌ Не удалось удалить студента", None

            return True, f"✅ Студент '{removed.fio}' удалён", removed
        except Exception as e:
            return False, f"❌ Непредвиденная ошибка: {e}", None

    def get_all_students(self) -> List[Student]:
        """Получить всех студентов."""
        return self._collection.get_all()

    def get_students_count(self) -> int:
        """Получить количество студентов."""
        return len(self._collection)

    def is_empty(self) -> bool:
        """Проверить, пуста ли коллекция."""
        return len(self._collection) == 0

    def clear_collection(self, confirm: bool = False) -> Tuple[bool, str]:
        """
        Очистить коллекцию.

        Args:
            confirm: Подтверждение очистки

        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        if not confirm:
            return False, "⚠️ Требуется подтверждение очистки"

        self._collection.clear()
        return True, "✅ Коллекция очищена"

    def get_collection(self):
        """Получить коллекцию (для сохранения)."""
        return self._collection

    # ============================================================
    # ПОИСК И ФИЛЬТРАЦИЯ
    # ============================================================

    def find_by_fio(self, substring: str) -> Tuple[List[Student], str]:
        """
        Поиск студентов по ФИО.

        Args:
            substring: Часть ФИО для поиска

        Returns:
            Tuple[List[Student], str]: (результаты, сообщение)
        """
        if not substring:
            return [], "❌ Введите текст для поиска"

        results = self._collection.find_by_fio(substring, exact_match=False)
        if not results:
            return [], f"❌ Студенты с ФИО, содержащим '{substring}', не найдены"

        return results, f"🔍 Найдено {len(results)} студентов"

    def find_by_group(self, group: str) -> Tuple[List[Student], str]:
        """
        Поиск студентов по группе.

        Args:
            group: Номер группы

        Returns:
            Tuple[List[Student], str]: (результаты, сообщение)
        """
        if not group:
            return [], "❌ Введите номер группы"

        results = self._collection.find_by_group(group, exact_match=True)
        if not results:
            return [], f"❌ Студенты в группе '{group}' не найдены"

        return results, f"🔍 Найдено {len(results)} студентов в группе '{group}'"

    def filter_by_excellent(self) -> Tuple[List[Student], str]:
        """Фильтрация отличников (GPA >= 4.8)."""
        results = self._collection.get_excellent_students().get_all()
        if not results:
            return [], "❌ Отличников не найдено"

        return results, f"🏆 Найдено {len(results)} отличников (GPA >= 4.8)"

    def filter_by_gpa_range(self, min_gpa: float, max_gpa: float) -> Tuple[List[Student], str]:
        """
        Фильтрация по диапазону GPA.

        Args:
            min_gpa: Минимальный GPA
            max_gpa: Максимальный GPA

        Returns:
            Tuple[List[Student], str]: (результаты, сообщение)
        """
        if min_gpa > max_gpa:
            return [], "❌ Минимальный GPA не может быть больше максимального"

        results = self._collection.get_by_gpa_range(min_gpa, max_gpa).get_all()
        if not results:
            return [], f"❌ Студенты с GPA в диапазоне [{min_gpa}, {max_gpa}] не найдены"

        return results, f"📊 Найдено {len(results)} студентов с GPA от {min_gpa} до {max_gpa}"

    def filter_by_course(self, course: int) -> Tuple[List[Student], str]:
        """
        Фильтрация по курсу.

        Args:
            course: Номер курса

        Returns:
            Tuple[List[Student], str]: (результаты, сообщение)
        """
        if course < 1 or course > 4:
            return [], f"❌ Курс должен быть от 1 до 4 (получено: {course})"

        results = self._collection.get_by_course(course).get_all()
        if not results:
            return [], f"❌ Студенты {course} курса не найдены"

        return results, f"📚 Найдено {len(results)} студентов {course} курса"

    def filter_by_active(self) -> Tuple[List[Student], str]:
        """Фильтрация активных студентов."""
        results = self._collection.get_active().get_all()
        if not results:
            return [], "❌ Активные студенты не найдены"

        return results, f"🟢 Найдено {len(results)} активных студентов"

    # ============================================================
    # СОРТИРОВКА
    # ============================================================

    def sort_by_fio(self) -> str:
        """Сортировка по ФИО."""
        self._collection.sort_by_fio()
        return "✅ Отсортировано по ФИО"

    def sort_by_gpa(self) -> str:
        """Сортировка по GPA (по убыванию)."""
        self._collection.sort_by_gpa(reverse=True)
        return "✅ Отсортировано по GPA (по убыванию)"

    def sort_by_course(self) -> str:
        """Сортировка по курсу."""
        self._collection.sort_by_course()
        return "✅ Отсортировано по курсу"

    def sort_by_age(self) -> str:
        """Сортировка по возрасту."""
        self._collection.sort_by_age()
        return "✅ Отсортировано по возрасту"

    def sort_by_group(self) -> str:
        """Сортировка по группе."""
        self._collection.sort_by_group()
        return "✅ Отсортировано по группе"

    # ============================================================
    # МЕТОДЫ ДЛЯ ВЫВОДА ДАННЫХ
    # ============================================================

    def get_table_string(self) -> str:
        """Получить форматированную таблицу студентов (без рамок)."""
        if len(self._collection) == 0:
            return "📦 Коллекция пуста"

        lines = []

        # Заголовки
        lines.append(f"{'№':<4} {'ФИО':<35} {'Группа':<14} {'GPA':<6} {'Курс':<6} {'Статус':<10}")
        lines.append("-" * 80)

        for i, student in enumerate(self._collection):
            status = "Активен" if student.is_active else "Неактивен"
            # Форматирование с выравниванием
            lines.append(
                f"{i:<4} {student.fio:<35} {student.group:<14} {student.gpa:<6.2f} {student.course:<6} {status:<10}")

        lines.append(f"\n📊 Итого: {len(self._collection)} студентов")

        return "\n".join(lines)

    def get_short_info_list(self) -> List[str]:
        """Получить краткую информацию о студентах."""
        return [f"{s.fio} | {s.group} | GPA: {s.gpa:.2f}" for s in self._collection]