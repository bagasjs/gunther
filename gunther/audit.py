from gunther.core import AuditResult, AuditError, FindingSeverity
from gunther.writers import Writer
from gunther.analyzers import list_of_analyzers

class AuditProcess(object):
    def __init__(self, input: str):
        self.input = input

    def perform(self) -> AuditResult:
        # TODO: find a way to support source files not only etherscan address
        result =  AuditResult(context=self.input, context_is_address=True, findings=[],)
        for name, analyzer in list_of_analyzers.items():
            print(f"INFO: Running `{name}` analyzer")
            try:
                analyzer.analyze(self.input)
                for finding in analyzer.findings:
                    result.add_finding(finding)
            except AuditError as e:
                print(f"ERROR: {e.message}")
        result.set_timestamp_as_now()
        return result

class AuditReportGenerator(object):
    def __init__(self, title: str, result: AuditResult, writer: Writer):
        self.title = title
        self.result = result
        self.writer = writer

    def generate_html(self) -> str:
        conclusion = self.writer.make_audit_result_conclusion(self.result)
        result = ''
        result += f'<center><h1>{self.title}</h1></center>'
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
            descibed_finding = self.writer.describe_finding(finding)
            result +=  '            <li>\n'
            result += f'            <h3>{descibed_finding.title}</h3>\n'
            result +=  '            <ol type="a">\n'
            result += f'                <li><h4>Severity: {descibed_finding.severity.value}</h4></li>\n'
            result += f'                <li><h4>Description</h4><p>{descibed_finding.description}</p></li>\n'
            result += f'                <li><h4>Recommendation</h4><p>{descibed_finding.recommendation}</p></li>\n'
            result +=  '            </ol>\n'
            result +=  '            </li>\n'


        result += "\n</ol>\n</li>\n"
        result += "<li>\n"
        result += '        <h2>Conclusion</h2>\n'
        result += f'       <p>{conclusion}</p>\n' 
        result += "</li>\n"
        result += "</ol>\n"
        return result
