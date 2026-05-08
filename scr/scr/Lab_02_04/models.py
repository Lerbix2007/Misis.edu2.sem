import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

lab_02_02_path = project_root / "Lab_02_02"
lab_03_path = project_root / "Lab_02_03"

sys.path.insert(0, str(lab_02_02_path))

from collection import StudentCollection
from model import Student

# Потом добавляем Lab_03 для base.py
sys.path.insert(0, str(lab_03_path))

from base import BachelorStudent, MasterStudent

from interfaces import Printable, Comparable, ScholarshipInfo


class ContractStudent(Student, Printable, Comparable, ScholarshipInfo):
    def get_scholarship_amount(self) -> int:
        if self.gpa >= 4.5:
            return 2000
        elif self.gpa >= 4.0:
            return 1500
        elif self.gpa >= 3.0:
            return 1000
        return 0

    def to_string(self) -> str:
        return f"Студент: {self.fio}, группа: {self.group}, GPA: {self.gpa}"

    def get_compare_value(self) -> float:
        return self.gpa

    def scholarship_info(self) -> str:
        return f"{self.fio}: стипендия {self.get_scholarship_amount()} руб."

    def scholarship_info(self) -> str:
        return f"{self.fio}: стипендия {self.get_scholarship_amount()} руб."


class ContractBachelorStudent(BachelorStudent, Printable, Comparable, ScholarshipInfo):
    def get_scholarship_amount(self) -> int:
        if self.gpa >= 4.5:
            base = 2000
        elif self.gpa >= 4.0:
            base = 1500
        elif self.gpa >= 3.0:
            base = 1000
        else:
            base = 0

        if self.has_thesis:
            return base + 500
        return base

    def to_string(self) -> str:
        thesis = "диплом защищён" if self.has_thesis else "диплом не защищён"
        return f"Бакалавр: {self.fio}, специализация: {self.specialization}, {thesis}, GPA: {self.gpa}"

    def get_compare_value(self) -> float:
        bonus = 0.2 if self.has_thesis else 0
        return self.gpa + bonus

    def scholarship_info(self) -> str:
        return f"{self.fio}: стипендия бакалавра {self.get_scholarship_amount()} руб."


class ContractMasterStudent(MasterStudent, Printable, Comparable, ScholarshipInfo):
    def get_scholarship_amount(self) -> int:
        if self.gpa >= 4.5:
            base = 2000
        elif self.gpa >= 4.0:
            base = 1500
        elif self.gpa >= 3.0:
            base = 1000
        else:
            base = 0

        return base + self.papers_count * 300

    def to_string(self) -> str:
        return f"Магистр: {self.fio}, область: {self.research_area}, публикаций: {self.papers_count}, GPA: {self.gpa}"

    def get_compare_value(self) -> float:
        return self.gpa + self.papers_count * 0.3

    def scholarship_info(self) -> str:
        return f"{self.fio}: стипендия магистра {self.get_scholarship_amount()} руб."


class InterfaceStudentCollection(StudentCollection):
    def filter_by_interface(self, interface_type):
        filtered = [
            item for item in self.get_all()
            if isinstance(item, interface_type)
        ]
        return InterfaceStudentCollection(filtered)

    def get_printable(self):
        return self.filter_by_interface(Printable)

    def get_comparable(self):
        return self.filter_by_interface(Comparable)

    def get_scholarship_items(self):
        return self.filter_by_interface(ScholarshipInfo)

    def sort_by_compare_value(self, reverse: bool = True):
        sorted_items = sorted(
            self.get_comparable().get_all(),
            key=lambda item: item.get_compare_value(),
            reverse=reverse
        )
        return InterfaceStudentCollection(sorted_items)