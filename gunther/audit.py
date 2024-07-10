from gunther.core import AuditResult, AuditError, FindingSeverity, Writer
from gunther.auditors import list_of_auditors
from gunther.writers import GeminiWriter

class AuditProcess(object):
    def __init__(self, input: str):
        self.input = input

    def perform(self) -> AuditResult:
        result =  AuditResult( findings=[],)
        for auditor_name, auditor in list_of_auditors.items():
            print(f"INFO: Running `{auditor_name}` auditor")
            try:
                auditor.perform_audit(self.input)
                for finding in auditor.findings:
                    result.add_finding(finding)
            except AuditError as e:
                print(f"ERROR: {e.message}")
        return result

class AuditReportGenerator(object):
    def __init__(self, result: AuditResult, writer: Writer):
        self.result = result
        self.writer = writer

    def generate_html(self) -> str:
        title = self.writer.extract_title(self.result)
        conclusion = self.writer.make_audit_result_conclusion(self.result)

        result = ''
        result += f'<center><h1>{title}</h1></center>'
        result +=  '<ol type="A">'
        result +=  '    <li>\n'
        result +=  '        <h2>Description</h2>\n'
        result += f'        <p>Our audit reported total of {self.result.get_findings_amount()} finding(s), categorized as follows</p>\n' 
        result +=  '        <ul>'
        finding_categories_count = self.result.get_finding_categories_count()
        for finding_category, amount in finding_categories_count.items():
            if finding_category == FindingSeverity.Note:
                result +=  f'            <li>{amount} {finding_category.value.lower()}(s)</li>'
            else:
                result +=  f'            <li>{amount} {finding_category.value.lower()}-severity issue(s)</li>'
        result +=  '        </ul>'
        if finding_categories_count[FindingSeverity.High] > 0:
            result += f"        <p>Based on those finding, There's critical security issue(s) were found.</p>\n"
        else:
            result += f'        <p>Based on those finding, No critical security issue(s) were found.</p>\n' 
        result +=  '    </li>\n'

        result +=  '    <li>\n<h2>Audit Findings</h2>\n'
        result +=  '        <ol type="1">\n'

        for finding in self.result.findings:
            result +=  '            <li>\n'
            result += f'            <h3>{finding.title}</h3>\n'
            result +=  '            <ol type="a">\n'
            result += f'                <li><h4>Severity: {finding.severity.value}</h4></li>\n'
            description = self.writer.describe_audit_finding(finding)
            result += f'                <li><h4>Description</h4><p>{description}</p></li>\n'
            result +=  '            </ol>\n'
            result +=  '            </li>\n'


        result += "\n</ol>\n</li>\n"
        result += "<li>\n"
        result += '        <h2>Conclusion</h2>\n'
        result += f'       <p>{conclusion}</p>\n' 
        result += "</li>\n"
        result += "</ol>\n"
        return result
