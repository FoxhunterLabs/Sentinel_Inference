from __future__ import annotations

import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    # Reset handlers to avoid duplicates in reload
    root.handlers = [handler]
