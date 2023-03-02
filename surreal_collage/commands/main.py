# This file is adapted from https://git.corp.adobe.com/euclid/python-project-scaffold
import argparse
import sys
from enum import IntEnum
from pathlib import Path

from surreal_collage.log import logger
from surreal_collage.commands.action1 import create_action1_parser
from surreal_collage.commands.action2 import create_action2_parser

def parse_args(argv):
  parser = argparse.ArgumentParser(description="SurrealCollage command line actions")

  parser.add_argument(
    "--verbose", action='store_true', dest='verbose',
  )
  parser.add_argument("--log-file", type=Path)


  # Actions
  subparser = parser.add_subparsers(
    help="Action to perform", dest="action", required=True
  )
  create_action1_parser(subparser)
  create_action2_parser(subparser)

  # Parse arguments
  return parser.parse_args(argv)


def main(argv = sys.argv[1:]):
  args = parse_args(argv)

  # 0 handler is console
  if args.verbose:
    logger.handlers[0].setLevel("DEBUG")
  else:
    logger.handlers[0].setLevel("INFO")

  if args.log_file:
    logger.info("Logging into the file %s", args.log_file)
    args.log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add_log_file(args.log_file, "DEBUG")

  # Run the action.
  return args.func(args)

# Needed by setup.py console scripts
def main_cmd():
  main()

if __name__ == "__main__":
  main()
