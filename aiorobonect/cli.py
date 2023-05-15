"""Cli for aiorobonect."""
import asyncio
import logging

from aiorobonect import RobonectClient

_LOGGER = logging.getLogger(__name__)


async def run_tester(host: str, username: str, password: dict):
    """Run tester for aiorobonect."""
    try:
        client = RobonectClient(host, username, password)
        status = await client.async_cmd("status")
        _LOGGER.debug(f"Status: {status}")
        await client.session_close()
    except Exception:
        return "Something went wrong"


def main():
    """Tester for the Robonect Automower API.

    The tester will login to host using username and password

    """
    import argparse

    parser = argparse.ArgumentParser(
        description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-h", "--host", required=True, help="Robonect host address")
    parser.add_argument("-u", "--username", required=True, help="Robonect username")
    parser.add_argument("-p", "--password", required=True, help="Robonect password")

    args = parser.parse_args()

    logging.basicConfig(level="DEBUG", format="%(asctime)s;%(levelname)s;%(message)s")
    asyncio.run(run_tester(args.host, args.username, args.password))
