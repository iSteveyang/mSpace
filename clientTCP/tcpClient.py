# -*- coding: UTF-8 -*-

import socket

client = socket.socket()

client.connect(('192.168.7.51', 9999))

while True:

    msg = input('>>:').strip()
    if not msg:
        continue
    else:
        client.send(msg.encode('utf-8'))
        upData = client.recv(1024)
        print(upData.decode())

