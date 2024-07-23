import requests
import os

from gunther.core import AuditError

def get_contract_name_from_etherscan(address: str) -> str:
    apikey = os.environ["ETHERSCAN_API_KEY"]
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={apikey}"
    res = requests.get(url)
    if not res.ok:
        raise AuditError(res.text)
    data = res.json()
    if data["message"] != "OK":
        raise AuditError(data["result"])
    if len(data["result"]) < 1:
        raise AuditError("Invalid etherscan address")
    if "ContractName" not in data["result"][0]:
        raise AuditError("Invalid key expecting ContractName this may be happened due to API change")
    return data["result"][0]["ContractName"]



