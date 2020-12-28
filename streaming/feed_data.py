#!/usr/bin/python3

import os
import socket
import sys
import time

HOST = sys.argv[1]
PORT = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        with open('data','r') as f:
            for line in f:
                conn.sendall(line.encode('utf-8'))
                time.sleep(1)
