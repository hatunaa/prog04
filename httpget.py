import socket
import sys
import html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Target url")
args = parser.parse_args()


def recvall(s):
    total_data = []
    response = s.recv(4096)
    while (len(response) > 0):
        total_data.append(response.decode())
        response = s.recv(4096)
    response = ''.join(total_data)
    return response


def getDomain(url):
    domain = ""
    if url[0:8] == "https://":
        for i in range(8, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    if url[0:7] == "http://":
        for i in range(7, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    return domain


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = args.url
domain = getDomain(url)
# print(domain)
client.connect((domain, 80))
request = "GET / HTTP/1.1\r\nHOST: "+domain+"\r\n\r\n"
client.send(request.encode())
response = recvall(client)
# print(response)
title = ""
for i in range(0, len(response)):
    if title != "":
        break
    if response[i:i+7] == "<title>":
        # print("yes")
        for j in range(i+7, len(response)):
            if response[j:j+8] == "</title>":
                title = response[i+7:j]
                break
#print("title", title)
print("title:", html.unescape(title))