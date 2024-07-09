from typing import List, Dict
from abc import ABC, abstractmethod
from enum import Enum
import json

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
    def describe(self, finding: AuditFinding) -> str:
        pass

class AuditReport(object):
    def __init__(self, 
                 title: str,
                 description: str,
                 findings: List[AuditFinding]):
        self.title = title
        self.description = description
        self.findings = findings

    def to_html(self) -> str:
        result = ''
        result += f'<center><h1>{self.title}</h1></center>'
        result +=  '<ol type="A">'
        result += f'    <li>\n<h2>Description</h2>\n<p>{self.description}</p>\n</li>\n'
        result +=  '    <li>\n<h2>Audit Findings</h2>\n'
        result +=  '        <ol type="1">\n'

        for finding in self.findings:
            result +=  '            <li>\n'
            result += f'            <h3>{finding.title}</h3>\n'
            result +=  '            <ol type="a">\n'
            result += f'                <li><h4>Severity: {finding.severity.value}</h4></li>\n'
            result += f'                <li><h4>Description</h4><p>{finding.description}</p></li>\n'
            result +=  '            </ol>\n'
            result +=  '            </li>\n'


        result += "\n</ol>\n</li>\n"
        result += "</ol>\n"
        return result

    def to_dict(self) -> dict:
        findings = []
        for finding in self.findings:
            findings.append(finding.to_dict())
        data = {
            "title": self.title,
            "description": self.description,
            "findings": findings,
        }
        return data        
