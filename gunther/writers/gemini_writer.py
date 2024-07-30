import google.generativeai as genai
import os
import json

from gunther.core import AuditReport
from gunther.writers.core import Writer

class GeminiWriter(Writer):
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def make_description_from_raw_finding(self, raw_finding: str) -> str:
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you give only the description of what happened based on this finding? {raw_finding}"
        return self.execute_prompt(prompt)
    
    def make_recommendation_from_raw_finding(self, raw_finding: str) -> str:
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you give the recommndation of what should be done based on this finding? {raw_finding}"
        return self.execute_prompt(prompt)

    def infer_title_from_raw_finding(self, raw_finding: str) -> str:
        prompt = f"The following is a raw analysis data from a smart contract analyzer. Could you tell me what title would be fit in the report based on this finding given by the analyzer \"{raw_finding}\" (NOTE Please provide the title only in your answer since I want to use it in my program)"
        return self.execute_prompt(prompt)

    def execute_prompt(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def make_audit_report_conclusion(self, report: AuditReport) -> str:
        result_as_json = json.dumps(report.to_dict())
        prompt  =  "The following JSON data is an audit result for a smart contract."
        prompt += f"Could you make a conclustion based on the result in raw text format?\n\n {result_as_json}"
        return self.execute_prompt(prompt)

    def make_audit_result_conclusion(self, result) -> str:
        result_as_json = json.dumps(result.to_dict())
        prompt  =  "The following JSON data is an audit result for a smart contract."
        prompt += f"Could you make a conclustion based on the result in raw text format?\n\n {result_as_json}"
        return self.execute_prompt(prompt)
