"""Minimal logging configuration for the MVP."""

import logging


def configure_logging(level: str) -> None:
    """Configure root logging once for local and container use."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
