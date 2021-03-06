
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


#-----------------------------------------authentification--------------------
def authentification():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((IpOfThisNode, 0))
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

#-----------------------node as client--------------------

def sendConfirmatioOfNewBlock(neighbor, accepted):
    if accepted:
        toSend = conversation.confirmNewBlock.value
    else:
        toSend = conversation.notConfirmNewBlock.value
    send_connection(neighbor.connection, toSend)
def checkNeigborsResponse():
    evryoneAnswered=1
    answer=1
    for i in range(len(Neighbors)):
        evryoneAnswered = evryoneAnswered and Neighbors[i].hasResponded
        answer = answer and Neighbors[i].responseValue
    if evryoneAnswered:
        if answer:
            printUser('Block added to the blockchain')
            b.confirmWaitingBlock()
            accepted=True
            for i in range(len(Neighbors)):
                Thread(target=sendConfirmatioOfNewBlock, args=[Neighbors[i], accepted]).start()

        else:
            printUser('Blok not accepted')
            accepted=False

            for i in range(len(Neighbors)):
                if Neighbors[i].responseValue:
                    Thread(target=sendConfirmatioOfNewBlock, args=[Neighbors[i],accepted]).start()

def start_conversation_client(ip, conversationEnumValue, contentFirstMessage=None):
    # open socket
    print('start soc with '+ip+':'+str(portNumber))
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = Ip4, STREAM = TCP
    soc.bind((IpOfThisNode,0))
    # open the socket
    iPaddresssServer = ip
    soc.connect((iPaddresssServer, portNumber))#ip4 and tcp
    send_connection(soc, conversationEnumValue+"/"+contentFirstMessage)  #send kind of conversation + first content of conversation
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

#neighbos who already have the update
ipAlreadyUpToDate =[]
latestIndex=0
def sendBlocksToAll():
    #ip => ask not to this ip address

    #for not sending the same block 2 times
    for i in range(len(Neighbors)):
        if not Neighbors[i].ipAddress in ipAlreadyUpToDate:# and neighbor[ip].connection ==None:
            Neighbors[i].reset()

            Thread(target=sendBlock, args=[ Neighbors[i]]).start()
        else:
            Neighbors[i].setTrue()

#send a block that you have receive from one of your neighbors to your other neighbors. first you have to ask if they already have this new block or not
def sendBlock(neighbor):
    try:
        tempp = b.get_lastblock().hash
        last4ofhashblockchain = tempp[-4:]
        firstContent = str(b.get_lastblock().index) + '/' + last4ofhashblockchain

        #start socket
        soc = start_conversation_client(neighbor.ipAddress, conversation.distribution._value_, firstContent)
        #remember socket
        neighbor.setConnection(soc)

        #what received
        result_string = read_connection(soc)
        if result_string==conversation.ImNotUpToDate.value:
            tosend = blockToText(b.get_lastblock()) #sending the last block of the chain as text
            send_connection(soc, tosend)

            answer = read_connection(soc)
            if answer== conversation.accepted._value_:
                neighbor.responseValue=True
            else:
                printUser("problem in the blockchain. neighbor doesn't accept confirmed block "+neighbor.ipAddress)

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
        # start connection and specify kind of conversation = new block is goig to be send and send waiting block
        soc = start_conversation_client(neighbor.ipAddress, conversation.sendCreatedBLock._value_, b.getWaitingBlockAsText())
        neighbor.setConnection(soc)


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


