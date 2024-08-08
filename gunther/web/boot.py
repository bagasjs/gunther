from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from gunther.web.controllers import audit_reports_controller, audit_findings_controller, others_controller

app = FastAPI()
app.include_router(audit_reports_controller.router)
app.include_router(audit_findings_controller.router)
app.include_router(others_controller.router)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )


def start_server():
    uvicorn.run(app="gunther.web.boot:app", host="localhost", port=8000, reload=True)
