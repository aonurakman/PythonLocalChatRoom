import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "25.74.127.57"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    #print(client.recv(2048).decode(FORMAT))

def receive():
    while (connected):
        msg = client.recv(2048).decode(FORMAT)
        if msg:
            print(msg)
 
def start():
    thread = threading.Thread(target = receive, args = ())
    thread.start()
    

start()
while(True):
    msg = input()
    if msg == "e":
        msg = DISCONNECT_MESSAGE
        send(msg)
        connected = False
        break
    else:
        send(msg)