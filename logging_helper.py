# -*- coding:utf-8 -*-
# @Date: "2024-02-18"
# @Description: logging helper

import logging
import logging.handlers
import pathlib
import sys
import inspect


def setup_logging_file(filename):
    handler = logging.handlers.RotatingFileHandler(
        filename, maxBytes=10*1024*1024, backupCount=5)
    logging.basicConfig(
        handlers=[handler],
        level=logging.INFO
    )


def init_logging(log_file, log_level, **kwargs):
    pathObj = pathlib.Path(log_file).expanduser()
    if not pathObj.is_absolute():
        if getattr(sys, 'frozen', False):
            pathObj = pathlib.Path(sys.executable, pathObj)
        else:
            pathObj = pathlib.Path(
                inspect.stack()[1].filename).parent / pathObj
    logging.basicConfig(
        filename=pathObj.resolve(),
        encoding='utf-8',
        level=log_level,
        **kwargs)
