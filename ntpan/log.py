"""Logging instance setup & configuration."""

# Standard Library
import sys

# Third Party
from loguru import _Logger
from loguru import logger as _loguru_logger

_LOG_FMT = (
    "<lvl><b>[{level}]</b> {time:YYYYMMDD} {time:HH:mm:ss} <lw>|</lw> {name}<lw>:</lw>"
    "<b>{line}</b> <lw>|</lw> {function}</lvl> <lvl><b>→</b></lvl> {message}"
)
_LOG_LEVELS = [
    {"name": "TRACE", "color": "<m>"},
    {"name": "DEBUG", "color": "<c>"},
    {"name": "INFO", "color": "<le>"},
    {"name": "SUCCESS", "color": "<g>"},
    {"name": "WARNING", "color": "<y>"},
    {"name": "ERROR", "color": "<y>"},
    {"name": "CRITICAL", "color": "<r>"},
]


def base_logger() -> _Logger:
    """Initialize logging instance."""
    _loguru_logger.remove()
    _loguru_logger.add(sys.stdout, format=_LOG_FMT, level="INFO", enqueue=True)
    _loguru_logger.configure(levels=_LOG_LEVELS)
    return _loguru_logger


log = base_logger()
