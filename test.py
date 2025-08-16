from src.logger import get_logger

logger = get_logger(__name__)

logger.info("logging is being done")
logger.error("Error occured ")
logger.warning("Warnign occured")