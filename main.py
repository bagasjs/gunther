from typing import Tuple, List
import sys
from gunther import AuditProcess
from gunther.http import GuntherServer

def shift_argv(argv: List[str], on_empty_error_message: str) -> Tuple[str, list[str]]:
    if len(argv) == 0:
        print(f"ERROR: {on_empty_error_message}")
        sys.exit(-1)
    return argv[0], argv[1:]

if __name__ == "__main__":
    argv = sys.argv
    program, argv = shift_argv(argv, "Unreachable state")
    subcommand, argv = shift_argv(argv, 
      "Please provide the subcommand. Check at subcommand `help` for list of available subcommands")
    
    match subcommand:
        case "help":
            print(f"USAGE: {program} <SUBCOMMAND>")
            print("List of subcommands")
            print("    audit  Audit a smart contract via source code or address and generate the PDF report")
            print("    serve  Run a gunther via web interface")
            print("    help   Get this help message")
        case "audit":
            input, argv = shift_argv(argv, "Please provide the address or file path of the smart contract")
            audit_process = AuditProcess(input)
            audit_report = audit_process.generate_report("Audit", "Bagas Jonathan Sitanggang")
            with open("report.html", "w") as file:
                file.write(audit_report.to_html())
        case "serve":
            server = GuntherServer()
            server.start(8080)
        case _:
            print(f"ERROR: Please provide a valid subcommand")
            sys.exit(-1)

