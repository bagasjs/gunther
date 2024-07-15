import json
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

contracts = {
    "Shiba Inu Token": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    "Arexa Platform": "0x50DB175C83149B413A6962439E7AEb658C55791c",
}

timeout = 10
for contract_name, contract_address in contracts.items():
    print("ANALYZING " + contract_name)
    command = [ "myth", "analyze", "-a", contract_address, "--rpc", "infura-mainnet", "--infura-id", os.getenv("INFURA_ID"),
            "--execution-timeout", str(timeout), "-o", "json", ]
    result = subprocess.run(command, shell=False, stdout=subprocess.PIPE)
    raw_findings_as_str = result.stdout.decode("utf-8")
    raw_findings = json.loads(raw_findings_as_str)
    print(raw_findings)

