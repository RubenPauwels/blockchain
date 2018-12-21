import socket
import random
from src.lib import *

users = []


def client_thread(conn, ip):
    try:
        #get username of node that wants to authentificate
        username = read_connection(conn)

        #initialise value
        find=False;

        #iterate over all users to find corrspondig User in our database
        for  x in users:
            if username == x.username:
                #find which client ask to authentificate
                user = x

                #we find someone
                find=True
                break

        #if we find the user
        if find:
            # send to the node a nonce
            send_connection(conn, user.generateNewNonce())

            #receive back the hash
            hashReceive = read_connection(conn)

            #the hash is good
            if(user.check(hashReceive)) :
                #sent to the user that he is authentificate
                send_connection(conn, conversation.accepted.value)

            #the hash is NOT good
            else :
                # sent to the user that he is NOT authentificate
                send_connection(conn, conversation.notAccepted.value)

        #there is no one with that username in our database
        else:
            send_connection(conn, "bad username")
            print('['+conn.getpeername()[0]+']','not find username')
    finally:
        #conversation ended
        print('[' + conn.getpeername()[0] + ']', 'Connection ' + str(ip) + ':' + str(portNumber) + " ended")
        conn.close() # close connection

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
        newUser = user(values[0])
        newUser.setHashSaltedPassword(values[1])
        users.append(newUser)

readUserFile()
start_server()
print('nonce ' + str(users[0].generateNewNonce()))
print('user '+str(users[0].username)+' pasword '+str(users[0].password)+' nonce '+str(users[0].nonce))