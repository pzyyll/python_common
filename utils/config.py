# -*- coding:utf-8 -*-
# @Date: "2022-10-26"
# @Description: config helper

import json


def load_config(file):
    with open(file, "r") as f:
        return json.load(f)
