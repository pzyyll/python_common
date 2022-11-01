# -*- coding:utf-8 -*-

import os
import pathlib
import sys


class PathHelper(object):
    def __init__(self, exec_file=""):
        self.exec_path = "."
        self.exec_file = exec_file or __file__
        self._init()
    
    def _init(self):
        if getattr(sys, 'frozen', False):
            self.exec_path = pathlib.Path(sys.executable).parent.resolve()
        elif __file__:
            self.exec_path = pathlib.Path(self.exec_file).parent.resolve()

    def get_path(self, path):
        if pathlib.Path(path).is_absolute():
            return path
        return str(pathlib.PurePath(self.exec_path, path))

    def get_resource_path(self, path):
        if getattr(sys, '_MEIPASS', None):
            return str(pathlib.PurePath(sys._MEIPASS, path))
        return self.get_path(path)

    def get_cwd_path(self, path):
        if pathlib.Path(path).is_absolute():
            return path
        return str(pathlib.PurePath(os.getcwd(), path))

    def cd(self, path):
        path = self.get_path(path)
        os.chdir(path)

    def is_local_path(self, path):
        return os.path.exists(path)

    def rmdir(self, path):
        import stat
        import shutil
        def handle_remove_readonly(func, path, exc):
            if func in (os.rmdir, os.remove, os.unlink):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            else:
                raise

        path = self.get_path(path)

        if self.is_local_path(path):
            shutil.rmtree(path, onerror=handle_remove_readonly)

    def mkdir(self, path, parents=True, exist_ok=True):
        path = self.get_path(path)
        pathlib.Path(path).mkdir(parents=parents, exist_ok=exist_ok)

    def join_paths(self, *args):
        return str(pathlib.Path(*args).resolve())
