"""Командная часть: разбор аргументов, вывод, коды возврата."""

import argparse
import logging
import os
import sys

from page_loader.errors import PageLoaderError
from page_loader.loader import download

logger = logging.getLogger("page_loader")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="page-loader",
        description="Downloads a page with its local resources",
    )
    parser.add_argument("url", help="page address")
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="output dir (default: current directory)",
    )
    parser.add_argument(
        "--log-level",
        default=os.environ.get("PAGE_LOADER_LOG_LEVEL", "WARNING"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="log level for stderr (default: WARNING)",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=args.log_level,
        stream=sys.stderr,
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        file_path = download(args.url, args.output)
    except PageLoaderError as error:
        logger.debug("download failed", exc_info=error)
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Page was downloaded as '{file_path}'")
    return 0


def run():
    sys.exit(main())


if __name__ == "__main__":
    run()
