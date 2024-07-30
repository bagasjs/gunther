from flask import Flask, render_template, request
from gunther.core import AuditError
from gunther.utils import get_contract_name_from_etherscan
from gunther.writers import GeminiWriter
from gunther.audit import AuditReportRenderer, Auditor

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/try-audit", methods=[ "GET", "POST" ])
def try_audit():
    # 0x50DB175C83149B413A6962439E7AEb658C55791c
    if request.method == "POST":
        etherscan_address = request.form.get("etherscan_address")
        if etherscan_address == None:
            return render_template("error.html", error_message="Something went wrong please provide an etherscan address")
        auditor = Auditor()
        report = auditor.perform_audit(etherscan_address)
        renderer = AuditReportRenderer(report)
        return renderer.render()
    else:
        return render_template("error.html")

def start_server():
    app.run(host="0.0.0.0", port=8080, debug=True)
