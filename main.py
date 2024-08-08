from dotenv import load_dotenv
import sys
from gunther.web import start_server
from gunther.web.core import migrate_fresh
from gunther.web.core.db import migrate_up, migrate_down, migrate_fresh

load_dotenv()

if __name__ == "__main__":
    argv = sys.argv
    def shift_argv(argv: list[str], on_empty_error_message: str) -> tuple[str, list[str]]:
        if len(argv) == 0:
            print(f"ERROR: {on_empty_error_message}")
            sys.exit(-1)
        return argv[0], argv[1:]
    argv = sys.argv
    program, argv = shift_argv(argv, "Unreachable state")
    subcommand, argv = shift_argv(argv, "Please provide the subcommand. Check at subcommand `help` for list of available subcommands")

    match subcommand:
        case "serve":
            start_server()
        case "migrate-up":
            migrate_up()
        case "migrate_down":
            migrate_down()
        case "migrate-fresh":
            migrate_fresh()
        case "help":
            print(f"USAGE: {program} <SUBCOMMAND>")
            print("List of subcommands")
            print("    serve         Start gunther web server")
            print("    migrate-up    Generate tables in database")
            print("    migrate-down  Remove every tables in database")
            print("    migrate-fresh `migrate-down` followed by `migrate-up`")
            print("    help          Get this help message")
        case _:
            pass

