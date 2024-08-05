import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from gunther.web.controllers import audit_reports_controller, audit_findings_controller

load_dotenv()
app = FastAPI()

if __name__ == "__main__":
    app.include_router(audit_reports_controller.router)
    app.include_router(audit_findings_controller.router)
    uvicorn.run(app=app, host="localhost", port=8000)
