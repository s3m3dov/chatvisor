import logging

from slacker_log_handler import SlackerLogHandler

from core.extensions.log_formatter import default_formatter

__all__ = ["default_handler", "slack_handler"]

default_handler = logging.StreamHandler()
default_handler.setFormatter(default_formatter)

slack_handler = SlackerLogHandler(
    api_key="xapp-1-A05BDKKMGUF-5395593308166-0d206b97a13ab72b63c3d405f3cdb67fe71cd7aa93ab08ecd1a62108bc7c84fd",
    channel="random",
    stack_trace=True,
    username="SmartBot Alerts",
    icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToa29oI8p2lspzZr6QkUMvEIYcgSzCZurrUizGavSGSA&s",
)
slack_handler.setLevel(logging.ERROR)
