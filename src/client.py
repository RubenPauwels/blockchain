# client.py
from src.lib import send_connection
from src.lib import read_connection

import src.lib
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
iPaddresssServer = "127.0.0.2"
soc.connect((iPaddresssServer, src.lib.portNumber))


clients_input = input("What you want to proceed my dear client?\n") #read from terminal

send_connection(soc,clients_input) # we must encode the string to bytes

result_string = read_connection(soc)


print("Result from server is {}".format(result_string))
