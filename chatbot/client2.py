import threading
import socket
nickname = input('nickname :')
client = socket.socket()
client.connect(('localhost',8888))
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))
y = threading.Thread(target=recieve)
y.start()
x = threading.Thread(target=write)
x.start()
# inp = input('enter room number to connect :')
# client.send(bytes(inp,'utf-8'))
# clientConnectedTo = client.recv(1024).decode()
# while True:
#     inp = input('type text to chat :')
#     client.send(bytes(inp,'utf-8'))