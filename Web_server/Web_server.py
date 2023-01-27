import socket
import threading
import os
import re

def start():
    WEB_server.listen()
    print(f"[LISTENING] server is lestening on {WEB_ip}")
    while True:
        conn, addr = WEB_server.accept()
        thread1 = threading.Thread(target=handle_client, args=(conn,addr))
        thread1.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    Active = True
    while Active:
        msg = conn.recv(Header).decode(Format)
        if len(msg):
            if msg == "Disconnect":
                conn.close()
                Active = False 
            else:     
                status = validation(msg)
                if status == "valid":   
                    (domain,file) = parse(msg)
                    flag = check_File(domain,file)
                    (response,file_Byte) = build(domain,file,flag)
                    conn.sendall(response.encode(Format))
                    conn.sendall(file_Byte)
                else:
                    err = "Invalid Connection."
                    response = err.encode(Format)
                    conn.sendall(response)
                    Active = False 
        conn.close()
        Active = False



def validation(msg):
    Pattern = '[A-Za-z\d.]+'
    a = re.findall(Pattern,msg)
    # print(f"{a[0]}\n{a[4]}")
    if a[0] == 'GET' and a[4] == 'HTTP':
        status = "valid"
    else:
        status = "invalid" 
    return status


def parse(msg):
    Pattern = '[A-Za-z\d.]+'
    a = re.findall(Pattern,msg)
    file = a[3]
    domain = a[7]
    return domain,file


def check_File(domain,file):
    path = f"\Files\{domain}\\tests"
    files = os.listdir(path)
    if file in files:
        flag = 1
    else:
        flag = 0
    return flag


def build(domain,file,flag):
    if flag == 1:
        path = f"G:\\Uni\\term3\Communication_Networks\Projects\Project1\Web_server\Files\{domain}\\tests\\{file}"
        f = open(path,'rb')
        file_Byte = f.read(Header) 
        data = "HTTP/1.1 200 Ok\r\n"
        data += "Server: Web_server\r\n"
        data += f"Domain: {domain}\r\n"
        data += f"Content: {file}"
    else:
        data = "HTTP/1.1 404 NOT_FOUND\r\n"
        data += "Server: Web_server\r\n"
        data += f"Domain: {domain}\r\n"
        data += f"Content: {file}"
        file_Byte = 0
    return data,file_Byte


####################### Main #######################

WEB_ip = socket.gethostbyname(socket.gethostname())                   # Get local ip automatically
WEB_port = 8080                                                       # Reserve a port for DNS.
Header = 1024 
Format = "UTF-8"

WEB_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          # Create a socket object
WEB_server.bind((WEB_ip,WEB_port))

print("[Starting] server is starting...")
start()


