from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from gunther.web.core import templates
from gunther.web.controllers import api_audit_reports_controller, api_audit_findings_controller, api_others_controller, audit_reports_controller

app = FastAPI()
app.mount("/static", StaticFiles(directory="./resources/static"), name="static")
app.include_router(api_audit_reports_controller.router)
app.include_router(api_audit_findings_controller.router)
app.include_router(api_others_controller.router)
app.include_router(audit_reports_controller.router)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
            request=request,
            name="index.html",
            )

def start_server():
    uvicorn.run(app="gunther.web.boot:app", host="localhost", port=8000, reload=True)
