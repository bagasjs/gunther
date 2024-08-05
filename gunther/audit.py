from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from gunther.writers import Writer
from gunther.core import AuditReport, AuditFinding, AuditError, Model
from gunther.analyzers import list_of_analyzers, FindingSeverity
from gunther.utils import html
from gunther.writers.gemini_writer import GeminiWriter
from datetime import datetime, timedelta, timezone

class Auditor(object):
    _engine: Engine
    _session: Session
    _sessionmaker: sessionmaker
    _writer: Writer

    AMOUNT_OF_RETRIES = 5

    def __init__(self):
        self._engine = create_engine("sqlite:///database.sqlite")
        self._sessionmaker = sessionmaker()
        self._sessionmaker.configure(bind=self._engine)
        self._session = self._sessionmaker()
        self._writer = GeminiWriter()
        Model.metadata.create_all(self._engine)

    def perform_audit(self, address: str, with_description = True, with_recommendation = True, echo = True) -> AuditReport:
        stmt = select(AuditReport).where(AuditReport.address == address).limit(1)
        report = self._session.execute(stmt).scalars().one_or_none()
        if report is None:
            report = AuditReport(title="A smart contract", address=address, conclusion="")
            self._session.add(report)
        else:
            if echo: print(f"INFO: There's already an audit report for `{address}`")
            required_time_range_to_change = (datetime.now() - timedelta(minutes=1)) # should be 1 week
            if report.updated > required_time_range_to_change:
                if echo: print(f"INFO: The report `{address}` is already recent")
                print(report.address == address)
                return report
            # TODO: Here since the report is already exists but need to be updated, we have to remove all of its old findings
            report.findings.clear()
            pass
        self._session.commit()

        # TODO: research if there's really no needs to use another analyzer
        for name, analyzer in list_of_analyzers.items():
            if echo: print(f"INFO: Running `{name}` analyzer")
            try:
                analyzer.analyze(address)
                for item in analyzer.get_results():
                    if echo: print(f"INFO: processing finding {item.title}")
                    description = None
                    recommendation = None
                    for _ in range(self.AMOUNT_OF_RETRIES):
                        try:
                            print(item.title, "===>", item.raw)
                            if with_description:
                                description = self._writer.make_description_from_raw_finding(item.raw)
                            if with_recommendation:
                                recommendation = self._writer.make_description_from_raw_finding(item.raw)
                            break
                        except Exception as e:
                            print(f"ERROR: {e}")

                    if description == None:
                        description = item.raw

                    self._session.add(AuditFinding(
                        title = item.title,
                        severity = item.severity.value,
                        raw = item.raw,
                        description = description,
                        recommendation = recommendation,
                        report_id = report.id,
                        ))
            except AuditError as e:
                print(f"ERROR: {e.message}")
        self._session.commit()

        # TODO: Change the report conclusion and updated timestamp
        report.updated = datetime.now()
        for _ in range(self.AMOUNT_OF_RETRIES):
            try:
                report.conclusion = self._writer.make_audit_report_conclusion(report)
                break
            except Exception as e:
                print(f"ERROR: {e}")
        self._session.commit()

        if echo: print("INFO: Analysis complete")
        return report

class AuditReportRenderer(object):
    def __init__(self, report: AuditReport):
        self.report = report
        self._finding_counts_by_severity = {}
        self._finding_counts_by_severity[FindingSeverity.Note] = 0
        self._finding_counts_by_severity[FindingSeverity.Low] = 0
        self._finding_counts_by_severity[FindingSeverity.Medium] = 0
        self._finding_counts_by_severity[FindingSeverity.High] = 0
        for finding in self.report.findings:
            severity = FindingSeverity[finding.severity]
            self._finding_counts_by_severity[severity] += 1

    def render(self) -> str:
        total_findings = len(self.report.findings)
        result = ''
        result += f'<center><h1>{self.report.title}</h1></center>'
        result +=  '<ol type="A">'
        result +=  '    <li>\n'
        result +=  '        <h2>Description</h2>\n'
        result += f'        <p>Our audit reported total of {total_findings} finding(s), categorized as follows</p>\n' 
        result +=  '        <ul>'

        for finding_category, amount in self._finding_counts_by_severity.items():
            if finding_category == FindingSeverity.Note:
                result +=  f'            <li>{amount} {finding_category.value.lower()}(s)</li>'
            else:
                result +=  f'            <li>{amount} {finding_category.value.lower()}-severity issue(s)</li>'
        result +=  '        </ul>'
        if self._finding_counts_by_severity[FindingSeverity.High] > 0:
            result += f"        <p>Based on those finding, There's critical security issue(s) were found.</p>\n"
        else:
            result += f'        <p>Based on those finding, No critical security issue(s) were found.</p>\n' 
        result +=  '    </li>\n'

        result +=  '    <li>\n<h2>Audit Findings</h2>\n'
        result +=  '        <ol type="1">\n'

        for finding in self.report.findings:
            result +=  '            <li>\n'
            result += f'            <h3>{finding.title}</h3>\n'
            result +=  '            <ol type="a">\n'
            result += f'                <li><h4>Severity: {finding.severity}</h4></li>\n'
            result += f'                <li><h4>Description</h4><p>{finding.description}</p></li>\n'
            if finding.recommendation:
                result += f'                <li><h4>Recommendation</h4><p>{finding.recommendation}</p></li>\n'
            result +=  '            </ol>\n'
            result +=  '            </li>\n'


        result += "\n</ol>\n</li>\n"
        result += "<li>\n"
        result += '        <h2>Conclusion</h2>\n'
        result += f'       <p>{self.report.conclusion}</p>\n' 
        result += "</li>\n"
        result += "</ol>\n"
        return result
