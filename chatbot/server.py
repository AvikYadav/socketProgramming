import socket
import threading
sever = socket.socket()
sever.bind(('localhost',8888))
sever.listen()
clients = []
nicknames = []
print('waiting for connections')
def broadcast(message):
    for i in clients:
        i.send(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
def recieve():
    while True:
        c,addr = sever.accept()
        c.send('NICK'.encode('ascii'))
        clients.append(c)
        nickname = c.recv(4026).decode('ascii')
        nicknames.append(nickname)
        broadcast("{} joined!".format(nickname).encode('ascii'))
        print('client connected', addr)
        thread = threading.Thread(target=handle,args=(c,))
        thread.start()
        # c.sendall(bytes('waiting for the other client to connect','utf-8'))
recieve()
