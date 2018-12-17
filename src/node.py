
from src.lib import *
import socket
# for handling task in separate jobs we need threading
from threading import Thread


NUMBER_NODE_temp = input("What client do you want to be?\n") #read from terminal
NUMBER_NODE=int(NUMBER_NODE_temp)

#-----------------------------------------
def authentification():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    soc.connect((ipAuthentification, portNumber))
    thisUser = readUser(NUMBER_NODE)

    send_connection(soc,thisUser.username)  #send username to auth center
    nonce = read_connection(soc)    #receive nonce
    send_connection(soc,thisUser.setNonce(nonce))   #send back hash

    answer = read_connection(soc)
    print(answer)

    soc.close();
    return answer=="accept"


b = blockchain()

def start_conversation_client(i, conversationEnumValue):
    # open socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = Ip4, STREAM = TCP

    # open the socket
    iPaddresssServer = i
    soc.connect((iPaddresssServer, portNumber))#ip4 and tcp
    send_connection(soc, conversationEnumValue)#send kind of conversation
    return soc

def sendBlocksEoAll():
    #asking last index to neighbours
    #for not sending the same block 2 times
    list=readIp_neighbors(NUMBER_NODE)
    string = "127.0.1.1"
    sendBlock(string)
    #Thread(target=sendBlock, args=(string)).start()
    for i in range(len(list)):
        print(list[i])
        if list[i]==string:
            print('match: '+i)
        #Thread(target=sendBlock, args=str(list[i])).start()

def sendBlock(string):
    print(string)
    soc =start_conversation_client(string, conversation.sendBLock._value_)

    #what received
    result_string = read_connection(soc)
    content = result_string.split('/')

    #get last 4 chars of current last block
    tempp= b.get_lastblock().hash
    last4ofhashblockchain=tempp[-4:]

    if int(content[0])==b.get_lastblock().index and last4ofhashblockchain==content[1]:
        tosend = conversation.ipToDate._value_
    else:
        tosend = blockToText(b.get_lastblock()) #sending the last block of the chain as text
    send_connection(soc,tosend)

    answer = read_connection(soc)
    print("answer "+answer)
    soc.close();
#----------------------------serverside------------------------
def receiveBlock(conn):
    # get last 4 chars of current last block
    tempp = b.get_lastblock().hash
    last4ofhashblockchain = tempp[-4:]
    toSend = str(b.get_lastblock().index) +'/'+ last4ofhashblockchain

    send_connection(conn,toSend)

    receive = read_connection(conn)
    if receive == conversation.upToDate._value_:
        return
    else:
        blockIncoming = textToBlock(receive)
        if b.controle_add(blockIncoming):
            send=conversation.accepted._value_
        else:
            send=conversation.notAccepted._value_
        send_connection(conn,send)



    #....

def Connection_as_server(conn, ip):
    identification_code = read_connection(conn)
    if identification_code==conversation.sendBLock._value_:
        receiveBlock(conn)


    conn.close()  # close connection
    print('Connection ' + str(ip) + ':' + str(portNumber)+ " ended")


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created on')

    ipaddress = readIp_node(NUMBER_NODE)
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


    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=Connection_as_server, args=(conn, ip)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

#-----------------main---------------------------


def main():
    if not authentification():
        print('not authentificate')
        return
    Thread(target=start_server).start()
    print('ja')
    while(True):
        inputText = input("to sho blockshain press'" + conversation.showBlockchain._value_+"', to make a transaction press everithing else'\n")
        if inputText ==conversation.showBlockchain._value_:
            b.print()
        else:
            amount = int(input('how much do you want to give\n'))
            who = input('to who\n')
            block = b.newTransaction(who,amount)
            #b.print()
            sendBlocksEoAll()




#------- TESTBENCH --------
# b = blockchain()
# dateTime = str(datetime.datetime.now())
# blok1 = block(1, 4, dateTime, "kakak", "sender", "previousHash")
#
#
# textFromBlock = blockToText(blok1)
# print(textFromBlock+"\n")
# blockRecoverd =textToBlock(textFromBlock)
# textRecoverd = blockToText(blockRecoverd)
# print(textRecoverd+"\n")
#
#
# b.__add__(blok1)
# blok2 = block(4, 4, dateTime, "Ruben", "sender", b.get_lastblock().hash)
# b.controle_add(blok2)
#
# print(b.get_lastblock().receiver)
# authentification()
#blok1 = block(1, 4, "123", "kakak", "sender", "previousHash")



main()
