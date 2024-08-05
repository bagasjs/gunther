import os
import subprocess

contracts = {
    "Shiba Inu Token": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    # "Arexa Platform": "0x8D2DB3aa724f55d447b0F05EBBb8f09F0dF357Bf",
}

if "reports" not in os.listdir(os.getcwd()):
    print("Report directory is not exists")
    os.mkdir("reports")

for contract_name, contract_address in contracts.items():
    print(f"TESTING: {contract_name}")
    command = ["python", "./cli.py", "audit", contract_address]
    subprocess.run(command, shell=False)
    command = ["mv", "./report.html", f"reports/{contract_name}.html"]
    subprocess.run(command, shell=False)

