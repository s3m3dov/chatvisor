import logging

from log_to_slack import SlackLogHandler

from core.config import settings
from core.extensions.log_formatter import default_formatter

__all__ = ["logger"]

logger = logging.getLogger("SmartBot App")

handler = logging.StreamHandler()
handler.setFormatter(default_formatter)
logger.addHandler(handler)

slack_handler = SlackLogHandler(
    slack_token=settings.slack_token,
    channel=settings.slack_channel,
    icon_url=settings.slack_icon_url,
    username="SmartBot App Alerts",
    stack_trace=True,
    fail_silent=False,
)
slack_handler.setLevel(logging.ERROR)
logger.addHandler(slack_handler)

logger.setLevel(logging.DEBUG)
