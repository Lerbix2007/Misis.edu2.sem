# demo.py
import sys
from pathlib import Path

# Настройка путей для импорта существующих классов из предыдущих работ
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # scr/

lab_02_01_path = project_root / "Lab_02_01"
lab_02_02_path = project_root / "Lab_02_02"
lab_02_03_path = project_root / "Lab_02_03"

sys.path.insert(0, str(lab_02_01_path))
sys.path.insert(0, str(lab_02_02_path))
sys.path.insert(0, str(lab_02_03_path))

# Импорт существующих классов (без дублирования кода)
from model import Student
from base import BachelorStudent, MasterStudent

# Импорт из текущей лабораторной работы
from container import (
    Displayable, Scorable, TypedCollection,
    D, S, T, R
)


def print_header(title: str, char: str = "=", length: int = 80) -> None:
    """Вывод заголовка с разделителем"""
    print(f"\n{char * length}")
    print(f"📌 {title}")
    print(f"{char * length}")


def print_subheader(title: str) -> None:
    """Вывод подзаголовка"""
    print(f"\n--- {title} ---")


def main() -> None:
    print_header("ЛАБОРАТОРНАЯ РАБОТА №6: PROTOCOLS И GENERIC-КОЛЛЕКЦИИ", "=")

    # ================================================================
    # ЧАСТЬ 1: Демонстрация работы Protocols без явного наследования
    # ================================================================
    print_header("ЧАСТЬ 1: ПРОВЕРКА ПРОТОКОЛОВ (структурная типизация)", "-")

    print_subheader("Создание объектов разных типов из иерархии ЛР-3")

    # Создаём обычного студента
    ordinary = Student(
        fio="Смирнов Алексей Владимирович",
        birthdate="2005-05-10",
        group="Бивт-25-6",
        gpa=4.2
    )

    # Создаём бакалавра
    bachelor = BachelorStudent(
        fio="Иванова Анна Сергеевна",
        birthdate="2004-08-15",
        group="Бивт-25-1",
        gpa=4.7,
        specialization="Прикладная математика",
        has_thesis=False
    )

    # Создаём магистра
    master = MasterStudent(
        fio="Петров Дмитрий Алексеевич",
        birthdate="2002-03-20",
        group="Бивт-25-2",
        gpa=4.9,
        research_area="Машинное обучение",
        supervisor="Проф. Соколов И.И."
    )

    # Магистр публикует статью
    master.publish_paper("NeurIPS 2025")

    print(f"   ✅ Создан Student: {ordinary.fio}")
    print(f"   ✅ Создан BachelorStudent: {bachelor.fio}")
    print(f"   ✅ Создан MasterStudent: {master.fio}")

    # ================================================================
    # ЧАСТЬ 2: Демонстрация Displayable Protocol
    # ================================================================
    print_header("ЧАСТЬ 2: ДЕМОНСТРАЦИЯ Displayable PROTOCOL", "-")

    # Добавляем метод display() в классы (если его нет)
    # Метод добавляется прямо в классы через monkey patching для демонстрации
    # В реальном коде методы должны быть определены в классах заранее

    def student_display(self) -> str:
        return f"👨‍🎓 {self.fio} | Группа: {self.group} | GPA: {self.gpa} | {self.status.value}"

    def bachelor_display(self) -> str:
        thesis_status = "✅ Диплом защищён" if self.has_thesis else "📝 Диплом не защищён"
        return f"🎓 {self.fio} (бакалавр) | Спец: {self.specialization} | {thesis_status} | GPA: {self.gpa}"

    def master_display(self) -> str:
        return f"🔬 {self.fio} (магистр) | Исслед: {self.research_area} | Публикаций: {self.papers_count} | GPA: {self.gpa}"

    # Добавляем методы в классы (для демонстрации)
    Student.display = student_display
    BachelorStudent.display = bachelor_display
    MasterStudent.display = master_display

    print_subheader("Типизированная коллекция Displayable объектов (TypedCollection[D])")

    # Создаём коллекцию, которая принимает только Displayable объекты
    displayable_collection: TypedCollection[Displayable] = TypedCollection[Displayable]()

    displayable_collection.add(ordinary)
    displayable_collection.add(bachelor)
    displayable_collection.add(master)

    print(f"   Коллекция содержит {len(displayable_collection)} объектов")
    print("\n   Вызов метода display() для каждого объекта:")
    for i, obj in enumerate(displayable_collection, 1):
        print(f"      {i}. {obj.display()}")

    # ================================================================
    # ЧАСТЬ 3: Демонстрация Scorable Protocol
    # ================================================================
    print_header("ЧАСТЬ 3: ДЕМОНСТРАЦИЯ Scorable PROTOCOL", "-")

    # Добавляем метод score() в классы
    def student_score(self) -> float:
        return self.gpa

    def bachelor_score(self) -> float:
        # Бакалавр получает бонус за диплом
        base = self.gpa
        if self.has_thesis:
            return base + 0.5
        return base

    def master_score(self) -> float:
        # Магистр получает бонус за публикации
        base = self.gpa
        return base + self.papers_count * 0.3

    Student.score = student_score
    BachelorStudent.score = bachelor_score
    MasterStudent.score = master_score

    print_subheader("Типизированная коллекция Scorable объектов (TypedCollection[S])")

    # Создаём коллекцию, которая принимает только Scorable объекты
    scorable_collection: TypedCollection[Scorable] = TypedCollection[Scorable]()

    scorable_collection.add(ordinary)
    scorable_collection.add(bachelor)
    scorable_collection.add(master)

    print(f"   Коллекция содержит {len(scorable_collection)} объектов")
    print("\n   Вызов метода score() для каждого объекта:")
    for i, obj in enumerate(scorable_collection, 1):
        print(f"      {i}. {type(obj).__name__}: {obj.fio} → score = {obj.score():.2f}")

    # Суммируем все очки
    total_score = sum(obj.score() for obj in scorable_collection)
    print(f"\n   Суммарный score всех объектов: {total_score:.2f}")

    # ================================================================
    # ЧАСТЬ 4: Демонстрация методов find, filter, map
    # ================================================================
    print_header("ЧАСТЬ 4: МЕТОДЫ find(), filter(), map()", "-")

    # Создаём обычную TypedCollection (без bound) для студентов
    student_collection: TypedCollection[Student] = TypedCollection[Student]()

    # Добавляем больше студентов для демонстрации
    students = [
        Student("Иванов Иван Иванович", "2005-05-10", "Бивт-26-1", 4.5),
        Student("Петрова Анна Сергеевна", "2005-08-15", "Бивт-25-1", 4.8),
        Student("Сидоров Алексей Владимирович", "2005-03-20", "Бивт-24-1", 3.9),
        Student("Козлова Екатерина Дмитриевна", "2004-12-25", "Бивт-25-1", 4.9),
        Student("Смирнов Дмитрий Алексеевич", "2005-07-05", "Бивт-24-1", 2.8),
        Student("Волкова Мария Игоревна", "2005-11-30", "Бивт-26-1", 4.2),
        Student("Морозов Артем Сергеевич", "2004-03-18", "Бивт-24-1", 3.5),
    ]

    for s in students:
        student_collection.add(s)

    print(f"   Создана коллекция из {len(student_collection)} студентов")

    # 4.1 Демонстрация find()
    print_subheader("Метод find() – поиск первого подходящего элемента")

    # Поиск существующего элемента
    found = student_collection.find(lambda s: s.gpa >= 4.8)
    if found:
        print(f"   ✅ Найден студент с GPA >= 4.8: {found.fio} (GPA: {found.gpa})")

    # Поиск существующего элемента по группе
    found = student_collection.find(lambda s: s.group == "ФИ-24")
    if found:
        print(f"   ✅ Найден студент из группы ФИ-24: {found.fio}")

    # Поиск несуществующего элемента
    not_found = student_collection.find(lambda s: s.gpa >= 5.0)
    if not_found is None:
        print(f"   ❌ Студент с GPA >= 5.0 не найден (вернулся None)")

    # 4.2 Демонстрация filter()
    print_subheader("Метод filter() – фильтрация списка")

    # Фильтр: студенты с высоким GPA
    high_gpa = student_collection.filter(lambda s: s.gpa >= 4.5)
    print(f"   Студенты с GPA >= 4.5: {len(high_gpa)} человек")
    for s in high_gpa:
        print(f"      - {s.fio} (GPA: {s.gpa})")

    # Фильтр: студенты конкретной группы
    group_23 = student_collection.filter(lambda s: s.group == "ФИ-23")
    print(f"\n   Студенты группы ФИ-23: {len(group_23)} человек")
    for s in group_23:
        print(f"      - {s.fio}")

    # 4.3 Демонстрация map() – изменение типа результата
    print_subheader("Метод map() – преобразование с изменением типа (TypeVar R)")

    # map: Student → str (ФИО)
    names: list[str] = student_collection.map(lambda s: s.fio)
    print(f"   map(Student → str) – список ФИО ({len(names)} элементов):")
    for i, name in enumerate(names[:5], 1):
        print(f"      {i}. {name}")
    if len(names) > 5:
        print(f"      ... и ещё {len(names) - 5} студентов")

    # map: Student → float (GPA)
    gpas: list[float] = student_collection.map(lambda s: s.gpa)
    print(f"\n   map(Student → float) – список GPA:")
    for i, gpa in enumerate(gpas, 1):
        print(f"      {i}. {gpa}")

    # map: Student → str (описание)
    descriptions: list[str] = student_collection.map(lambda s: f"{s.fio} [{s.group}]")
    print(f"\n   map(Student → str) – описания:")
    for desc in descriptions[:3]:
        print(f"      - {desc}")

    # map: Student → int (возраст)
    ages: list[int] = student_collection.map(lambda s: s.get_age())
    print(f"\n   map(Student → int) – список возрастов:")
    for i, age in enumerate(ages, 1):
        print(f"      {i}. {age} лет")

    # Демонстрация цепочки filter + map
    print_subheader("Цепочка методов: filter() + map()")

    # Получаем имена отличников
    excellent_names: list[str] = (
        student_collection
        .filter(lambda s: s.gpa >= 4.5)
        .map(lambda s: s.fio)
    )
    print(f"   Имена отличников (GPA >= 4.5):")
    for name in excellent_names:
        print(f"      - {name}")

    # ================================================================
    # ЧАСТЬ 5: Демонстрация типобезопасности (ошибки при несоответствии)
    # ================================================================
    print_header("ЧАСТЬ 5: ТИПОБЕЗОПАСНОСТЬ (ошибки при несоответствии)", "-")

    print("   Попытка добавить объект без метода display() в TypedCollection[Displayable]:")

    # Создаём класс без метода display
    class WithoutDisplay:
        def __init__(self, name: str):
            self.name = name

    obj_without_display = WithoutDisplay("Тестовый объект")

    try:
        # Это вызовет ошибку типов в mypy, но во время выполнения пройдёт
        # В production коде нужна runtime проверка
        displayable_collection.add(obj_without_display)  # type: ignore
        print("   ⚠️ Объект добавлен, но при вызове display() будет ошибка")
    except AttributeError as e:
        print(f"   ❌ Ошибка при вызове display(): {e}")

    print("\n   ✅ Типобезопасность на уровне статического анализа (mypy)")
    print("   ✅ Runtime проверку можно добавить через hasattr() в методе add()")

    # ================================================================
    # ЧАСТЬ 6: Демонстрация работы Generic с разными типами
    # ================================================================
    print_header("ЧАСТЬ 6: GENERIC – РАБОТА С РАЗНЫМИ ТИПАМИ", "-")

    # Коллекция строк
    string_collection: TypedCollection[str] = TypedCollection[str]()
    string_collection.add("Первый")
    string_collection.add("Второй")
    string_collection.add("Третий")

    print(f"   TypedCollection[str]: {len(string_collection)} элементов")
    print(f"   Содержимое: {', '.join(string_collection.get_all())}")

    # Коллекция чисел
    int_collection: TypedCollection[int] = TypedCollection[int]()
    for i in range(1, 6):
        int_collection.add(i)

    # map для чисел: int → int (квадрат)
    squares: list[int] = int_collection.map(lambda x: x ** 2)
    print(f"\n   TypedCollection[int]: исходные числа: {int_collection.get_all()}")
    print(f"   map(квадрат): {squares}")

    # filter для чисел
    even_numbers: list[int] = int_collection.filter(lambda x: x % 2 == 0)
    print(f"   filter(чётные): {even_numbers}")

    # ================================================================
    # ИТОГ
    # ================================================================
    print_header("ИТОГИ ЛАБОРАТОРНОЙ РАБОТЫ №6", "=")



if __name__ == "__main__":
    main()