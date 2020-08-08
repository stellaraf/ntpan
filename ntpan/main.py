import asyncio
import sys
from ipaddress import IPv4Network, IPv6Network, ip_network
from typing import Any, Dict, List, Union

from ntpan.config import params
from ntpan.device import get_ntp_output
from ntpan.log import log
from ntpan.mailer import send_email
from ntpan.models.device import Device
from ntpan.panorama import get_devices
from ntpan.parse import parse_output


def _member_of(target: Any, networks: List[Union[IPv4Network, IPv6Network]]) -> bool:
    """Check if IP address belongs to network."""
    membership = False

    if not isinstance(target, (IPv4Network, IPv6Network)):
        target = ip_network(target)

    for network in networks:

        if (
            network.network_address <= target.network_address
            and network.broadcast_address >= target.broadcast_address  # NOQA: W503
        ):
            membership = True
            break

    return membership


async def _gather(device: Device) -> Dict:
    ntp_output = await get_ntp_output(device)
    if ntp_output is not None:
        result = {"device": device.hostname}
        parsed = parse_output(ntp_output)
        result.update(parsed)
        return result


async def collect(email: bool = True) -> List[Dict]:
    log.info("Starting collection...")
    devices = await get_devices()
    coros = [_gather(d) for d in devices if _member_of(d.ip, params.device_subnets)]
    base_results = await asyncio.gather(*coros)
    results = sorted([r for r in base_results if r], key=lambda r: r["device"].lower())
    if email:
        send_email(results)
    return results


def run(email: bool = True) -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(collect(email=email))
    except KeyboardInterrupt:
        print("Exiting...")
        loop.stop()
        sys.exit(1)


if __name__ == "__main__":
    run()
