from typing import List
from gunther.core import AuditError
from gunther.analyzers.core import AnalysisResultItem, Severity, AnalysisResult, BaseAnalyzer
import subprocess
import json
import os

_impact_to_severity = {
    "High": Severity.High,
    "Medium": Severity.Medium,
    "Low": Severity.Low,
    "Informational": Severity.Note,
}

class SlitherAnalyzer(BaseAnalyzer):
    _checks: List[str]
    _result: AnalysisResult

    def __init__(self):
        self._result = AnalysisResult()
        self._checks = []

    def reset(self):
        self.findings = []
        self._checks = []

    def get_result(self) -> AnalysisResult:
        return self._result

    def analyze(self, input: str):
        self.reset()
        command = ["slither", input, "--etherscan-apikey", os.getenv("ETHERSCAN_API_KEY"), "--json", "-"]
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
                    severity = Severity.Unknown

                self._result.add_item(AnalysisResultItem(
                        title=check,
                        severity=severity,
                        description=detector["description"],
                    ))
                self._checks.append(check)
