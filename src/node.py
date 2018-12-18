
from src.lib import *
import socket
# for handling task in separate jobs we need threading
from threading import Thread
import time

NUMBER_NODE_temp = input("What client do you want to be?\n") #read from terminal
NUMBER_NODE=int(NUMBER_NODE_temp)
b = blockchain()
Neighbors=readIp_neighbors(NUMBER_NODE)
BlockWaitingToBeAdd=None



#-----------------------------------------
def authentification():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((ipAuthentification, portNumber))
    thisUser = readUser(NUMBER_NODE)
    ipSource="authentification center"
    send_connection(soc,thisUser.username,ipSource)  #send username to auth center
    nonce = read_connection(soc,ipSource)    #receive nonce
    send_connection(soc,thisUser.setNonce(nonce),ipSource)   #send back hash

    answer = read_connection(soc,ipSource)
    print(answer)

    soc.close();
    return answer=="accept"




def checkNeigborsResponse():
    evryoneAnswered=1
    answer=1
    for i in range(len(Neighbors)):
        evryoneAnswered = evryoneAnswered and Neighbors[i].hasResponded
        answer = answer and Neighbors[i].responseValue
    if evryoneAnswered:
        if answer:
            print('response: block added to the blockchain')
            b.confirmWaitingBlock()
        else:
            print('response: blok not accepted')



def start_conversation_client(ip, conversationEnumValue,ipSource):
    # open socket
    print('start soc with '+ip+':'+str(portNumber))
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = Ip4, STREAM = TCP
    soc.bind((ipSource,0))
    # open the socket
    iPaddresssServer = ip
    soc.connect((iPaddresssServer, portNumber))#ip4 and tcp
    send_connection(soc, conversationEnumValue,ip)#send kind of conversation
    return soc

def sendBlocksToAllWithCheck(ipSource, ip='optional'):
    #ip => ask not to this ip address
    #asking last index to neighbours
    #for not sending the same block 2 times
    for i in range(len(Neighbors)):
        if Neighbors[i].ipAddress!=ip:
            Neighbors[i].reset()
            Thread(target=sendNewBlockWithCheck, args=[ipSource, Neighbors[i]]).start()
        else:
            Neighbors[i].setTrue()

def sendBlocksToAll(ipSource, ip='optional'):
    #ip => ask not to this ip address
    #asking last index to neighbours
    #for not sending the same block 2 times
    for i in range(len(Neighbors)):
        if Neighbors[i].ipAddress!=ip:
            Neighbors[i].reset()
            Thread(target=sendBlock, args=[ipSource, Neighbors[i]]).start()
        else:
            Neighbors[i].setTrue()



#send a block that you have receive from one of your neighbors to your other neighbors. first you have to ask if they already have this new block or not
def sendBlock(ipSource, neighbor):
    try:
        soc =start_conversation_client(neighbor.ipAddress, conversation.askStatusOfBLockchain._value_, ipSource)

        #what received
        result_string = read_connection(soc, neighbor.ipAddress)
        content = result_string.split('/')

        #get last 4 chars of current last block
        tempp= b.get_lastblock().hash
        last4ofhashblockchain=tempp[-4:]

        if int(content[0])==b.get_lastblock().index and last4ofhashblockchain==content[1]: #controll of last block of neigbor: hask + index
            tosend = conversation.upToDate._value_
        else:
            tosend = blockToText(b.get_lastblock()) #sending the last block of the chain as text
        send_connection(soc, tosend, neighbor.ipAddress)

        answer = read_connection(soc, neighbor.ipAddress)
        if answer== conversation.accepted._value_:
            neighbor.responseValue=True

        soc.close();

    except ConnectionRefusedError:
        print("Terible error! could not connect with: " + neighbor.ipAddress)
    except:
        print("Terible error with: " + neighbor.ipAddress)
        import traceback
        traceback.print_exc()
    finally:
        neighbor.hasResponded = True

#send a new block that thos node just has made to his neighbors, if the all neighbors accept the block, the block can be add to the blockchain
def sendNewBlockWithCheck(ipSource, neighbor):
    try:
        soc =start_conversation_client(neighbor.ipAddress, conversation.sendNewBLock._value_, ipSource)#start connection and specify kind of conversation = new block is goig to be send
        time.sleep(0.5)
        #sending the new Block
        toSend  = b.getWaitingBlockAsText()
        send_connection(soc,toSend,neighbor.ipAddress)

        #Is the block accepted or not by th neigbor?
        answer = read_connection(soc, neighbor.ipAddress)
        if answer== conversation.accepted._value_:
            #block is accepted
            neighbor.responseValue=True

        soc.close();

    except ConnectionRefusedError:
        print("Terible error! could not connect with: " + neighbor.ipAddress)
    except:
        print("Terible error! with: " + neighbor.ipAddress)
        import traceback
        traceback.print_exc()
    finally:
        # conversation with this neighbor is done
        neighbor.hasResponded = True
        checkNeigborsResponse()


#----------------------------serverside------------------------
def receiveBlock(conn,ip):
    # get last 4 chars of current last block
    tempp = b.get_lastblock().hash
    last4ofhashblockchain = tempp[-4:]
    toSend = str(b.get_lastblock().index) +'/'+ last4ofhashblockchain

    send_connection(conn,toSend,ip)

    receive = read_connection(conn,ip)
    if receive == conversation.upToDate._value_:
        return
    else:
        blockIncoming = textToBlock(receive)
        if b.controle_add(blockIncoming):
            send=conversation.accepted._value_
            ipSource = readIp_node(NUMBER_NODE)
            send_connection(conn, send, ip)
            sendBlocksToAll(ipSource, ip)

        else:
            send=conversation.notAccepted._value_
            send_connection(conn,send,ip)

def receiveNewBlock(conn,ip):
    receive = read_connection(conn, ip)
    blockIncoming = textToBlock(receive)
    if b.controle_add(blockIncoming):
        send = conversation.accepted._value_
        send_connection(conn, send, ip)
        receiveconfirmation =  read_connection(conn, ip)
        if receiveconfirmation


        ipSource = readIp_node(NUMBER_NODE)
        sendBlocksToAll(ipSource, ip)

    else:
        send = conversation.notAccepted._value_
        send_connection(conn, send, ip)


    ipSource = readIp_node(NUMBER_NODE)
    sendBlocksToAll(ipSource, ip)

def Connection_as_server(conn, ipSource):
    identification_code = read_connection(conn,ipSource)#read first message with tag to know subject of conversation

    if identification_code==conversation.askStatusOfBLockchain._value_:
        #get a request for updating of blockchain
        receiveBlock(conn,ipSource)
    elif identification_code == conversation.sendNewBLock._value_:
        receiveNewBlock(conn,ipSource)

    conn.close()  # close connection
    print('Connection ' + str(ipSource) + ':' + str(portNumber)+ " ended")


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
    ipSource = readIp_node(NUMBER_NODE)
    while(True):
        inputText = input("to sho blockshain press'" + conversation.showBlockchain._value_+"', to make a transaction press everithing else'\n")
        if inputText ==conversation.showBlockchain._value_:
            b.print()
        else:
            amount = int(input('how much do you want to give\n'))
            who = input('to who\n')
            BlockWaitingToBeAdd =  b.setWaitingBlock(who, amount)
            sendBlocksToAllWithCheck(ipSource)





main()
