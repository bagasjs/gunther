from fastapi import APIRouter, Query, Path, HTTPException
from gunther.web.core import gunther_sessionmaker
from gunther.web.models.audit_finding import AuditFinding, GetAuditFinding

router = APIRouter(
    prefix="/api/findings",
    tags=["findings"],
)

@router.get("/", response_model=GetAuditFinding)
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
async def update(id: int = Path(ge=1)) -> AuditFinding | None:
    pass

@router.put("/{id}/generate-better-description", response_model=GetAuditFinding)
async def generate_better_description(id: int = Path(ge=1)) -> AuditFinding | None:
    pass

@router.put("/{id}/generate-better-description", response_model=GetAuditFinding)
async def generate_better_recommendation(id: int = Path(ge=1)) -> AuditFinding | None:
    pass
