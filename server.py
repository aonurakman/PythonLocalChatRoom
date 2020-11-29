import socket
import threading # farklı kodların aynı anda çalışması

HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "25.74.127.57"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
conns = []

def postClients(conn, addr, msg):
    message = f"[{addr}] says: {msg}"
    for x in range (len(clients)):
        if conns[x] != conn:
            conns[x].send(message.encode(FORMAT))

def handleClient(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} connected.")
    clients.append(addr)
    conns.append(conn)
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conns.remove(conn)
                clients.remove(addr)
            else:
                postClients(conn, addr, msg)
            print(f"[{addr}]: {msg}")
            conn.send("SERVER RECEIVED YOUR MESSAGE".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while (True):
        conn, addr = server.accept()
        thread = threading.Thread(target = handleClient, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(conns)}")



print("[STARTING] server is starting...")
start()