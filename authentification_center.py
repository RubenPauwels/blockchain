import _thread
import socket
import uuid

def client_thread(socket):
    data = s.recv(1024)
    if data:
        message_queues[s].put(data)
        if s not in outputs:
            outputs.append(s)
    else:
        if s in outputs:
            outputs.remove(s)
        inputs.remove(s)
        s.close()
        del message_queues[s]




#Homoooooo's

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
    _thread.start_new_thread(client_thread(clientsocket),())

