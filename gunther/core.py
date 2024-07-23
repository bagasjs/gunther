from __future__ import annotations
from typing import List, Dict
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timezone

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
                 severity: FindingSeverity,
                 raw: str = "",
                 description: str = "",
                 recommendation: str = "",
                 ):
        self.title = title
        self.description = description
        self.severity = severity
        self.recommendation = recommendation
        self.raw = raw

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "severity": str(self.severity),
            "raw": self.raw,
            "description": self.description,
            "recommendation": self.recommendation,
        }

class Analyzer(ABC):
    findings: List[AuditFinding]

    @abstractmethod
    def analyze(self, input: str):
        pass

# Find if this useful
class DescribedAuditFinding(object):
    def __init__(self, title: str, raw: str, severity: FindingSeverity, description: str, recommendation: str):
        self.title = title
        self.raw = raw
        self.severity = severity
        self.description = description
        self.recommendation = recommendation

class Writer(ABC):
    @abstractmethod
    def describe_audit_finding(self, finding: AuditFinding) -> str:
        pass

    @abstractmethod
    def describe_finding(self, finding: AuditFinding) -> DescribedAuditFinding:
        pass

    @abstractmethod
    def execute_prompt(self, prompt: str) -> str:
        pass

    @abstractmethod
    def make_audit_result_conclusion(self, result: AuditResult) -> str:
        pass

class AuditResult(object):
    _findings_amount: int
    _findings_categories_count: Dict[FindingSeverity, int]
    _findings_changed: bool

    findings: List[AuditFinding]
    unix_timestamp: int
    context: str
    context_is_address: bool

    def __init__(self, context: str, context_is_address: bool, findings: List[AuditFinding]):
        self.findings = findings
        self.context = context
        self.context_is_address = context_is_address

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

    def set_timestamp_as_now(self):
        self.unix_timestamp = int(datetime(1970,1,1,1,0,tzinfo=timezone.utc).timestamp())

    def to_dict(self) -> dict:
        findings = []
        for finding in self.findings:
            findings.append(finding.to_dict())
        data = { "findings": findings, }
        return data
