import socket
import uuid

def thread_client(conn):
    




#https://docs.python.org/2/howto/sockets.html
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) #Ip4 en TCP
#bind the socket to a public host,
# and a well-known port

Port  = 4598


serversocket.bind((socket.gethostname(), Port))
#become a server socket
serversocket.listen(5)

while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    #now do something with the clientsocket
    #in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()
