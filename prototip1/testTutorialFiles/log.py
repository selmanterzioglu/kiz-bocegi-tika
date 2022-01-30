import logging 

logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
    level= logging.DEBUG)

logger = logging.getLogger()

logger.debug("Debug mesaji")
logger.info("info mesaji")
logger.warning("warning mesaji")
logger.error("error mesaji")
logger.critical("kritik hata mesaji")


