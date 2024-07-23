import os
import subprocess

contracts = {
    "Shiba Inu Token": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    "Arexa Platform": "0x50DB175C83149B413A6962439E7AEb658C55791c",
}

if "reports" not in os.listdir(os.getcwd()):
    print("Report directory is not exists")
    os.mkdir("reports")

for contract_name, contract_address in contracts.items():
    print(f"TESTING: {contract_name}")
    command = ["python", "./main.py", "audit", contract_address]
    subprocess.run(command, shell=False)
    command = ["mv", "./report.html", f"reports/{contract_name}.html"]
    subprocess.run(command, shell=False)

