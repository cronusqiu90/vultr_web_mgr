from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format="{time:%Y-%m-%d %H:%m:%S} | {level: >7} | {message}",
    level="INFO",
)
