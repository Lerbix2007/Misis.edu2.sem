from abc import ABC, abstractmethod


class Printable(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass


class Comparable(ABC):
    @abstractmethod
    def get_compare_value(self) -> float:
        pass


class ScholarshipInfo(ABC):
    @abstractmethod
    def scholarship_info(self) -> str:
        pass