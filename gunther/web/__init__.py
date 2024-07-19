from flask import Flask, render_template, request
from gunther.writers import GeminiWriter
from gunther.audit import AuditReportGenerator, AuditProcess

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
        audit_process = AuditProcess(etherscan_address)
        result = audit_process.perform()
        writer = GeminiWriter()
        report_generator = AuditReportGenerator(result, writer)
        return report_generator.generate_html()
    else:
        return render_template("error.html")

def start_server():
    app.run(host="0.0.0.0", port=8080, debug=True)
