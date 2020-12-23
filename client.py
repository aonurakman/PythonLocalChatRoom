import socket
import threading
import time

HEADER = 64 # Header, gonderilecek veri hakkında onceden server'i bilgilendirmek icin. Header icin fixed 64 byte boyut belirledim.
PORT = 8000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" # Server'dan kopmadan once server'a gonderilecek mesaj
SERVER = "192.168.0.21" #Server IP
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Client tanımlaması, socket() icindeki protokoller ile protokol belirleniyor
client.connect(ADDR) 

connected = True # Baglı oldugumuz surece True kalacak degisken

def send(msg): # Server'a mesaj gonderen fonksiyon
    message = msg.encode(FORMAT)
    msgLength = len(message) # Once mesajın boyutunun belirtileceigin soylemistim
    sendLength = str(msgLength).encode(FORMAT)
    sendLength = (b' ' * (HEADER - len(sendLength))) + sendLength  # Header 64 byte, 64'e tamamlamak icin boslukları dlduruyorum
    client.send(sendLength) # Once header, yani mesajın uzunlugunu gonder, bunun icin server onay mesajı dondurmeyecek
    client.send(message) # Mesajı gonderiyoruz


def receive(): # Surekli server dinlensin diye olusturulmus fonk.
    while (connected): # Baglı oldugumuz surece
        msgLength = client.recv(HEADER).decode(FORMAT)
        if msgLength: # Boyle bir header bilgisi geldiyse, mesaj da gelecek demektir
                msgLength = int(msgLength) 
                msg = client.recv(msgLength).decode(FORMAT) # mesaji al
                print(msg) # Ekrana yazdir
 
def start(): # Baslangıcta serverı surekli dinlemek icin thread olusturup receive()'e bagladim
    receiveThread = threading.Thread(target = receive, args = ()) 
    receiveThread.start()
    

start()
while(True): #Surekli kullanıcıdan input bekle
    msg = input()
    if msg == "e": # e karakterini disconnect olmak icin bir kod olacak sekilde ayarladım. e girilirse serverdan kop
        msg = DISCONNECT_MESSAGE
        send(msg)
        connected = False # Koptuk
        break
    else:
        send(msg) # Eger input e degilse, mesajdir. Gonder