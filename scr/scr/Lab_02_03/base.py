# inherited.py
from model import Student


class BachelorStudent(Student):
    """Студент-бакалавр"""

    def __init__(self, fio: str, birthdate: str, group: str, gpa: float,
                 specialization: str, has_thesis: bool = False):
        super().__init__(fio, birthdate, group, gpa)
        self.specialization = specialization
        self.has_thesis = has_thesis

    # Переопределение полиморфного метода
    def get_scholarship_amount(self) -> int:
        base = super().get_scholarship_amount()
        if self.has_thesis:
            return base + 500   # надбавка за защиту диплома
        return base

    # Новый метод
    def defend_thesis(self) -> str:
        if self.has_thesis:
            return f"{self.fio} уже защитил(а) диплом по {self.specialization}"
        self.has_thesis = True
        return f"{self.fio} защитил(а) диплом по {self.specialization}"

    # Переопределение __str__
    def __str__(self) -> str:
        base = super().__str__()
        thesis_status = "Диплом защищён" if self.has_thesis else "Диплом не защищён"
        return base + f"\n│ 🎓 Специализация: {self.specialization}\n│ 📜 {thesis_status}"


class MasterStudent(Student):
    """Студент-магистр"""

    def __init__(self, fio: str, birthdate: str, group: str, gpa: float,
                 research_area: str, supervisor: str):
        super().__init__(fio, birthdate, group, gpa)
        self.research_area = research_area
        self.supervisor = supervisor
        self.papers_count = 0

    # Переопределение полиморфного метода
    def get_scholarship_amount(self) -> int:
        base = super().get_scholarship_amount()
        return base + self.papers_count * 300   # надбавка за публикации

    # Новый метод
    def publish_paper(self, conference: str) -> str:
        self.papers_count += 1
        return f"{self.fio} опубликовал(а) статью в '{conference}' (всего: {self.papers_count})"

    # Переопределение __str__
    def __str__(self) -> str:
        base = super().__str__()
        return (base +
                f"\n│  Область исследований: {self.research_area}"
                f"\n│  Научный руководитель: {self.supervisor}"
                f"\n│  Публикаций: {self.papers_count}")