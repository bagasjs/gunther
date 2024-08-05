import requests
import os

from gunther.core import AuditError

def kebab_to_title_case(text: str):
    items = text.split("-")
    new_items = []
    for item in items:
        parts = list(item)
        parts[0] = parts[0].upper()
        new_items.append("".join(parts))
    return " ".join(new_items)

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

class Etherscan(object):
    def __init__(self, apikey: str):
        self.__apikey = apikey

    def _make_request_to_etherscan(self):
        pass

    def validate_contract_address(self, address: str, network: str = "mainnet"):
        pass

    def download_contract_source(self, address: str, dirpath: str, override_if_dirpath_exists: bool = False):
        pass

    def get_contract_name(self, address: str) -> str:
        return address
