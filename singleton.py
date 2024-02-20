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
            # note: __init__ will be called by default, no need to manually call
            # cls.__instance.__init__(*args, **kwargs)
            cls.__instance.init(*args, **kwargs)
        return cls.__instance

    @classmethod
    def is_inited(cls):
        return cls.__instance is not None

    def init(self, *args, **kwargs):
        """
        Override this method to provide initialization.
        """
        pass


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def singleton(cls):
    """
    A decorator to make a class a singleton.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
