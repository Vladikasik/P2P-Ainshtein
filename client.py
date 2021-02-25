#!/usr/bin/env python
# -*- coding: utf-8 -*-

# simply calling server
import socket


def call(ip, port, to_send):
    sock = socket.socket()
    print(f'connecting to {(str(ip), int(port))}')
    sock.connect((str(ip), int(port)))
    print('succesfully connected')
    sock.send(str(to_send).encode('utf-8'))
    print('data sent')
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
    print(to_send)
    serv_recv = call('194.67.91.122', '7777', to_send).decode('utf-8')[2:-1]
    print(serv_recv)
    data_recv = json.loads(serv_recv)

    print(call(data_recv[0], data_recv[1], 'hello from vlad_pc'))


def recv_p2p():
    ip_info = get_ip_info()
    print(f'your info {ip_info}')
    to_send = json.dumps(list(ip_info)).encode('utf-8')
    serv_recv = call('194.67.91.122', '7777', to_send)
    print(f'serv recv = {serv_recv}')
    sock = socket.socket()
    sock.bind(("", ip_info[1]))
    print(f'secket binded to {("", ip_info[1])}, waiting')
    sock.listen(1)
    print('socket listening at the moment')
    while 1:
        print('entered while 1')
        conn, addr = sock.accept()
        print('new connection')
        data = conn.recv(2048)
        print(data)
        conn.send(data.upper())


send_p2p()
