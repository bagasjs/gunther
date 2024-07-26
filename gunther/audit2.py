from __future__ import annotations
import os
import sys
from gunther.analyzers.core import AnalysisResult, AnalysisResultItem
from gunther.utils import Etherscan
from gunther.analyzers import list_of_analyzers

# Auditor class imports
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

# Model related imports
from sqlalchemy import create_engine, Engine, Column, Integer, String, Text, ForeignKey, DateTime
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
    type = Column(String)
    raw = Column(Text)
    description = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    result_id = Column(Integer, ForeignKey("audit_results.id"))

    result = relationship("AuditResult", back_populates="findings")

class AuditResult(Model):
    __tablename__ = "audit_results"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    address = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    findings = relationship("AuditFinding", order_by=AuditFinding.id, back_populates="result")


class Auditor(object):
    _engine: Engine
    _session: Session
    _sessionmaker: sessionmaker
    _etherscan: Etherscan

    def __init__(self):
        self._engine = create_engine("sqlite:///database.sqlite")
        self._sessionmaker= sessionmaker()
        self._sessionmaker.configure(bind=self._engine)
        self._session = self._sessionmaker()
        self._etherscan = Etherscan(os.environ["ETHERSCAN_API_KEY"]) 

    def analyze_smart_contract_in_network(self, network: str, address: str) -> AnalysisResult:
        if not self._etherscan.validate_address(network, address):
            print(f"ERROR: Invalid address or network {network}:{address}", file=sys.stderr)

        result = AnalysisResult()
        for name, analyzer in list_of_analyzers.items():
            print(f"INFO: Running `{name}` analyzer")
            try:
                analyzer.analyze(address)
                result.add_from_other_analysis(analyzer.get_result())
            except AuditError as e:
                print(f"ERROR: {e}")
        return result

    def generate_audit_result_from_analysis(self, analysis: AnalysisResult) -> AuditResult:
        pass

    def create_audit_finding_from_analysis(self, analysis_item: AnalysisResultItem) -> AuditFinding:
        pass

    def __enter__(self) -> Auditor:
        return self

    def __exit__(self, *_):
        pass

