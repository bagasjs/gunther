from fastapi import APIRouter, Request, Query, HTTPException, Path
from gunther.web.core import gunther_sessionmaker, templates
from gunther.web.models.audit_report import AuditReport
from sqlalchemy import select, orm

router = APIRouter(
    prefix="/reports",
    tags=["others-api-route"],
)

@router.get("/")
async def all(request: Request, limit: int = Query(1000, gt=0), offset: int = Query(0, ge=0)):
    with gunther_sessionmaker() as session:
        reports = session.query(AuditReport).limit(limit).offset(offset).all()
        return templates.TemplateResponse(
                request=request,
                name="report_list.html",
                context={
                    "reports": reports,
                })

@router.get("/{id}/edit")
async def edit(request: Request, id: int = Path(ge=1)):
    with gunther_sessionmaker() as session:
        report = (session
                  .query(AuditReport)
                  .where(AuditReport.id == id)
                  .options(orm.joinedload(AuditReport.findings))
                  .first())
        if report is None:
            raise HTTPException(status_code=404, detail=f"Not found report with id {id}")
        return templates.TemplateResponse(
                request=request,
                name="report_editor.html",
                context={
                    "report": report,
                })



@router.get("/{id}")
async def find(request: Request, id: int = Path(ge=1)):
    with gunther_sessionmaker() as session:
        report = (session
                  .query(AuditReport)
                  .where(AuditReport.id == id)
                  .options(orm.joinedload(AuditReport.findings))
                  .first())

        finding_per_severity_categorization = {}
        if report:
            for finding in report.findings:
                if finding.severity not in finding_per_severity_categorization.keys():
                    finding_per_severity_categorization[finding.severity] = 1
                else:
                    finding_per_severity_categorization[finding.severity] += 1

        return templates.TemplateResponse(
                request=request,
                name="report_detail.html",
                context={
                    "report": report,
                    "finding_per_severity_categorization": finding_per_severity_categorization,
                })

