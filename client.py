#!/usr/bin/env python
# -*- coding: utf-8 -*-

# simply calling server
import socket


def call(ip, port, to_send):
    sock = socket.socket()
    sock.connect((str(ip), int(port)))
    sock.send(str(to_send).encode('utf-8'))

    data = sock.recv(1024)
    sock.close()
    return data


# getting public ip-port info
import stun


def get_ip_info():
    type_nat, ip, port = stun.get_ip_info()
    return (ip, port)


# main send functionality
import json


def send_p2p():
    to_send = json.dumps(list(get_ip_info())).encode('utf-8')
    serv_recv = call('194.67.91.122', '7777', to_send)

    data_recv = json.loads(serv_recv.decode('urf-8'))

    print(call(data_recv[0], data_recv[1], 'hello from vlad_pc'))


def recv_p2p():
    sock = socket.socket()
    sock.bind(get_ip_info())
    sock.listen(1)
    while 1:
        conn, addr = sock.accept()
        data = conn.recv(2048)
        print(data)
