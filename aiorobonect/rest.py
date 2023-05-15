"""Robonect library using aiohttp."""
from __future__ import annotations

import logging
import urllib.parse

import aiohttp

from .const import TIMEOUT
from .utils import transform_json_to_single_depth

_LOGGER = logging.getLogger(__name__)


class RobonectClient:
    """Class to communicate with the Robonect API."""

    def __init__(self, host, username, password, transform_json=False) -> None:
        """Initialize the Communication API to get data."""
        auth = None
        self.host = host
        self.session = None
        self.transform_json = transform_json
        if username is not None and password is not None:
            auth = aiohttp.BasicAuth(login=username, password=password)
            self.session = aiohttp.ClientSession(
                read_timeout=TIMEOUT, raise_for_status=True, auth=auth
            )

    async def session_close(self):
        """Close the session."""
        await self.session.close()

    async def async_cmd(self, command=None, params={}) -> list[dict]:
        """Send command to mower."""
        if command is None:
            return False
        params = urllib.parse.urlencode(params)
        if command == "job":
            _LOGGER.debug(f"Job params: {params}")
            return

        async with self.session.get(
            f"http://{self.host}/json?cmd={command}&{params}"
        ) as response:
            result = await response.json()
            _LOGGER.debug("Response mower data: %s", response)
            if response.status == 200:
                result = await response.json()
                _LOGGER.debug("Result mower data: %s", result)
            if response.status >= 400:
                response.raise_for_status()
        if self.transform_json:
            return transform_json_to_single_depth(result)
        return result

    async def async_cmds(self, commands=None) -> list[dict]:
        """Send command to mower."""
        result = []
        for cmd in commands:
            result.append({cmd: await self.async_cmd(cmd)})
        await self.session_close()
        return result
