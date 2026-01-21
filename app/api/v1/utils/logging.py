from loguru import logger
import logging
import sys

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

def setup_logger():
    logger.remove()

    logger.add(sys.stdout, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    for lib in ["httpx", "httpcore", "urllib3"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    return logger