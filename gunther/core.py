from __future__ import annotations
from typing import List, Dict
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

class AuditError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

class Model(DeclarativeBase):
    pass

class AuditFinding(Model):
    __tablename__ = "audit_findings"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    severity = Column(String)
    raw = Column(Text)
    description = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    report_id = Column(Integer, ForeignKey("audit_reports.id"), nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "title": self.title,
            "severity": str(self.severity),
            "raw": self.raw,
            "description": self.description,
            "recommendation": self.recommendation,
        }

class AuditReport(Model):
    __tablename__ = "audit_reports"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    address = Column(String)
    conclusion = Column(Text, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    findings = relationship("AuditFinding")

    def to_dict(self):
        findings = []
        for finding in self.findings:
            findings.append(finding.to_dict())
        return {
            "findings": findings,
            "conclusion": self.conclusion,
        }

