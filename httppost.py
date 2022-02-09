import socket
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Target url")
parser.add_argument("--username", help="Username")
parser.add_argument("--password", help="Password")
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
username = args.username
password = args.password
domain = getDomain(url)
# print(domain)
client.connect((domain, 80))
body = "log="+username+"&pwd="+password+"&wp-submit=Log+In"
request = "POST /wp-login.php HTTP/1.1\r\n"+"HOST: "+domain + "\r\n"+"Content-Length: "+str(len(body))+"\r\n"+"Content-Type: application/x-www-form-urlencoded"+"\r\n"+"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"+"\r\n"+"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"+"\r\n" + "Cookie: wordpress_test_cookie=WP Cookie check; wp_lang=en_US"+"\r\n" \
    "\r\n"+body
# print(request)
client.send(request.encode())
response = recvall(client)
# print(response)
if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
    print("User "+username+" dang nhap thanh cong.")
else:
    print("User "+username+" dang nhap that bai.")