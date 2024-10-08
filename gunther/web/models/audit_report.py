from gunther.core import AuditFinding
from gunther.web.core import BaseDBModel, BaseDTOModel
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from gunther.web.models.audit_finding import GetAuditFinding

class AuditReport(BaseDBModel):
    __tablename__ = "audit_reports"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    address = Column(String)
    conclusion = Column(Text, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    findings = relationship("AuditFinding")


class CreateAuditReport(BaseDTOModel):
    title: str
    address: str

class UpdateAuditReport(BaseDTOModel):
    title: str
    conclusion: str

class GetAuditReport(BaseDTOModel):
    id: int
    title: str
    address: str
    conclusion: str
    created: datetime
    updated: datetime

class DetailedAuditReport(GetAuditReport):
    findings: list[GetAuditFinding]

