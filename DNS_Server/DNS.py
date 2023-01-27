import json 
import socket
import threading

def start():
    DNS_server.listen()
    print(f"[LISTENING] server is lestening on {DNS_ip}")
    while True:
        conn, addr = DNS_server.accept()
        thread1 = threading.Thread(target=handle_client, args=(conn,addr))
        thread1.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(Header).decode(Format)
        if len(msg):
            f = open('DNS_DATA.json')
            data = json.load(f)
            f.close()
            (ip,port) = extract_data(msg,data)
            DATA = {"IP":ip,"PORT":port}
            DATA = json.dumps(DATA)
            mseg_ip = DATA.encode(Format)
            conn.send(mseg_ip)
            conn.close()
            connected = False
            if msg == "Disconnect":
                conn.close()
                DNS_server.close()
                connected = False

def extract_data(msg,data):
    if msg == "network1.com":
        ip = data["root"]["domains"]["network1.com"]["ip"]
        port = data["root"]["domains"]["network1.com"]["port"]
        
    elif msg == "sub1.network1.com":
        ip = data["root"]["domains"]["network1.com"]["subdomains"]["sub1.network1.com"]["ip"]
        port = data["root"]["domains"]["network1.com"]["subdomains"]["sub1.network1.com"]["port"]

    elif msg == "sub2.network1.com":
        ip = data["root"]["domains"]["network1.com"]["subdomains"]["sub2.network1.com"]["ip"]
        port = data["root"]["domains"]["network1.com"]["subdomains"]["sub2.network1.com"]["port"]

    elif msg == "network2.com":
        ip = data["root"]["domains"]["network2.com"]["ip"]
        port = data["root"]["domains"]["network2.com"]["port"]

    elif msg == "sub1.network2.com":
        ip = data["root"]["domains"]["network2.com"]["subdomains"]["sub1.network2.com"]["ip"]
        port = data["root"]["domains"]["network2.com"]["subdomains"]["sub1.network2.com"]["port"]

    elif msg == "sub2.network2.com":
        ip = data["root"]["domains"]["network2.com"]["subdomains"]["sub2.network2.com"]["ip"]
        port = data["root"]["domains"]["network2.com"]["subdomains"]["sub2.network2.com"]["port"]
    else:
        ip = "Noun"
        port = "Noun"
    return ip,port



############ Main ##############
DNS_ip = socket.gethostbyname(socket.gethostname())                   # Get local ip automatically
DNS_port = 5353                                                       # Reserve a port for DNS.
Header = 1024 
Format = "UTF-8"

DNS_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          # Create a socket object
DNS_server.bind((DNS_ip,DNS_port))

print("[Starting] server is starting...")
start()


