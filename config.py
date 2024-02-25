# -*- coding:utf-8 -*-
# @Date: "2022-10-26"
# @Description: config helper

import json


class Config(object):
    @staticmethod
    def load(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def __init__(self, config_file):
        self.data = self.load(config_file)
        self.config_file = config_file

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __repr__(self):
        return f"<Config {self.config_file}>"