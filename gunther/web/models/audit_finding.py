from gunther.web.core import BaseDBModel, BaseDTOModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

class AuditFinding(BaseDBModel):
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

class GetAuditFinding(BaseDTOModel):
    id: int
    title: str
    severity: str
    raw: str
    description: str | None
    recommendation: str
    report_id: int
    created: datetime | None
    updated: datetime | None


