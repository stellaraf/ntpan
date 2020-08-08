import re
from typing import Any, Generator, Mapping, Sequence

FAILURE = """
NTP state:
    NTP not synched, using local clock
    NTP server: 162.159.200.1
        status: rejected
        reachable: yes
        authentication-type: none
    NTP server: 162.159.200.123
        status: rejected
        reachable: yes
        authentication-type: none
"""

SUCCESS = """
NTP state:
    NTP synched to 162.159.200.123
    NTP server: 162.159.200.1
        status: available
        reachable: yes
        authentication-type: none
    NTP server: 162.159.200.123
        status: synched
        reachable: yes
        authentication-type: none
"""


def _map_value(value: str) -> Any:
    value_map = {
        "none": None,
        "yes": True,
        "no": False,
    }
    if value in value_map:
        value = value_map[value]
    return value


def _map_kv(line: str) -> Generator:
    k, v = line.split(": ")
    k = re.sub(r"\W", "_", k).lower()
    if "ntp_server" in k:
        k = "server"
    yield k
    yield _map_value(v)


def parse_output(output: str) -> Mapping:
    _, values = output.strip().split("NTP state:")

    values = [l.strip() for l in values.splitlines() if l]
    sync_str = values.pop(0)
    synced = None

    if "local clock" in sync_str:
        synced = False
    elif "NTP synched" in sync_str:
        synced = True

    servers = []
    server_idx = []
    for i, val in enumerate(values):
        if "NTP server:" in val:
            server_idx.append(i)

    for i, idx in enumerate(server_idx):
        if idx != 0:
            servers.append(values[:idx])

        if i == len(server_idx) - 1:
            servers.append(values[idx:])

    server_statuses = []
    for server in servers:
        status = {}
        for line in server:
            k, v = _map_kv(line)
            status[k] = v

        server_statuses.append(status)

    return {"synced": synced, "servers": server_statuses}
