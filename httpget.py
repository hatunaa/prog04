#!/usr/bin/env python3

import socket 
import argparse, re
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url",dest="target_host", help="url argument")
args = parser.parse_args()

HOST = args.target_host
PORT = 80


def recv_basic(the_socket):
    total_data=[]
    data = the_socket.recv(8192)
    while (len(data) > 0):
        # if not data: break
        total_data.append(data.decode())
        data = the_socket.recv(8192)
    data = ''.join(total_data)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    domain = urlparse(f'{HOST}').netloc
    #print(domain)

    # socket connect
    client.connect((domain,PORT))

    request = (f'GET / HTTP/1.1\r\nHost: {domain}\r\n\r\n')

    client.send(request.encode())
    response = recv_basic(client)
    # print(response)

    title = re.findall(r"<title>(.*)</title>", response)[0]
    print("Title: ", title[0:10])
