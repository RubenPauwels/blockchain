import socket
import random
from src.lib import *

users = []

#-------------------------------------------------------
class user():
    def __init__(self,userName,password):
        self.username=userName
        self.password=password
        self.nonce = 0

    def getNonce(self):
        self.nonce =random.getrandbits(80)
        return self.nonce

    def check(self, hash):
        return hash == hash(str(self.password)+str(self.nonce))

#-------------------------------------------

def client_thread(conn, ip):
    input_text = read_connection(conn)
    username='test'


    send_connection(conn,"send back same from server:"+input_text)# send it to client
    conn.close()  # close connection
    print('Connection ' + str(ip) + ':' + str(portNumber)+ " ended")


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created on')

    ipaddress = "127.0.0.2"
    try:
        soc.bind((ipaddress, portNumber))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening on '+str(ipaddress))

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
print('nonce '+str(users[0].getNonce()))
print('user '+str(users[0].username)+' pasword '+str(users[0].password)+' nonce '+str(users[0].nonce))