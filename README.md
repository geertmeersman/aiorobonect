# aiorobonect

Asynchronous library to communicate with the Robonect API

## API Example

```python
"""Test for aiorobonect."""
from aiorobonect import RobonectClient

import asyncio
import json

host = "10.0.0.2"        ## The Robonect mower IP
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

async def main():
    client = RobonectClient(host, username, password)
    status = await client.async_cmd("status")
    print(status)
    tracking = await client.async_cmds(tracking)
    print(json.dumps(tracking, indent=2))
    await client.session_close()

asyncio.run(main())
```
