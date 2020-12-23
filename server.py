import socket
import threading # farklı kodların aynı anda çalışması
import time

HEADER = 64 # Fixed header boyutu. Detaylar icin client.py'a bak.
PORT = 8000
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.21"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Protokol TCP
server.bind(ADDR)

conns = [] # Bagli clientlarin connlari
addrs = []

def postClients(addr, msg): # Gelen mesajı, gonderen haric diger clientlara gonderen fonk.
    message = f"[{addr}] says: {msg}" # Gonderilecek mesajın olusturulmasi
    for i in range (len(addrs)-1): # Her client icin
        if addrs[i] != addr: # Client = Gonderen degilse
            try:
                respondToClient(conns[i],message)
            except:
                print("ERROR 2")

def handleClient(conn, addr): # Her bagli client icin ayri ayri thread ile calisan fonk
    conns.append(conn)
    addrs.append(addr)
    print(f"\n[NEW CONNECTION] {addr} connected.")
    print(f"[ACTIVE CONNECTIONS] {len(conns)}")
    postClients(addr, "[CONNECTED]")
    connected = True 
    try:
        while connected: # Connected oldugu surece
            msgLength = conn.recv(HEADER).decode(FORMAT) # Oncelikle mesajin uzunlugunu al
            if msgLength: # Boyle bir header bilgisi geldiyse, mesaj da gelecek demektir
                msgLength = int(msgLength) 
                msg = conn.recv(msgLength).decode(FORMAT) # mesaji al
                if msg and msg == DISCONNECT_MESSAGE: #mesaji aldiysan ve disconnect mesajiysa...
                    print(f"Message: [{addr}]: {msg}")
                    connected = False
                    conns.remove(conn)
                    addrs.remove(addr)
                    print(f"\n[CLIENT DISCONNECT] {addr} disconnected.")
                    print(f"[ACTIVE CONNECTIONS] {len(conns)}")
                    postClients(addr, "[DISCONNECTED]") # Client koptu
                elif msg: # Ama normal mesajsa diger client'lara gonder
                    postClients(addr, msg)
                    print(f"Message: [{addr}]: {msg}")
                    respondToClient(conn, "RCVD") # Alinan her mesaj icin, gonderene onay mesajı gonder
        conn.close() # While'dan ciktiysak client kopmustur, baglantiyi kapat
    except:
        print("ERROR")

def respondToClient(conn, msg):
    message = msg + '\n'
    message = message + ( ' ' * (HEADER - len(message)))
    conn.send(message.encode(FORMAT))

def sendEmptyPackages(conn):
    while (conn in conns):
        time.sleep(0.5)
        try:
            respondToClient(conn, "")
        except:
            continue

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while (True):
        conn, addr = server.accept() # Baglanmak isteyen varsa bilgilerini al
        thread = threading.Thread(target = handleClient, args = (conn, addr)) # Hepsi icin thread calistir
        thread2 = threading.Thread(target = sendEmptyPackages, args = (conn,))
        thread.start()
        thread2.start()

print("[STARTING] server is starting...")
start()













    #message = message.encode(FORMAT)
    #msgLength = len(message) # Once mesajın boyutunun belirtileceigin soylemistim
    #sendLength = str(msgLength) + '\n'
    #sendLength = sendLength +(' ' * (HEADER - len(sendLength))) # Header 64 byte, 64'e tamamlamak icin boslukları dlduruyorum
    #conn.send(sendLength.encode(FORMAT)) # Once header, yani mesajın uzunlugunu gonder, bunun icin server onay mesajı dondurmeyecek