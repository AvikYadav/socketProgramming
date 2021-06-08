import threading
import socket
import time
nickname = input('nickname :')
client = socket.socket()
connect  = True
client.connect(('localhost',8888))
# room_ids_list = ][]
# def check(nickname):
#     if '&&' in str(nickname):
#         name, roomCreateCheck = nickname.split('&&')
#         if 'create' in roomCreateCheck:
#             dele, room_id_got = roomCreateCheck.split('create')
#             room_id_got = roomCreateCheck.strip()
#             room_ids_list.append(room_id_got)
#         else:
#             roomCreateCheck = roomCreateCheck.strip()
#             check = room_ids_check(False, roomCreateCheck)
#             if not check:
#                 c.send('hey user pls enter a valid room id to join chat using && after name'.encode('utf-8'))
#                 # c.close()
#                 closeConnection(c)
#                 break
#     else:
#         c.send('hey user pls enter a room id to join chat using && after name'.encode('utf-8'))
#         closeConnection(c)
#         break
def recieve():
    while True:
        try:
            #here is issue
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
            if message == '!DISCONNECT':
                connect = False
                client.send('DISCONNECTED'.encode('ascii'))
                time.sleep(5)
                client.close()
            if message == '!AUTHENCATED!':
                break
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
def write():
    name = nickname.split('&&')
    while True:
        message = '{}: {}'.format(name[0], input(' '))
        client.send(message.encode('ascii'))
recieve()
if connect:
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