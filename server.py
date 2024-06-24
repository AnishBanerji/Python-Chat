import threading
import socket

host = socket.gethostbyname(socket.gethostname())
port = 55555
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while  True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break

def kick(nickname):
    try:
        idx = nicknames.index(nickname)
        client = clients[idx]

        client.send("You have been removed. GoodBye!".encode('ascii'))
        clients.remove(client)
        client.close()
        broadcast(f"{nickname} has been removed".encode('ascii'))
        nicknames.remove(nickname)
    except:
        print("")

def write():
    while True:
        try:
            message = input("")
            lr = message.split()
            print(lr)
            if lr[0] == 'remove' or lr[0]=='Remove' or lr[0]=='kick' or lr[0]=='Kick':
                lr.remove(lr[0])
                for nick in lr:
                    kick(nick)
                    print (f"{nick} has been kicked")
            
        except:
            print("")



def recieve():
    while True:
        client, address = server.accept()
        print (f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print (f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread_h = threading.Thread(target=handle,args=((client,)))
        thread_h.start()

        thread_w = threading.Thread(target=write)
        thread_w.start()


print("Server is listenning")
recieve()

