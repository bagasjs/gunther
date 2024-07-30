from abc import ABC, abstractmethod
from typing import List
from enum import Enum

class FindingSeverity(Enum):
    Unknown = "Unknown"
    Note    = "Note"
    Low     = "Low"
    Medium  = "Medium"
    High    = "High"

class AnalysisResult(object):
    def __init__(self, title: str, severity: FindingSeverity, raw: str):
        self.title = title
        self.severity = severity
        self.raw = raw


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, input: str):
        pass

    @abstractmethod
    def get_results(self) -> List[AnalysisResult]:
        pass

