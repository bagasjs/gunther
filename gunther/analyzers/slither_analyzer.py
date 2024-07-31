from typing import List
from gunther.core import AuditError
from gunther.analyzers.core import Analyzer, FindingSeverity, AnalysisResult
import subprocess
import json
import os

_impact_to_severity = {
    "High": FindingSeverity.High,
    "Medium": FindingSeverity.Medium,
    "Low": FindingSeverity.Low,
    "Informational": FindingSeverity.Note,
}

class SlitherAnalyzer(Analyzer):
    _checks: List[str]
    _results: List[AnalysisResult]

    def reset(self):
        self._results = []
        self._checks  = []

    def get_results(self) -> List[AnalysisResult]:
        return self._results

    def analyze(self, input: str):
        self.reset()
        command = ["slither", input, "--etherscan-apikey", os.getenv("ETHERSCAN_API_KEY"), "--json", "-"]
        raw_findings_as_str = ""
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

                self._results.append(AnalysisResult(
                    title=check,
                    severity=severity,
                    raw=detector["description"],
                    ))
                self._checks.append(check)
