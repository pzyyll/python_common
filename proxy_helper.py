# -*- coding:utf-8 -*-
# @Date: "2024-02-19"
# @Description: 
# 简单的封装设置代理，注意修改的是全局的socket.socket，所以在多线程环境下要注意
# 通过上下文管理来管理代理，使用到了 socks ，需要 pip install pysocks
# with Proxy('socks5://127.0.0.1:1080'):
#     # do something
#     pass

import socket
import socks
import logging
import threading
from concurrent.futures import ProcessPoolExecutor


thread_local = threading.local()


def get_proxy_stack():
    if not hasattr(thread_local, 'proxy_stack'):
        thread_local.proxy_stack = []
    return thread_local.proxy_stack


class Proxy(object):
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self.proto = None
        self.ip = None
        self.port = None
        if proxy:
            try:
                self.proto, self.ip, self.port = self._parse_proxy_str(proxy)
            except ValueError as exc:
                logging.error(exc)
                self.proto = self.ip = self.port = None

    def _parse_proxy_str(self, proxy_str):
        import re
        pattern = r'((?P<proto>\w+)://)?(?P<ip>[^\s:]+)(:(?P<port>\d+))?'
        match = re.match(pattern, proxy_str)
        if not match:
            raise ValueError(f'Invalid proxy format: {proxy_str}')
        
        proto = match.group('proto') or 'http'  # 提供默认协议
        ip = match.group('ip')
        port_str = match.group('port')
        
        # 设置默认端口
        port = 8080
        if port_str is not None:
            try:
                port = int(port_str)
            except ValueError as exc:
                raise ValueError(f'Invalid port number: {port_str} in proxy: {proxy_str}') from exc
        
        return proto.upper(), ip, port

    def is_valid(self):
        return self.proto and self.ip and self.port and self.proto in socks.PROXY_TYPES

    def set_proxy(self):
        if self.is_valid():
            socks.set_default_proxy(socks.PROXY_TYPES[self.proto], self.ip, self.port)
            get_proxy_stack().append(socket.socket)
            logging.debug(f'Setting proxy: {id(self)},{self.proxy},cur={socket.socket}')
            socket.socket = socks.socksocket  # 设置新的socket构造器以使用代理

    def reset_proxy(self):
        if self.is_valid():
            org_socket = get_proxy_stack().pop() #恢复原始socket构造器
            logging.debug(f'Resetting proxy: {id(self)},{self.proxy},cur={socket.socket},org={org_socket}')
            socket.socket = org_socket

    def __enter__(self):
        self.set_proxy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_proxy()


class ProxyWorkerPoolManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self.process_pools = []

    def add_process_pool(self, max_workers=1, *args, **kwargs):
        process_pool = ProcessPoolExecutor(max_workers=max_workers, *args, **kwargs)
        self.process_pools.append(process_pool)
        return process_pool

    def shutdown(self, wait=True):
        for process_pool in self.process_pools:
            process_pool.shutdown(wait=wait)
        self.process_pools = []


class ProxyWorkerPool(object):
    '''Proxy worker pool
    利用ProcessPoolExecutor来实现将需要代理的访问放在进程中进行
    '''
    def __init__(self, max_workers=1):
        self.proxy = None
        self.worker = None
        self.proxy_class_info = None
        self.worker = ProxyWorkerPoolManager().add_process_pool(max_workers=max_workers)

    def set_proxy_info(self, proxy, proxy_cls, *proxy_cls_args, **proxy_cls_kwargs):
        '''Set proxy info
        proxy: 代理地址
        proxy_cls, proxy_cls_args, proxy_cls_kwargs: 需要进行代理的类信息，将实例化延迟到子进程中
        '''
        self.proxy = proxy
        self.proxy_class_info = (proxy_cls, proxy_cls_args, proxy_cls_kwargs)

    @classmethod
    def run_func(cls, proxy, proxy_cls_info, func, *args, **kwargs):
        if not proxy_cls_info:
            raise ValueError('Invalid class info.')
        proxy_cls = proxy_cls_info[0]
        if not proxy_cls:
            raise ValueError('Invalid class.')
        try:
            proxy_instance = proxy_cls(*proxy_cls_info[1], **proxy_cls_info[2])
        except Exception as e:
            raise ValueError(f'Failed to create class instance: {e}') from e
        with Proxy(proxy):
            return getattr(proxy_instance, func)(*args, **kwargs)

    def submit(self, func, *args, **kwargs):
        return self.worker.submit(self.run_func, self.proxy, self.proxy_class_info, func, *args, **kwargs)
