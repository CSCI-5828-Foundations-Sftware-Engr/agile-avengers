import logging.config
import os

logging.config.fileConfig(
    fname=os.path.dirname(os.path.realpath(__file__)) + "/config/generic_log.conf", disable_existing_loggers=True,
)
logger = logging.getLogger(__name__)
