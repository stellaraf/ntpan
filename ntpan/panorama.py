from typing import Tuple

import xmltodict
from httpx import AsyncClient

from ntpan.config import params
from ntpan.log import log
from ntpan.models.device import Device


async def get_devices() -> Tuple[Device]:
    async with AsyncClient(
        params={"key": params.panorama.api_key.get_secret_value(), "type": "op"}
    ) as client:
        log.debug("Opened connection to {}", str(params.panorama.url))
        res = await client.get(
            str(params.panorama.url),
            params={"cmd": "<show><devices><connected></connected></devices></show>"},
        )
        parsed = xmltodict.parse(res.text)
        if "@status" not in parsed["response"]:
            log.warning("Failed to get devices")
            log.warning(parsed)
            raise RuntimeError("Failed to get devices")
        devices = ()

        for result in parsed["response"]["result"]["devices"]["entry"]:
            device = {
                "hostname": result["hostname"],
                "ip": result["ip-address"],
                "version": result["sw-version"],
                "model": result["model"],
                "uptime": result["uptime"],
            }

            devices += (Device(**device),)
        log.debug("All devices:\n{}", devices)
        return devices
