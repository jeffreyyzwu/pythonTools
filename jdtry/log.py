import logging
import logging.config

logging.config.fileConfig("conf/logger.conf")
logger = logging.getLogger("jdtry")
