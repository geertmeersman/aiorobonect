# aiorobonect

Asynchronous library to communicate with the Robonect API

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20a%20Duvel-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/f6qxuMA4)

[![MIT License](https://img.shields.io/github/license/geertmeersman/miwa?style=flat-square)](https://github.com/geertmeersman/miwa/blob/master/LICENSE)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/aiorobonect)](https://github.com/geertmeersman/aiorobonect/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/aiorobonect.svg)](http://isitmaintained.com/project/geertmeersman/aiorobonect)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/aiorobonect.svg)](http://isitmaintained.com/project/geertmeersman/aiorobonect)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/aiorobonect/pulls)

[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/aiorobonect/search?l=python)

[![github release](https://img.shields.io/github/v/release/geertmeersman/aiorobonect?logo=github)](https://github.com/geertmeersman/aiorobonect/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/aiorobonect)](https://github.com/geertmeersman/aiorobonect/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/aiorobonect)](https://github.com/geertmeersman/aiorobonect/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/aiorobonect)](https://github.com/geertmeersman/aiorobonect/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/aiorobonect?logo=github)](https://github.com/geertmeersman/aiorobonect/commits/main)


## API Example

```python
"""Test for aiorobonect."""
from aiorobonect import RobonectClient

import asyncio
import json
import aiohttp

async def main():
    host = "10.0.0.99"        ## The Robonect mower IP
    username = "USERNAME"    ## Your Robonect username
    password = "xxxxxxxx"    ## Your Robonect password
    tracking = [             ## Commands to query
                "battery",
                "wlan",
                "version",
                "timer",
                "hour",
                "error"
            ]
    client = RobonectClient(host, username, password)
    try:
        status = await client.async_cmd("status")
        print(status)
        tracking = await client.async_cmds(tracking)
        print(json.dumps(tracking, indent=2))
    except Exception as exception:
        if isinstance(exception, aiohttp.ClientResponseError):
            print(exception)
    await client.session_close()

asyncio.run(main())
```
