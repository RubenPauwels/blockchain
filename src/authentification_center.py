import socket
import random
from src.lib import *

users = []

#-------------------------------------------

def client_thread(conn, ip):
    input_text = read_connection(conn)
    username='ulrik'
    for  x in users:
        if username == x.username:
            user = x
            break

    send_connection(conn,user.getNonce())# send it to client
    hashReceive = read_connection(conn)
    if(user.check(hashReceive)) :
        send_connection("accept")
    else :
        send_connection("not accept")

    conn.close()  # close connection
    print('Connection ' + str(ip) + ':' + str(portNumber)+ " ended")


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
        values = line.split(" ")
        users.append(user(values[0],values[1]))

readUserFile()
start_server()
print('nonce '+str(users[0].getNonce()))
print('user '+str(users[0].username)+' pasword '+str(users[0].password)+' nonce '+str(users[0].nonce))