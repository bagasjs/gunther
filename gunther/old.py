class AuditResult(object):
    _findings_amount: int
    _findings_categories_count: Dict[FindingSeverity, int]
    _findings_changed: bool

    findings: List[AuditFinding]
    unix_timestamp: int
    context: str
    context_is_address: bool

    def __init__(self, context: str, context_is_address: bool, findings: List[AuditFinding]):
        self.findings = findings
        self.context = context
        self.context_is_address = context_is_address

        self._findings_amount = len(self.findings)
        self._findings_categories_count = {}
        self._findings_categories_count[FindingSeverity.Note] = 0
        self._findings_categories_count[FindingSeverity.Low] = 0
        self._findings_categories_count[FindingSeverity.Medium] = 0
        self._findings_categories_count[FindingSeverity.High] = 0
        self._findings_changed = True

    def add_finding(self, finding: AuditFinding):
        self._findings_amount += 1
        self._findings_changed = True
        self.findings.append(finding)

    def get_findings_amount(self) -> int:
        return self._findings_amount

    def get_finding_categories_count(self) -> Dict[FindingSeverity, int]:
        if self._findings_changed:
            for finding in self.findings:
                self._findings_categories_count[finding.severity] += 1
        return self._findings_categories_count

    def set_timestamp_as_now(self):
        self.unix_timestamp = int(datetime(1970,1,1,1,0,tzinfo=timezone.utc).timestamp())

    def to_dict(self) -> dict:
        findings = []
        for finding in self.findings:
            findings.append(finding.to_dict())
        data = { "findings": findings, }
        return data
