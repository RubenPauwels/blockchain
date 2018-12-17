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