import socket
import threading
sever = socket.socket()
sever.bind(('localhost',8888))
sever.listen()
room_ids_list = []
clients = []
nicknames = []
connect = False
print('waiting for connections')
def broadcast(message):
    for i in clients:
        print(i)
        i.send(message)
def room_ids_check(create:bool,roomid):
    if create == True:
        room_ids_list.append(roomid)
        print(room_ids_list)
        return True
    else:
        if int(roomid) in room_ids_list:
            return True
        return False
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
def closeConnection(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
def recieve():
    try:
        while True:
            c,addr = sever.accept()
            c.send('NICK'.encode('ascii'))
            clients.append(c)
            connect = True
            nickname = c.recv(4026).decode('ascii')
            print(nickname)
            if '&&' in str(nickname):
                name , roomCreateCheck = nickname.split('&&')
                print(name,roomCreateCheck)
                if 'create' in roomCreateCheck:
                    room_id_got = roomCreateCheck.replace('create','')
                    print(room_id_got)
                    room_id_got = room_id_got.replace(' ','')
                    print(room_id_got)
                    room_ids_check(True,int(room_id_got))
                    nickname = name
                else:
                    roomCreateCheck = roomCreateCheck.strip()
                    check = room_ids_check(False,roomCreateCheck)
                    print(room_ids_list)
                    print(check)
                    nickname = name
                    if not check:
                        c.send('!DISCONNECT'.encode('ascii'))
                        msg = c.recv(4026).decode('ascii')
                        if str(msg) == 'DISCONNECTED':
                            closeConnection(c)
                            connect = False
                        # c.close()
            else:
                c.send('!DISCONNECT'.encode('ascii'))
                msg = c.recv(4026).decode('ascii')
                if str(msg) == 'DISCONNECTED':
                    closeConnection(c)
                    connect = False
            if connect:
                nicknames.append(nickname)
                broadcast("{} joined!".format(nickname).encode('ascii'))
                c.send('!AUTHENCATED!'.encode('ascii'))
                print('client connected', addr)
                thread = threading.Thread(target=handle, args=(c,))
                thread.start()
    except Exception as err:
        print(err)
        closeConnection(c)
        # c.sendall(bytes('waiting for the other client to connect','utf-8'))
recieve()
