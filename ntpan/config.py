from pathlib import Path
from typing import Dict

import yaml

from ntpan.models.params import Params

CONFIG_PATH = Path("/etc/ntpan/config.yaml")


def _import() -> Dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "NTPAN requires a config file located at {}".format(str(CONFIG_PATH))
        )
    with CONFIG_PATH.open("r") as f:
        config = yaml.load(f) or {}
    return config


params = Params(**_import())
