import google.generativeai as genai
import os
import json

from gunther.writers.core import Writer
from gunther.core import AuditFinding, AuditResult, DescribedAuditFinding

class GeminiWriter(Writer):
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def describe_finding(self, finding: AuditFinding) -> DescribedAuditFinding:
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you give only the description of what happened based on this finding? {finding.raw}"
        description = self.execute_prompt(prompt)
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you give the recommndation of what should be done based on this finding? {finding.raw}"
        recommendation = self.execute_prompt(prompt)
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you tell me what title would be fit in the report based on this finding given by the analyzer \"{finding.raw}\" (NOTE Please provide the title only in your answer since I want to use it in my program)"
        title = self.execute_prompt(prompt)
        described = DescribedAuditFinding(title, finding.raw, finding.severity, description, recommendation)
        return described

    def execute_prompt(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def make_audit_result_conclusion(self, result: AuditResult) -> str:
        result_as_json = json.dumps(result.to_dict())
        prompt  =  "The following JSON data is an audit result for a smart contract."
        prompt += f"Could you make a conclustion based on the result in raw text format?\n\n {result_as_json}"
        return self.execute_prompt(prompt)

    def describe_audit_finding(self, finding: AuditFinding) -> str:
        prompt = f"This is an audit finding of a smart contract. Could you make the description of this finding in raw text format?\n\n${finding.title}\n${finding.description}"
        return self.execute_prompt(prompt)
