from scrapli.driver import AsyncGenericDriver
from scrapli.exceptions import ScrapliException

from ntpan.config import params
from ntpan.log import log
from ntpan.models.device import Device


async def get_ntp_output(device: Device) -> str:
    try:
        async with AsyncGenericDriver(
            transport="asyncssh",
            host=str(device.ip),
            auth_username=params.device_username,
            auth_password=params.device_password.get_secret_value(),
            auth_strict_key=False,
            timeout_ops=60,
            timeout_transport=60,
            timeout_socket=10,
            ssh_known_hosts_file=False,
        ) as connection:
            log.debug("Opened connection to {}", device.hostname)
            await connection.send_command("set cli pager off")
            res = await connection.send_command("show ntp")
        return res.result
    except ScrapliException as err:
        log.warning(err)
