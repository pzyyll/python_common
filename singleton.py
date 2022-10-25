# -*- coding:utf-8 -*-
# @Date: "2022-10-25"
# @Description: "singleton"

class Singleton(object):
    """
    A generic base class to derive any singleton class from.
    addition:
        Borg pattern
        class Borg(object):
            _shared_state = {}
            def __init__(self):
                self.__dict__ = self._shared_state
                self.state = "Init"
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method, such that it is a singleton.
        """
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.__instance.__init__(*args, **kwargs)
        return cls.__instance

    @classmethod
    def is_inited(cls):
        return cls.__instance is not None
