from fastapi import APIRouter, Query, Path, HTTPException
from gunther.web.core import gunther_sessionmaker
from gunther.web.models.audit_finding import AuditFinding, GetAuditFinding, UpdateAuditFinding

from datetime import datetime
from sqlalchemy import select, orm

from gunther.writers.gemini_writer import GeminiWriter

router = APIRouter(
    prefix="/api/findings",
    tags=["findings"],
)

@router.get("/", response_model=list[GetAuditFinding])
async def get_all(limit: int = Query(1000, gt=0), offset: int = Query(0, ge=0)) -> list[AuditFinding]:
    with gunther_sessionmaker() as session:
        return session.query(AuditFinding).limit(limit).offset(offset).all()

@router.get("/{id}", response_model=GetAuditFinding)
async def get_by_id(id: int = Path(ge=1)) -> AuditFinding | None:
    with gunther_sessionmaker() as session:
        user = session.query(AuditFinding).where(
                AuditFinding.id == id
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="Requested audit finding is not found")
        return user

@router.put("/{id}", response_model=GetAuditFinding)
async def update(finding: UpdateAuditFinding, id: int = Path(ge=1)) -> AuditFinding | None:
    with gunther_sessionmaker() as session:
        stmt = select(AuditFinding).where(AuditFinding.id == id).limit(1)
        report = session.execute(stmt).scalars().one_or_none()
        if not report :
            raise HTTPException(status_code=404, detail="Requested audit report is not found")
        report.description = finding.description
        report.recommendation = finding.recommendation
        report.updated = datetime.now()
        session.commit()
        session.refresh(report)
        return report


# TODO(bagasjs) Change the name into paraphrase since the description and recommendation could be None
@router.put("/{id}/generate-description-automatically", response_model=GetAuditFinding)
async def generate_description_automatically(id: int = Path(ge=1)) -> AuditFinding | None:
    with gunther_sessionmaker() as session:
        stmt = select(AuditFinding).where(AuditFinding.id == id).limit(1)
        report = session.execute(stmt).scalars().one_or_none()
        if not report :
            raise HTTPException(status_code=404, detail="Requested audit report is not found")
        report.description = GeminiWriter().make_description_from_raw_finding(report.raw)
        report.updated = datetime.now()
        session.commit()
        session.refresh(report)
        return report

@router.put("/{id}/generate-recommendation-automatically", response_model=GetAuditFinding)
async def generate_recommendation_automatically(id: int = Path(ge=1)) -> AuditFinding | None:
    with gunther_sessionmaker() as session:
        stmt = select(AuditFinding).where(AuditFinding.id == id).limit(1)
        report = session.execute(stmt).scalars().one_or_none()
        if not report :
            raise HTTPException(status_code=404, detail="Requested audit report is not found")
        report.recommendation = GeminiWriter().make_recommendation_from_raw_finding(report.raw)
        report.updated = datetime.now()
        session.commit()
        session.refresh(report)
        return report
