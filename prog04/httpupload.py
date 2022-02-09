import socket
import sys
import string
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Target url")
parser.add_argument("--username", help="Username")
parser.add_argument("--password", help="Password")
parser.add_argument("--localfile", help="path local file to upload")
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


def getCookies(response):
    cookies = []
    stringSplit = response.split("\r\n")
    for i in stringSplit:
        if "Set-Cookie: " in i:
            cookies.append(i.split(";")[0].split(":")[1].strip())
    return ";".join(cookies)


def getWpNonce(cookies, domain):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, 80))
    valid = string.ascii_lowercase+string.digits
    # print(valid)
    request = "GET /wp-admin/upload.php HTTP/1.1\r\n" + \
        "Host: "+domain+"\r\n"+"Cookie: "+cookies+"\r\n\r\n"
    # print(request)
    client.send(request.encode())
    response = recvall(client)
    #print("response", response)
    result = ""
    for i in range(0, len(response)):
        if result != "":
            break
        if response[i:i+12] == "\"_wpnonce\":\"":
            for j in range(i+12, len(response)):
                if(response[j] not in valid):
                    break
                result += response[j]
    client.close()
    return result


def uploadImage(cookies, domain, fileName, pathLocalFile):
    data = open(pathLocalFile, 'rb').read()
    # print(len(data))
    test = ""
    for i in data:
        test += chr(i)
    # print(test)
    wpnonce = getWpNonce(cookies, domain)
    contentType = fileName.split(".")[-1]
    contentType = "jpeg"
    # print(wpnonce)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, 80))
    body = "------WebKitFormBoundary"+"\r\n"+"Content-Disposition: form-data; name=\"name\"" + \
        "\r\n\r\n"+fileName+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
        "Content-Disposition: form-data; name=\"action\"" + \
        "\r\n\r\n"+"upload-attachment"+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
        "Content-Disposition: form-data; name=\"_wpnonce\""+"\r\n\r\n"+wpnonce+"\r\n"+"------WebKitFormBoundary" + \
        "\r\n"+"Content-Disposition: form-data; name=\"async-upload\"; filename=\"" + \
        fileName+"\""+"\r\n"+"Content-Type: image/"+contentType+"\r\n\r\n"
    body = body.encode()+data+b"\r\n"+b"------WebKitFormBoundary--"
    lenBody = str(len(body))
    request = "POST /wp-admin/async-upload.php HTTP/1.1\r\n"+"Host: "+domain+"\r\n"+"Cookie: " + \
        cookies+"\r\n"+"Connection: keep-alive\r\n"+"Content-Type: multipart/form-data; boundary=----WebKitFormBoundary" + \
        "\r\n"+"Content-Length: "+lenBody+"\r\n"+"\r\n"
    # print(request.encode()+body)
    client.send(request.encode()+body)
    response = recvall(client)
    # print(response)
    if "HTTP/1.1 200 OK" in response and "{\"success\":true" in response:
        print("Upload success.")
        path_url = ""
        for i in range(0, len(response)):
            if(path_url != ""):
                break
            if response[i:i+7] == "\"url\":\"":
                # print("yes")
                for j in range(i+7, len(response)):
                    if(response[j] == "\""):
                        break
                    path_url += response[j]
        path_url = path_url.replace('\\', '')
        print("File upload url:"+path_url)
    else:
        print("Upload fail.")
    return


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = args.url
username = args.username
password = args.password
pathLocalFile = args.localfile
domain = getDomain(url)
# print(domain)
fileName = pathLocalFile.split("/")[-1]
client.connect((domain, 80))
body = "log="+username+"&pwd="+password+"&wp-submit=Log+In"
request = "POST /wp-login.php HTTP/1.1\r\n"+"HOST: "+domain + "\r\n"+"Content-Length: "+str(len(body))+"\r\n"+"Content-Type: application/x-www-form-urlencoded"+"\r\n"+"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"+"\r\n"+"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"+"\r\n" + "Cookie: wordpress_test_cookie=WP Cookie check; wp_lang=en_US"+"\r\n" \
    "\r\n"+body
# print(request)
client.send(request.encode())
response = recvall(client)
# print(response)
if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
    #print("User "+username+" dang nhap thanh cong.")
    cookies = getCookies(response)
    uploadImage(cookies, domain, fileName, pathLocalFile)
    # print(cookies)
else:
    print("User "+username+" dang nhap that bai.")
    exit(0)