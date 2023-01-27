import socket
import json
import re


def dns(message):
    DNS_ip = socket.gethostbyname(socket.gethostname())                   # Get local ip automatically
    DNS_port = 5353                                                       # Reserve a port for DNS.
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    client.connect((DNS_ip,DNS_port))
    client.send(message.encode(Format))
    msg = client.recv(Header).decode(Format)
    if len(msg):
        msg = json.loads(msg)
        ip = msg['IP']
        port = msg['PORT']
        return ip,port                    
    client.close()


def http(url,ip):
    ip = socket.gethostbyname(socket.gethostname())                       # Get local ip automatically
    server_ip = ip                  
    server_port = 8080                                                    # Reserve a port for DNS.
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    client.connect((server_ip,server_port))
    message = Get(url)
    client.sendall(message.encode(Format))
    msg1 = client.recv(Header)
    if msg1:
        data = msg1.decode(Format)
        flag = validation(data)
        if flag == 1 :
            file = parse(data)
            msg2 = client.recv(Header)
            f = open(file,'wb')
            f.write(msg2)
            f.close()
            print(f"[Receive] File {file} received")
        else:
            print(f"File Not Found!!")       
    client.close()


def Get(url):
    domain = url.split("/")[0]
    path = url.split("/")[1]
    data = f"GET /{path}/ HTTP/1.1/\r\n"
    data += f"Host: {domain}/\r\n"
    data += "Connection: keep-alive"
    return data


def validation(msg):
    Pattern = '[A-Za-z\d._]+'
    a = re.findall(Pattern,msg)
    if a[2] == '200' :
        flag = 1
    else:
        flag = 0
    return flag


def parse(msg):
    Pattern = '[A-Za-z\d._]+'
    a = re.findall(Pattern,msg)
    file = a[9]
    domain = a[7]
    return file


################# Main #####################
Header = 1024
Format = "UTF-8"
Disconnect_message = "Disconnect"
Active = True
print("Commands:\n[ 1.dns  2.http  3.exit ]")
while Active:
    inp = input("ENTER Command--> ")
    command = inp.split()[0]       
    if command == "dns":
        url = inp.split()[1]
        (ip,port) = dns(url)
        if ip == "Noun":
            print("This URL's ip Doesn't exist in DNS") 
            continue
        else:   
            print(f"[Result] dns query result for {url} is {ip} with port {port}")

    elif command == "http":
        url = inp.split()[1]
        domain = url.split("/")[0]
        (ip,port) = dns(domain)
        print(f"[result] dns query result for {domain} is {ip} with port {port}")
        http(url,ip)         
    elif command == "exit":
        Active = False
    else:
        print("Coammand is Wrong. Try again..")



