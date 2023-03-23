import datetime
import logging
import os
import random
import string
import sys

from config.constants import PATH_DETAILS

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


file_name = "{}_{}".format(randomString(), datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))


logger = logging.getLogger(__name__)
logger_format = "%(asctime)s - %(filename)s - %(funcName)s() - line:%(lineno)s - %(levelname)s - %(message)s"
logger.propagate = False


def set_file_name(new_file_name):
    global file_name
    file_name = new_file_name
    logger.handlers = []
    # if not logger.handlers:
    logger.setLevel(logging.INFO)

    file_location = "{}/{}".format(PATH_DETAILS["LOG_FOLDER"], new_file_name)
    # create a file handler
    handler = logging.FileHandler(file_location)
    # handler = logging.StreamHandler()

    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(logger_format)
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.propagate = False
