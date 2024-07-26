from __future__ import annotations
from typing import Dict, List
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

class HTMLElement(object):
    def __init__(self, tag, attrs: Dict[str, str], children: List[HTMLElement]):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def set_attr(self, key: str, value: str) -> HTMLElement:
        self.attrs[key] = value
        return self

class HTMLGenerator(object):
    _output: str

    @classmethod
    def h1(cls, *childs: HTMLElement):
        return HTMLElement(
                "h1",
                {},
                list(childs),)

    def __init__(self):
        self._output = ""


class Etherscan(object):
    def __init__(self, apikey: str):
        self.__apikey = apikey

    def validate_address(self, network: str, address: str) -> bool:
        return True

    def _make_request_to_etherscan(self):
        pass

    def download_contract_source(self, address: str, dirpath: str, override_if_dirpath_exists: bool = False):
        pass

    def get_contract_name(self, address: str) -> str:
        return address
