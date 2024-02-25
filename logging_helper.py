# -*- coding:utf-8 -*-
# @Date: "2024-02-18"
# @Description: logging helper

import logging
import pathlib
import sys
import inspect


def init_logging(log_file, log_level, **kwargs):
    pathObj = pathlib.Path(log_file).expanduser()
    if not pathObj.is_absolute():
        if getattr(sys, 'frozen', False):
            pathObj = pathlib.Path(sys.executable, pathObj)
        else:
            pathObj = pathlib.Path(inspect.stack()[1].filename).parent / pathObj
    logging.basicConfig(
        filename=pathObj.resolve(), 
        encoding='utf-8', 
        level=log_level, 
        **kwargs)



