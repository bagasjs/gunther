from gunther.core import AuditReport
from abc import ABC, abstractmethod

class Writer(ABC):
    @abstractmethod
    def make_description_from_raw_finding(self, raw_finding: str) -> str:
        pass

    @abstractmethod
    def make_recommendation_from_raw_finding(self, raw_finding: str) -> str:
        pass

    @abstractmethod
    def infer_title_from_raw_finding(self, raw_finding: str) -> str:
        pass

    @abstractmethod
    def make_audit_report_conclusion(self, report: AuditReport) -> str:
        pass

    @abstractmethod
    def execute_prompt(self, prompt: str) -> str:
        pass
