from fastapi import APIRouter, Query, HTTPException, status
from sqlalchemy import select, orm
from datetime import datetime, timedelta

from gunther.core import AuditError
from gunther.analyzers import list_of_analyzers
from gunther.web.core import gunther_sessionmaker
from gunther.web.models.audit_report import AuditReport, CreateAuditReport, GetAuditReport
from gunther.web.models.audit_finding import AuditFinding

router = APIRouter(
    prefix="/api",
    tags=["others-api-route"],
)

AMOUNT_OF_RETRIES = 3

@router.post("/audit", status_code=status.HTTP_201_CREATED, response_model=GetAuditReport)
async def audit(dto: CreateAuditReport) -> AuditReport | None:
    title = dto.title
    address = dto.address
    with gunther_sessionmaker() as session:
        stmt = select(AuditReport).where(AuditReport.address == address).limit(1)
        report = session.execute(stmt).scalars().one_or_none()
        if report is None:
            print(f"INFO: There's no audit reports with address `{address}`")
            report = AuditReport(title=title, address=address, conclusion="")
            session.add(report)
        else:
            print(f"INFO: There's already an audit report for `{address}`")
            required_time_range_to_change = (datetime.now() - timedelta(weeks=1)) # should be 1 week
            if report.updated > required_time_range_to_change:
                print(f"INFO: The report `{address}` is already recent")
                return report
            else:
                report.findings.clear() # Remove the old findings
        session.commit()
        session.refresh(report)

        for name, analyzer in list_of_analyzers.items():
            print(f"INFO: Running `{name}` analyzer")
            try:
                analyzer.analyze(address)
                for item in analyzer.get_results():
                    session.add(AuditFinding(
                        title = item.title,
                        severity = item.severity.value,
                        raw = item.raw,
                        description = item.raw,
                        recommendation = None,
                        report_id = report.id,
                        ))
            except AuditError as e:
                raise HTTPException(status_code=400, detail=f"Something went wrong: {e.message}")
        session.commit()
        session.refresh(report)
        return report

