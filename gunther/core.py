from __future__ import annotations
from typing import List, Dict
from abc import ABC, abstractmethod
from enum import Enum

class AuditError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

class FindingSeverity(Enum):
    Unknown = "Unknown"
    Note    = "Note"
    Low     = "Low"
    Medium  = "Medium"
    High    = "High"

class AuditFinding(object):
    def __init__(self,
                 title: str,
                 auditor: str,
                 severity: FindingSeverity,
                 raw: str = "",
                 description: str = "",
                 recommendation: str = "",
                 ):
        self.title = title
        self.auditor = auditor
        self.description = description
        self.severity = severity
        self.recommendation = recommendation
        self.raw = raw

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "auditor": self.auditor,
            "description": self.description,
            "raw": self.raw,
            "severity": str(self.severity),
            "recommendation": self.recommendation,
        }

class Auditor(ABC):
    findings: List[AuditFinding]

    @abstractmethod
    def perform_audit(self, input: str):
        pass

class Writer(ABC):
    @abstractmethod
    def extract_title(self, result: AuditResult) -> str:
        pass

    @abstractmethod
    def describe_audit_finding(self, finding: AuditFinding) -> str:
        pass

    @abstractmethod
    def make_audit_result_conclusion(self, result: AuditResult) -> str:
        pass

class AuditResult(object):
    _findings_amount: int
    _findings_categories_count: Dict[FindingSeverity, int]
    _findings_changed: bool

    findings: List[AuditFinding]

    def __init__(self, findings: List[AuditFinding]):
        self.findings = findings

        self._findings_amount = len(self.findings)
        self._findings_categories_count = {}
        self._findings_categories_count[FindingSeverity.Note] = 0
        self._findings_categories_count[FindingSeverity.Low] = 0
        self._findings_categories_count[FindingSeverity.Medium] = 0
        self._findings_categories_count[FindingSeverity.High] = 0
        self._findings_changed = True

    def add_finding(self, finding: AuditFinding):
        self._findings_amount += 1
        self._findings_changed = True
        self.findings.append(finding)

    def get_findings_amount(self) -> int:
        return self._findings_amount

    def get_finding_categories_count(self) -> Dict[FindingSeverity, int]:
        if self._findings_changed:
            for finding in self.findings:
                self._findings_categories_count[finding.severity] += 1
        return self._findings_categories_count

    def to_dict(self) -> dict:
        findings = []
        for finding in self.findings:
            findings.append(finding.to_dict())
        data = { "findings": findings, }
        return data
