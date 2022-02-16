#!/usr/bin/env python3

import socket 
import argparse, re
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url",dest="target_host", help="url argument")
args = parser.parse_args()

HOST = args.target_host
PORT = 80

def recvall(s):
    total_data = []
    response = s.recv(4096)
    while (len(response) > 0):
        total_data.append(response.decode())
        response = s.recv(4096)
    response = ''.join(total_data)
    return response

def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(8192)
        if not data: break
        total_data.append(data)
        reponse = b''.join(total_data)
    return reponse

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    domain = urlparse(f'{HOST}').netloc
    #print(domain)

    # socket connect
    client.connect((domain,PORT))

    request = (f'GET / HTTP/1.1\r\nHost: {domain}\r\n\r\n')

    client.send(request.encode())
    response = recvall(client)
    # print(response)

    title = re.findall(r"<title>(.*)</title>", response)[0]
    print("Title: ", title[0:10])
