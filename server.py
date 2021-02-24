#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def recv_info(ip, port):
    sock = socket.socket()
    sock.bind(('', int(port)))
    sock.listen(2)
    while 1:
        fst_conn, fst_addr = sock.accept()
        scnd_conn, scnd_addr = sock.accept()
        fst_data = fst_conn.recv(1024)
        scnd_data = scnd_conn.recv(1024)
        fst_conn.send(scnd_data)
        scnd_conn.send(fst_data)


if __name__ == '__main__':
    recv_info('194.67.91.122', '7777')