#----------------------------node as server------------------------
def receiveBlock(conn, contentFirstMessage):
    global latestIndex
    ipAlreadyUpToDate.append(conn.getpeername()[0])
    # what received
    infolastBlock = contentFirstMessage
    content = infolastBlock.split('/')

    # get last 4 chars of current last block
    tempp = b.get_lastblock().hash
    last4ofhashblockchain = tempp[-4:]

    if int(content[0]) == b.get_lastblock().index and last4ofhashblockchain == content[1]:  # controll of last block of neigbor: hask + index
        tosend = conversation.ImUpToDate._value_
        send_connection(conn, tosend)
    else:
        tosend =  conversation.ImNotUpToDate._value_
        send_connection(conn, tosend)


        receive = read_connection(conn)
        blockIncoming = textToBlock(receive)
        if blockIncoming.index<=latestIndex and b.controle(blockIncoming):
            toSend = conversation.accepted._value_
            send_connection(conn, toSend)
        elif b.controle_add(blockIncoming):
            latestIndex=latestIndex+1
            ipAlreadyUpToDate.clear()
            ipAlreadyUpToDate.append(conn.getpeername()[0])
            toSend=conversation.accepted._value_
            send_connection(conn, toSend)
            printUser("an new block is aded to the blockchain by " + conn.getpeername()[0] + " press " + conversation.showBlockchain._value_ + " to see the blockchain")
            sendBlocksToAll()

        else:
            send=conversation.notAccepted._value_
            send_connection(conn, send)

def validateCreatedBlock(conn, contentFirstMessage):
    global latestIndex
    #the first message contains the created block as Text
    receivedBlockAsText = contentFirstMessage

    #the created block is controlled and if accept stored to be add in the blockchain
    if b.setWaitingBlockAsText(receivedBlockAsText):
        #send back to the creater of the block that we accept the block
        toSend = conversation.accepted._value_
        send_connection(conn, toSend)

        #we received the final confirmation from the creator of the block
        receiveConfirmation = read_connection(conn)

        # the final confirmation said that the block has been approved by everyone
        if receiveConfirmation==conversation.confirmNewBlock.value:
            #We add the block to our blockchain
            b.confirmWaitingBlock()
            #we distribute this new block to our neighbors (except to the neighbor that created the block)

            #the user is informd that a new block has been added to the chain
            printUser("an new block is aded to the blockchain by "+conn.getpeername()[0]+" press "+conversation.showBlockchain._value_+" to see the blockchain")
            ipAlreadyUpToDate.clear()
            ipAlreadyUpToDate.append(conn.getpeername()[0])
            latestIndex= latestIndex + 1
            sendBlocksToAll()


        # the final confirmation said that the block has NOT been approved by everyone
        else:
            # the user is informd that a neighbor try to create a new blockbut failed
            printUser( conn.getpeername()[0]+" try to add a new block to the chain, but the block was not accepted press "+conversation.showBlockchain._value_+" to see the blockchain press "+conversation.showBlockchain._value_+" to see the blockchain")

    # the created block was controlled but not approved
    else:
        # send back to the creater of the block that we NOT accept the block
        toSend = conversation.notAccepted._value_
        send_connection(conn, toSend)
        #conversation is done, the creator will inform everyone that the block can not be added to the blockchain



def Connection_as_server(conn, ip):
    try:
        # read first message and split into tag and content
        read = read_connection(conn).split('/', 1)

        #fisrt part of the message is a tag to know todetermine the subject of conversation
        identification_code = read[0]
        #the second part of the message is content for the conversation
        contentFirstMessage = read[1]

        # the tag indicate that this message is about distribution algoritm
        if identification_code==conversation.distribution.value:
            #start distribution conversation
            receiveBlock(conn, contentFirstMessage)

        # the tag indicate that this message is about validation of a new created block algoritm
        elif identification_code == conversation.sendCreatedBLock.value:
            # start validation conversation
            validateCreatedBlock(conn, contentFirstMessage)

    finally:
        print('Connection', conn.getpeername()[0], ':' + str(portNumber) + " ended")
        conn.close()  # close connection


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


    # this will make an infinite loop needed for not reseting server for every client
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
            BlockWaitingToBeAdd = b.setWaitingBlock(who, amount, NUMBER_NODE)
            sendBlocksToAllWithCheck()





main()
