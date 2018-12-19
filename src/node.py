
from src.lib import *
import socket
# for handling task in separate jobs we need threading
from threading import Thread
import time

NUMBER_NODE_temp = inputUser("What client do you want to be?\n") #read from terminal
NUMBER_NODE=int(NUMBER_NODE_temp)
b = blockchain()
Neighbors=readIp_neighbors(NUMBER_NODE)
BlockWaitingToBeAdd=None
IpOfThisNode = readIp_node(NUMBER_NODE)


#-----------------------------------------
def authentification():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ipAuthentification, portNumber))
        thisUser = readUser(NUMBER_NODE)
        send_connection(soc, thisUser.username)  #send username to auth center
        nonce = read_connection(soc)  #receive nonce
        send_connection(soc, thisUser.setNonce(nonce))  #send back hash

        answer = read_connection(soc)
        print(answer)

        soc.close();
        return answer==conversation.accepted.value
    except:
        return 0



def sendConfirmatioOfNewBlock( neighbor):
    toSend = conversation.confirmNewBlock.value
    send_connection(neighbor.connection, toSend)

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
            for i in range(len(Neighbors)):
                Thread(target=sendConfirmatioOfNewBlock, args=[ Neighbors[i]]).start()


        else:
            print('response: blok not accepted')



def start_conversation_client(ip, conversationEnumValue):
    # open socket
    print('start soc with '+ip+':'+str(portNumber))
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = Ip4, STREAM = TCP
    soc.bind((IpOfThisNode,0))
    # open the socket
    iPaddresssServer = ip
    soc.connect((iPaddresssServer, portNumber))#ip4 and tcp
    send_connection(soc, conversationEnumValue)  #send kind of conversation
    return soc

def sendBlocksToAllWithCheck(ip='optional'):
    #ip => ask not to this ip address
    #asking last index to neighbours
    #for not sending the same block 2 times
    for i in range(len(Neighbors)):
        if Neighbors[i].ipAddress!=ip:
            Neighbors[i].reset()
            Thread(target=sendNewBlockWithCheck, args=[ Neighbors[i]]).start()
        else:
            Neighbors[i].setTrue()

def sendBlocksToAll(ip='optional'):
    #ip => ask not to this ip address
    #asking last index to neighbours
    #for not sending the same block 2 times
    for i in range(len(Neighbors)):
        if Neighbors[i].ipAddress!=ip and neighbor.connection ==None:
            Neighbors[i].reset()

            Thread(target=sendBlock, args=[ Neighbors[i]]).start()
        else:
            Neighbors[i].setTrue()



#send a block that you have receive from one of your neighbors to your other neighbors. first you have to ask if they already have this new block or not
def sendBlock(neighbor):
    try:
        soc = start_conversation_client(neighbor.ipAddress, conversation.askStatusOfBLockchain._value_)
        neighbor.setConnectio(soc)
        #what received
        result_string = read_connection(soc)
        content = result_string.split('/')

        #get last 4 chars of current last block
        tempp= b.get_lastblock().hash
        last4ofhashblockchain=tempp[-4:]

        if int(content[0])==b.get_lastblock().index and last4ofhashblockchain==content[1]: #controll of last block of neigbor: hask + index
            tosend = conversation.upToDate._value_
            send_connection(soc, tosend)
            neighbor.responseValue = True

        else:
            tosend = blockToText(b.get_lastblock()) #sending the last block of the chain as text
            send_connection(soc, tosend)

            answer = read_connection(soc)
            if answer== conversation.accepted._value_:
                neighbor.responseValue=True
            else:
                print("problem in the blockchain. neighbor doesn't accept confirmed block "+neighbor.ipAddress)

    except ConnectionRefusedError:
        print("Terible error! could not connect with: " + neighbor.ipAddress)
    except:
        print("Terible error with: " + neighbor.ipAddress)
        import traceback
        traceback.print_exc()
        soc.close()
    finally:
        neighbor.hasResponded = True

#send a new block that thos node just has made to his neighbors, if the all neighbors accept the block, the block can be add to the blockchain
def sendNewBlockWithCheck(neighbor):
    try:
        soc = start_conversation_client(neighbor.ipAddress,
                                        conversation.sendNewBLock._value_)  #start connection and specify kind of conversation = new block is goig to be send
        neighbor.setConnectio(soc)
        time.sleep(0.5)
        #sending the new Block
        toSend  = b.getWaitingBlockAsText()
        send_connection(soc, toSend)

        #Is the block accepted or not by th neigbor?
        answer = read_connection(soc)
        if answer== conversation.accepted._value_:
            #block is accepted
            neighbor.responseValue=True



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

    send_connection(conn, toSend)

    receive = read_connection(conn)
    if receive == conversation.upToDate._value_:
        return
    else:
        blockIncoming = textToBlock(receive)
        if b.controle_add(blockIncoming):
            send=conversation.accepted._value_
            ipSource = readIp_node(NUMBER_NODE)
            send_connection(conn, send)
            sendBlocksToAll(ip)

        else:
            send=conversation.notAccepted._value_
            send_connection(conn, send)

def receiveNewBlock(conn,ip):
    receivedBlockAsText = read_connection(conn)
    if b.setWaitingBlockAsText(receivedBlockAsText):
        send = conversation.accepted._value_
        send_connection(conn, send)
        receiveconfirmation = read_connection(conn)
        if receiveconfirmation:
            b.confirmWaitingBlock()
            ipSource = readIp_node(NUMBER_NODE)
            sendBlocksToAll(ip)

    else:
        send = conversation.notAccepted._value_
        send_connection(conn, send)


def Connection_as_server(conn, ip):

    identification_code = read_connection(conn)  #read first message with tag to know subject of conversation

    if identification_code==conversation.askStatusOfBLockchain._value_:
        #get a request for updating of blockchain
        receiveBlock(conn, ip)
    elif identification_code == conversation.sendNewBLock._value_:
        receiveNewBlock(conn, ip)

    conn.close()  # close connection
    print('Connection ' + str(ip) + ':' + str(portNumber) + " ended")


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
        inputText = inputUser("to show blockshain press '" + conversation.showBlockchain._value_ + "', to make a transaction press everithing else\n")
        if inputText ==conversation.showBlockchain._value_:
            b.print()
        else:
            amount = int(inputUser('how much do you want to give\n'))
            who = inputUser('to who\n')
            BlockWaitingToBeAdd =  b.setWaitingBlock(who, amount)
            sendBlocksToAllWithCheck()





main()
