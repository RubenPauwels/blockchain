# client.py

from src.lib import *

import socket

def idetification():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    soc.connect((ipAuthentification, portNumber))
    thisUser = user('user1', 'unicorn', None)


    send_connection(soc, thisUser.username)  #send username to auth center
    nonce = read_connection(soc)  #receive nonce
    send_connection(soc, thisUser.setNonce(nonce))  #send back hash

    answer = read_connection(soc)
    print(answer)

    soc.close();
    return answer=="accept"

idetification()