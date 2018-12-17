import socket
import random
from src.lib import *

users = []

#-------------------------------------------

def client_thread(conn, ip):
    username = read_connection(conn)
    find=False;
    for  x in users:
        if username == x.username:
            #find which client ask to authentificate
            user = x
            print(user.username+" ask for authentification "+ " pass "+user.password)
            find=True
            break
    if find:
        send_connection(conn,user.getNonce()) # send it to client the nonce as bytes
        hashReceive = read_connection(conn)

        if(user.check(hashReceive)) :
            send_connection(conn,"accept")
        else :
            send_connection(conn,"not accept")

        conn.close()  # close connection
        print('Connection ' + str(ip) + ':' + str(portNumber)+ " ended")
    else:
        send_connection(conn,"bad username")
        print('not find username')

def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created on')

    try:
        soc.bind((ipAuthentification, portNumber))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening on '+str(ipAuthentification))

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

def readUserFile():
    filename = "../config/users.txt"
    with open(filename) as f:
        lines= f.readlines()
    for line in lines:
        values = line.replace('\n','').split(" ")
        users.append(user(values[0],values[1]))

readUserFile()
start_server()
print('nonce '+str(users[0].getNonce()))
print('user '+str(users[0].username)+' pasword '+str(users[0].password)+' nonce '+str(users[0].nonce))