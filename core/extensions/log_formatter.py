from typing import Optional

import colorlog
from pydantic.main import BaseModel

__all__ = ["default_formatter", "FormatterConfig"]


class FormatterConfig(BaseModel):
    """
    Config for Logging
    """

    date_format: Optional[str] = "%Y-%m-%d %H:%M:%S"
    format: Optional[str] = (
        "%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)s] "
        "(%(name)s) %(message)s"
    )
    log_colors: Optional[dict] = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }


formatter_config = FormatterConfig()

default_formatter = colorlog.ColoredFormatter(
    fmt=formatter_config.format,
    datefmt=formatter_config.date_format,
    log_colors=formatter_config.log_colors,
)
