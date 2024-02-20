# -*- coding:utf-8 -*-
# @Date: "2024-02-19"
# @Description: 
# 简单的封装设置代理
# 通过上下文管理来管理代理，使用到了 socks ，需要 pip install pysocks
# with Proxy('socks5://127.0.0.1:1080'):
#     # do something
#     pass

import socket
import socks


class Proxy(object):
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self._tmp_socket = None
        if proxy:
            self.proto, self.ip, self.port = self._parse_proxy_str(proxy)

    def _parse_proxy_str(self, proxy_str):
        import re
        pattern = r'((?P<proto>\w+)://)?(?P<ip>[^\s:]+)(:(?P<port>\d+))?'
        match = re.match(pattern, proxy_str)
        if not match:
            raise ValueError(f'Invalid proxy: {proxy_str}')
        
        proto = match.group('proto') or 'http'  # 提供默认协议
        ip = match.group('ip')
        port_str = match.group('port')
        
        # 尝试将端口转换为整数，如果未提供端口，则设置默认端口
        try:
            port = int(port_str) if port_str is not None else 8080
        except ValueError:
            raise ValueError(f'Invalid port number: {port_str} in proxy: {proxy_str}')
        
        return proto.upper(), ip, port

    def set_proxy(self):
        if not self.proxy:
            return
        if self.proto in socks.PROXY_TYPES:
            socks.set_default_proxy(socks.PROXY_TYPES[self.proto], self.ip, self.port)
            self._tmp_socket = socket.socket  # 保存原始socket构造器
            socket.socket = socks.socksocket  # 设置新的socket构造器以使用代理
        else:
            raise ValueError(f'Unsupported proxy protocol: {self.proto}')

    def reset_proxy(self):
        if self._tmp_socket:
            socket.socket = self._tmp_socket
            self._tmp_socket = None 

    def __enter__(self):
        self.set_proxy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_proxy()
