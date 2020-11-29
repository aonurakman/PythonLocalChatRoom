import socket

HEADER = 64
PORT = 5050 #? Boş portu bulmak
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.20.10.6"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("HELLO!!!") 
send("HELLOOOOOOOOOOOOO!!!")    
send(DISCONNECT_MESSAGE)