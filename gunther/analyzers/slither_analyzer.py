from typing import List
from gunther.core import Analyzer, AuditError, AuditFinding, FindingSeverity
import subprocess
import json

_impact_to_severity = {
    "High": FindingSeverity.High,
    "Medium": FindingSeverity.Medium,
    "Low": FindingSeverity.Low,
    "Informational": FindingSeverity.Note,
}


class SlitherAnalyzer(Analyzer):
    _checks: List[str]

    def reset(self):
        self.findings = []
        self._checks = []

    def analyze(self, input: str):
        self.reset()
        command = ["slither", input, "--json", "-"]
        result = subprocess.run(command, shell=False, stdout=subprocess.PIPE)
        raw_findings_as_str = result.stdout.decode("utf-8")
        if len(raw_findings_as_str) == 0:
            raise AuditError(f"Failed to perform audit for `{input}` with slither")
        raw_findings = json.loads(raw_findings_as_str)

        if "results" not in raw_findings:
            raise AuditError(f"Key `result` is not in output, these might be happened due to version change")
        if "detectors" not in raw_findings["results"]:
            raise AuditError(f"Key `detectors` is not in output['results'], these might be happened due to version change")

        for detector in raw_findings["results"]["detectors"]:
            check = detector["check"]
            if check not in self._checks:
                try:
                    severity = _impact_to_severity[detector["impact"]]
                except KeyError:
                    severity = FindingSeverity.Unknown

                audit_finding = AuditFinding(
                        title=check,
                        auditor="slither",
                        severity=severity,
                        recommendation="",
                        raw=detector["description"],
                        )
                self.findings.append(audit_finding)
                self._checks.append(check)
