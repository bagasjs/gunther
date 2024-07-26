from abc import ABC, abstractmethod

class Writer(ABC):
    @abstractmethod
    def describe_audit_finding(self, finding) -> str:
        pass

    @abstractmethod
    def describe_finding(self, finding):
        pass

    @abstractmethod
    def execute_prompt(self, prompt: str) -> str:
        pass

    @abstractmethod
    def make_audit_result_conclusion(self, result) -> str:
        pass
