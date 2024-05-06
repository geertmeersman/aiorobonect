"""Robonect library using aiohttp."""
from __future__ import annotations

from datetime import datetime
import json
import logging
import urllib.parse

import httpx

from .const import TIMEOUT
from .utils import transform_json_to_single_depth

_LOGGER = logging.getLogger(__name__)


def encode_dict_values_to_utf8(dictionary):
    """Encode dict values to utf8."""
    encoded_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            encoded_dict[key] = encode_dict_values_to_utf8(value)
        elif isinstance(value, str):
            encoded_dict[key] = value.encode("utf-8")
        else:
            encoded_dict[key] = value
    return encoded_dict


def validate_json(json_str):
    """Validate json string."""
    if isinstance(json_str, dict):
        return True
    try:
        return json.loads(json_str)
    except ValueError as error:
        print(error)
        return False


class RobonectException(Exception):
    """Raised when an update has failed."""

    def __init__(self, cmd, exception, result):
        """Init the Robonect Exception."""
        self.message = f"Aiorobonect call for cmd {cmd} failed: {result}\n{exception}"
        super().__init__(self.message)


class RobonectClient:
    """Class to communicate with the Robonect API."""

    def __init__(self, host, username, password, transform_json=False) -> None:
        """Initialize the Communication API to get data."""
        self.auth = None
        self.host = host
        self.username = username
        self.password = password
        self.client = None
        self.sleeping = None
        self.transform_json = transform_json
        if username is not None and password is not None:
            self.auth = (username, password)

    async def client_start(self):
        """Start the httpx client."""
        if not self.client:
            self.client = httpx.AsyncClient(timeout=TIMEOUT, auth=self.auth)

    async def client_close(self):
        """Close the httpx client."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def async_cmd(self, command=None, params={}) -> list[dict]:
        """Send command to mower."""
        if command is None:
            return False
        if params is None:
            params = ""
        else:
            params = urllib.parse.urlencode(params)

        if command == "job":
            _LOGGER.debug(f"Job params: {params}")
            return

        result_json = None
        await self.client_start()
        url = f"http://{self.host}/json?cmd={command}&{params}"
        _LOGGER.debug(f"Calling {url}")
        response = await self.client.get(url)
        if response.status_code == 200:
            result_text = response.text
            _LOGGER.debug(f"Rest API call result for {command}: {result_text}")
            result_json = json.loads(result_text)
            result_json["sync_time"] = datetime.now()
        elif response.status_code >= 400:
            response.raise_for_status()
        await self.client_close()

        if self.transform_json:
            return transform_json_to_single_depth(result_json)

        return result_json

    async def async_cmds(self, commands=None, bypass_sleeping=False) -> dict:
        """Send command to mower."""
        await self.client_start()
        result = await self.state()
        if result:
            result = {"status": result}
            if not self.sleeping or bypass_sleeping:
                for cmd in commands:
                    json_res = await self.async_cmd(cmd)
                    if json_res:
                        result.update({cmd: json_res})
            await self.client_close()
        return result

    async def state(self) -> dict:
        """Send status command to mower."""
        await self.client_start()
        result = await self.async_cmd("status")
        if result:
            self.sleeping = result.get("status").get("status") == 17
            await self.client_close()
        return result

    async def async_start(self) -> bool:
        """Start the mower."""
        result = await self.async_cmd("start")
        return result

    async def async_stop(self) -> bool:
        """Stop the mower."""
        result = await self.async_cmd("stop")
        return result

    async def async_reboot(self) -> bool:
        """Reboot Robonect."""
        result = await self.async_cmd("service", {"service": "reboot"})
        return result

    async def async_shutdown(self) -> bool:
        """Shutdown Robonect."""
        result = await self.async_cmd("service", {"service": "shutdown"})
        return result

    async def async_sleep(self) -> bool:
        """Make Robonect sleep."""
        result = await self.async_cmd("service", {"service": "sleep"})
        return result

    def sleeping(self) -> int:
        """Return if the mower is sleeping."""
        return self.sleeping
