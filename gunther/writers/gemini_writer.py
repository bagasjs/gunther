import google.generativeai as genai
import os

from gunther.core import AuditFinding, Writer

class GeminiWriter(Writer):
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.0-pro-latest")

    def describe(self, finding: AuditFinding) -> str:
        prompt = f"This is an audit finding of a smart contract. Could you make the description of this finding?\n\n${finding.title}\n${finding.description}"
        response = self.model.generate_content(prompt)
        return response.text

