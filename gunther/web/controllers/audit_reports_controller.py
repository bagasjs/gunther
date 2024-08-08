from fastapi import APIRouter, Query, HTTPException, Path, status
from gunther.web.core import gunther_sessionmaker
from gunther.web.models.audit_report import AuditReport, DetailedAuditReport, GetAuditReport, CreateAuditReport
from sqlalchemy import select, orm
from datetime import datetime

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
)

@router.get("/", response_model=list[GetAuditReport])
async def get_all(limit: int = Query(1000, gt=0), offset: int = Query(0, ge=0)) -> list[AuditReport]:
    with gunther_sessionmaker() as session:
        return session.query(AuditReport).limit(limit).offset(offset).all()

@router.get("/{id}", response_model=DetailedAuditReport)
async def get_by_id(id: int = Path(ge=1)) -> AuditReport | None:
    with gunther_sessionmaker() as session:
        report = session.query(AuditReport).where(AuditReport.id == id).options(orm.joinedload(AuditReport.findings)).first()
        if not report:
            raise HTTPException(status_code=404, detail="Requested audit report is not found")
        return report 

@router.get("/{address}", response_model=GetAuditReport)
async def get_by_address(address: str) -> list[AuditReport]:
    with gunther_sessionmaker() as session:
        return session.query(AuditReport).where(AuditReport.address == address).all()

@router.put("/{id}", response_model=GetAuditReport)
async def update(id: int = Path(ge=1)) -> AuditReport | None:
    with gunther_sessionmaker() as session:
        stmt = select(AuditReport).where(AuditReport.id == id).limit(1)
        report = session.execute(stmt).scalars().one_or_none()
        if not report :
            raise HTTPException(status_code=404, detail="Requested audit report is not found")
        # report.updated = datetime.now()
        return report
