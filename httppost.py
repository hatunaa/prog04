#!/usr/bin/env python3

import socket 
import argparse, re
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url",dest="target_host", help="url target login")
parser.add_argument("--user",dest="username", help="user for login")
parser.add_argument("--password",dest="passwd", help="password for login")
parser.usage = parser.format_help()
args = parser.parse_args()

HOST = args.target_host
PORT = 80
user = args.username
password = args.passwd

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
    cookieList = ["wordpress_test_cookie=WP+Cookie+check"]
    
    body = f'log={user}&pwd={password}&wp-submit=Log+In'
    request = ( f'POST /wp-login.php HTTP/1.1\r\n'
                f'Host: {domain}\r\n'
                f'Content-Type: application/x-www-form-urlencoded\r\n'
                f'Accept: text/html,application/xhtml+xml,application/xml\r\n'
                f'Content-Length: {len(body)}\r\n'
                f'Connection: keep-alive\r\n\r\n'
                f'{body}\r\n'
    )

    client.send(request.encode())
    response = recv_basic(client)
    #print (response)
    
    cookie_response = re.findall(r"Set-Cookie: (wordpress_logged_in_.*?)\r\n", response)
    if cookie_response:
        print(f"User {user} đăng nhập thành công ")
    else:
        print(f"User {user} đăng nhập thất bại")
