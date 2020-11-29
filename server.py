import socket
import threading # farklı kodların aynı anda çalışması

HEADER = 64
PORT = 5050 #? Boş portu bulmak
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "172.20.10.6"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleClient(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}]: {msg}")
            conn.send("RECEIVED".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while (True):
        conn, addr = server.accept()
        thread = threading.Thread(target = handleClient, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")



print("[STARTING] server is starting...")
start()