#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def call_server(ip, port, to_send):
    sock = socket.socket()
    sock.connect((str(ip), int(port)))
    sock.send(str(to_send).encode('utf-8'))

    data = sock.recv(1024)
    sock.close()
    return data


print(call_server('194.67.91.122', '7777', 'hello 2st'))
