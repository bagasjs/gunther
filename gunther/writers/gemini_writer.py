import google.generativeai as genai
import os
import json

from gunther.core import AuditFinding, AuditResult, Writer

class GeminiWriter(Writer):
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.0-pro-latest")

    def _execute_prompt(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def extract_title(self, result: AuditResult) -> str:
        return "Audit Report of SMART CONTRACT"

    def make_audit_result_conclusion(self, result: AuditResult) -> str:
        result_as_json = json.dumps(result.to_dict())
        prompt  =  "The following JSON data is an audit result for a smart contract."
        prompt += f"Could you make a conclustion based on the result in raw text format?\n\n {result_as_json}"
        return self._execute_prompt(prompt)

    def describe_audit_finding(self, finding: AuditFinding) -> str:
        prompt = f"This is an audit finding of a smart contract. Could you make the description of this finding in raw text format?\n\n${finding.title}\n${finding.description}"
        return self._execute_prompt(prompt)
