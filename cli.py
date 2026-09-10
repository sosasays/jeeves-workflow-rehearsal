import argparse
import importlib

parser = argparse.ArgumentParser(description="Jeeves workflow rehearsal")
parser.add_argument("command", choices=["status", "library"])
args = parser.parse_args()
module = importlib.import_module("commands." + args.command)
module.main()
