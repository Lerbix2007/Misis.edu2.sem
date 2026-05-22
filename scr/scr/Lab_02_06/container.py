# container.py
import sys
from pathlib import Path
from typing import TypeVar, Generic, List, Optional, Iterator, Callable, Any, Protocol

# Настройка путей для импорта существующих классов
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

lab_02_02_path = project_root / "Lab_02_02"
lab_02_03_path = project_root / "Lab_02_03"

sys.path.insert(0, str(lab_02_02_path))
sys.path.insert(0, str(lab_02_03_path))

from model import Student, StudentStatus
from base import BachelorStudent, MasterStudent
from collection import StudentCollection  # оригинальная коллекция (не используется напрямую)


# === PROTOCOL 1: Displayable ===
class Displayable(Protocol):
    """Протокол для объектов, которые могут отображать информацию о себе"""

    def display(self) -> str:
        """
        Вернуть строковое представление объекта для отображения.

        Returns:
            str: Отформатированная строка с информацией об объекте
        """
        ...


# === PROTOCOL 2: Scorable ===
class Scorable(Protocol):
    """Протокол для объектов, которые имеют числовую оценку/рейтинг"""

    def score(self) -> float:
        """
        Вернуть числовую оценку объекта.

        Returns:
            float: Числовая оценка (например, GPA, рейтинг)
        """
        ...


# === TypeVar с ограничением (bound) ===
D = TypeVar('D', bound=Displayable)  # Только объекты с методом display()
S = TypeVar('S', bound=Scorable)  # Только объекты с методом score()
T = TypeVar('T')  # Универсальный тип (без ограничений)
R = TypeVar('R')  # Для map


class TypedCollection(Generic[T]):
    """
    Generic-версия коллекции, которая хранит элементы определённого типа T.
    """

    def __init__(self, items: Optional[List[T]] = None) -> None:
        self._items: List[T] = []
        if items:
            for item in items:
                self.add(item)

    def add(self, item: T) -> None:
        """Добавить элемент в коллекцию"""
        self._items.append(item)

    def add_all(self, items: List[T]) -> None:
        """Добавить несколько элементов"""
        for item in items:
            self.add(item)

    def remove(self, item: T) -> bool:
        """Удалить элемент"""
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False

    def remove_at(self, index: int) -> Optional[T]:
        """Удалить элемент по индексу"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def get_all(self) -> List[T]:
        """Получить все элементы"""
        return self._items.copy()

    def get_by_index(self, index: int) -> Optional[T]:
        """Получить элемент по индексу"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    # === НОВЫЕ МЕТОДЫ ===

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Найти первый элемент, удовлетворяющий условию"""
        for item in self._items:
            if predicate(item):
                return item
        return None

    # container.py (исправленная версия методов filter, filter_by)

    def filter(self, predicate: Callable[[T], bool]) -> "TypedCollection[T]":

        filtered_items: List[T] = [item for item in self._items if predicate(item)]
        return TypedCollection[T](filtered_items)

    def filter_to_list(self, predicate: Callable[[T], bool]) -> List[T]:

        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:

        return [transform(item) for item in self._items]

    # === МЕТОДЫ ФИЛЬТРАЦИИ И СОРТИРОВКИ ===

    def filter_by(self, predicate: Callable[[T], bool]) -> "TypedCollection[T]":
        """Отфильтровать коллекцию (возвращает новую)"""
        filtered_items: List[T] = [item for item in self._items if predicate(item)]
        return TypedCollection[T](filtered_items)

    def sort_by(self, key_func: Callable[[T], Any], reverse: bool = False) -> "TypedCollection[T]":
        """Отсортировать коллекцию (возвращает новую)"""
        sorted_items: List[T] = sorted(self._items, key=key_func, reverse=reverse)
        return TypedCollection[T](sorted_items)

    def apply(self, func: Callable[[T], Any]) -> List[Any]:
        """Применить функцию ко всем элементам"""
        return [func(item) for item in self._items]

    # === МАГИЧЕСКИЕ МЕТОДЫ ===

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        if index < 0:
            index = len(self._items) + index
        if 0 <= index < len(self._items):
            return self._items[index]
        raise IndexError(f"Индекс {index} вне диапазона")

    def __setitem__(self, index: int, value: T) -> None:
        if index < 0:
            index = len(self._items) + index
        if 0 <= index < len(self._items):
            self._items[index] = value
        else:
            raise IndexError(f"Индекс {index} вне диапазона")

    def __contains__(self, item: object) -> bool:
        return item in self._items

    def __str__(self) -> str:
        if not self._items:
            return "📦 Коллекция пуста"

        result: str = f"📦 TypedCollection<T> (всего: {len(self._items)})\n"
        result += "═" * 70 + "\n"
        for i, item in enumerate(self._items, 1):
            result += f"{i}. {item}\n"
        result += "═" * 70
        return result

    def __repr__(self) -> str:
        return f"TypedCollection(items={len(self._items)} элементов)"