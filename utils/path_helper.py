# -*- coding:utf-8 -*-

import os
import pathlib
import sys
import inspect


class PathHelper(object):
    def __init__(self, exec_file=""):
        # 入口执行文件的路径，打包后为可执行文件exe所在的路径
        self.exec_path = "."  
        # 资源路径，未打包与exec_path一样，打包后通常是一个临时资源的路径，用来读取资源文件
        self.resource_path = "."   
        self.set_exec_file(exec_file or inspect.stack()[1].filename)

    def set_exec_file(self, exec_file=""):
        self.exec_file = exec_file or inspect.stack()[1].filename
        self.resource_path = pathlib.Path(self.exec_file).parent.resolve()
        self.exec_path = (pathlib.Path(sys.executable).parent.resolve()
                          if getattr(sys, 'frozen', False)
                          else self.resource_path)

    def get_path(self, path):
        return self.get_exec_path(path)

    def get_exec_path(self, path):
        '''获取执行文件的路径，打包后是exe的路径'''
        pathObj = pathlib.Path(path).expanduser()
        if pathObj.is_absolute():
            return str(pathObj)
        return str(pathlib.Path(self.exec_path, pathObj).resolve())

    def get_resource_path(self, path):
        '''获取资源文件的路径，打包后是一个临时资源的路径'''
        # import logging
        # logging.debug("path: %s", path)
        # logging.debug("resource_path: %s", self.resource_path)
        # logging.debug(f"hehe{getattr(sys, '_MEIPASS', 'no')}")
        pathObj = pathlib.Path(path).expanduser()
        if pathObj.is_absolute():
            return str(pathObj)
        return str(pathlib.Path(self.resource_path, pathObj).resolve())

    def get_cwd_path(self, path):
        if pathlib.Path(path).is_absolute():
            return path
        return str(pathlib.Path(os.getcwd(), path).resolve())

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
