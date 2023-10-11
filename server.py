import socket
import threading

HOST = '127.0.0.1' #private ip address
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
#receive - new clients connecting

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with{str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        client.send("Joined the chat".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
#handle handles the connection
print("server running")
receive()
