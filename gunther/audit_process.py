from gunther.core import AuditReport, AuditError
from gunther.auditors import list_of_auditors
from gunther.writers import GeminiWriter

class AuditProcess(object):
    def __init__(self, input: str):
        self.input = input

    def generate_report(self, title: str, description: str) -> AuditReport:
        report = AuditReport(
                title=title,
                description=description,
                findings=[],
                )

        writer = GeminiWriter()
        for auditor_name, auditor in list_of_auditors.items():
            print(f"INFO: Running `{auditor_name}` auditor")
            try:
                auditor.perform_audit(self.input)
                for finding in auditor.findings:
                    finding.description = writer.describe(finding)
                    report.findings.append(finding)
            except AuditError as e:
                print(f"ERROR: {e.message}")

        return report
