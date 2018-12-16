# client.py
from src.lib import send_connection
from src.lib import *

import src.lib
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect((ipAuthentification, src.lib.portNumber))
user = user('user1' , 'unicorn')


send_connection(soc,user.username)  #send username to auth center
nonce = read_connection(soc)    #receive nonce
send_connection(soc,user.setNonce(nonce))   #send back hash

answer = read_connection(soc)
print(answer)

soc.close();


print("Result from server is {}".format(result_string))
