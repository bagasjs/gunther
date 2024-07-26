from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List

class Severity(Enum):
    Unknown = "Unknown"
    Note    = "Note"
    Low     = "Low"
    Medium  = "Medium"
    High    = "High"

class AnalysisResultItem(object):
    title: str
    description: str
    severity: Severity

    def __init__(self,
                 title: str,
                 severity: Severity,
                 description: str,
                 ):
        self.title = title
        self.description = description
        self.severity = severity

    def to_dict(self):
        return {
            "title": self.title,
            "severity": str(self.severity),
            "description": self.description,
        }

class AnalysisResult(object):
    _items: List[AnalysisResultItem]
    _items_amount: int
    # _items_by_severity_count: Dict[Severity, int]

    def __init__(self):
        self._items = []
        self._items_amount = 0

        # self._items_by_severity_count = {}
        # self._items_by_severity_count[Severity.Note] = 0
        # self._items_by_severity_count[Severity.Low] = 0
        # self._items_by_severity_count[Severity.Medium] = 0
        # self._items_by_severity_count[Severity.High] = 0

    def items(self) -> List[AnalysisResultItem]:
        return self._items

    def get_items_amount(self) -> int:
        return self._items_amount

    def add_item(self, item: AnalysisResultItem):
        self._items_amount += 1
        self._items.append(item)

    def add_from_other_analysis(self, other: AnalysisResult):
        for item in other.items():
            self.add_item(item)

    def to_dict(self) -> dict:
        items = []
        for item in self._items:
            items.append(item.to_dict())
        data = { "items": items, }
        return data

class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, input: str):
        pass

    @abstractmethod
    def get_result(self) -> AnalysisResult:
        pass
