
from src.lib import *
import datetime
from src.lib import send_connection
from src.lib import read_connection
import socket
from src.lib import *
from threading import Thread
import src.lib
import socket

# for handling task in separate jobs we need threading
from threading import Thread

import array as arr
import os.path

NUMBER_NODE_temp = input("What client do you want to be?\n") #read from terminal
NUMBER_NODE=int(NUMBER_NODE_temp)


#input 1-6#output IP-adress
def readIp_node(nodeNumber):

        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist")
        else:
            with open(filename) as f:
                content = f.readlines()

                ip_address = content[1].split('= ')
                ip_address = ip_address[1]

        return ip_address

#input 1-6#registration IP adress
def readIp_reg(nodeNumber):
        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist")
        else:
            with open(filename) as f:
                content = f.readlines()

                ip_address = content[5].split('= ')
                ip_address = ip_address[1]

        return ip_address

 #input 1-6#list of ip numbers of neighbors
def readIp_neighbors(nodeNumber):
        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist")
        else:
            with open(filename) as f:
                content = f.readlines()
                ip_address_neighbors = content[9 :]
                for i in range(len(ip_address_neighbors)):
                    ip_address_neighbors[i] = ip_address_neighbors[i].translate({ord(c): None for c in ' \n"'})


        return ip_address_neighbors

 #input 1-6#list of ip numbers of neighbors
def readUser(nodeNumber):
        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist "+filename)
        else:
            with open(filename) as f:
                content = f.readlines()
                name = content[2].split('=')[1].translate({ord(c): None for c in ' \n"'})
                secr = content[6].split('=')[1].translate({ord(c): None for c in ' \n"'})
        return user(name,secr)

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



# ----------------------------------------------------------------------------------






class block():
    # this is a block
    def __init__(self, index, amount, timestamp, receiver, sender, prevHash):
        self.index =index  # height of the block
        print('indexb '+str(self.index))
        self.amount =amount  # amount of transaction
        self.timestamp =timestamp  # time (string)
        self.receiver =receiver
        self.sender =sender
        self.prevHash =prevHash  # hash of the previous block
        # we putt everything together

        i=str(index) + str(amount) + timestamp + receiver + sender + prevHash

        self.hash = generateHash(i)


    def Hash_calculate(self, index, amount, timestamp, receiver, sender, prevHash):
        i = str(index) + str(amount) + timestamp + receiver + sender + prevHash
        ans = hash(i)
        return (ans)

    def print(self):
        print(" index "+str(self.index))
        print(" amount "+str(self.amount))
        print(" timestamp "+self.timestamp)
        print(" receiver "+self.receiver)
        print(" prevHash "+self.prevHash)
        print(" hash "+self.hash)
# ---------------------------------------------------------------------------------



def blockToText(block):
    text =str(block.index)+'/'+str(block.amount)+'/'+str(block.timestamp)+'/'+str(block.receiver)+'/'+str(block.sender)\
          +'/'+str(block.prevHash)+'/'+str(block.hash)
    return text

def textToBlock(text):
    content = text.split('/')
    print(content)
    blockFromText = block(int(content[0]), int(content[1]), content[2], content[3], content[4], content[5])
    return blockFromText


# ----------------------


class blockchain():
    def __init__(self):
        self.Blockchain_arr = []
        genesisBlock = block(0, 0, '0', 'I', 'you', 'genesis')
        self.Blockchain_arr.append(genesisBlock)


    def __add__(self, block_add):
        #add the given block to the blockchain
        self.Blockchain_arr.append(block_add)

    def get_lastblock(self):
        #return a copy of the last block opbject
        a=self.Blockchain_arr[-1]
        return a

    def controle(self,block_incomming):
        #function that gives back 0 or 1, to check if a block may be added to the blockchain
        if self.get_lastblock().hash==block_incomming.prevHash and (self.get_lastblock().index+1)==block_incomming.index :
            if block_incomming.regenerateHash(block_incomming.index,block_incomming.amount,block_incomming.timestamp,block_incomming.receiver,block_incomming.sender,block_incomming.prevHash)==block_incomming.hash:
                return 1
        else:
                return 0

    def controle_add(self,block_incomming):
        #controle if block may be added, if yes add
        if self.controle(block_incomming):
            self.__add__(block_incomming)
            return 1
        else:
            index=b.get_lastblock().index
            print("blok not added, should be blok"+str(index+1))
            return 0

    def newTransaction(self,to,amount):
        lastBlock = self.get_lastblock()
        dateTime = str(datetime.datetime.now())
        newblock = block(lastBlock.index+1 ,amount,dateTime, 'me','to',lastBlock.hash)
        self.__add__(newblock)
        return newblock
    def print(self):
        for i in range(len(self.Blockchain_arr)):
            print("block "+str(i))
            self.Blockchain_arr[i].print()

b = blockchain()

def start_conversation_client(i,conversationEnum):
    # open socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = Ip4, STREAM = TCP

    # open the socket
    iPaddresssServer = i
    soc.connect((iPaddresssServer, src.lib.portNumber))#ip4 and tcp
    send_connection(soc, conversationEnum)#send kind of conversation
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
        #Thread(target=sendBlock, args=str(list[i])).start()

def sendBlock(string):
    print(string)
    soc =start_conversation_client(string, conversation.sendBLock)

    #what received
    result_string = read_connection(soc)
    content = result_string.split('/')

    #get last 4 chars of current last block
    tempp= b.get_lastblock().hash
    last4ofhashblockchain=tempp[-4:]

    if int(content[0])==b.get_lastblock().index and last4ofhashblockchain==content[1]:
        tosend = conversation.ipToDate
        soc.close()
    else:
        tosend = blockToText(b.get_lastblock()) #sending the last block of the chain as text
    send_connection(soc,tosend)

    soc.close();
#----------------------------serverside------------------------
def receiveBlock(conn):
    # get last 4 chars of current last block
    tempp = b.get_lastblock().hash
    last4ofhashblockchain = tempp[-4:]
    toSend = str(b.get_lastblock().index) +'/'+ last4ofhashblockchain
    send_connection(conn,toSend)

    receive = receiveBlock(conn)
    if receive == conversation.upToDate:
        return
    else:
        blockIncoming = textToBlock(receive)
        if b.controle_add(blockIncoming):
            send=conversation.accepted
        else:
            send=conversation.notAccepted
        send_connection(conn,send)



    #....

def Connection_as_server(conn, ip):
    identification_code = read_connection(conn)
    if identification_code==conversation.sendBLock:
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
    print('length '+str(b.get_lastblock()))
    if not authentification():
        print('not authentificate')
        return
    Thread(target=start_server).start()
    print('ja')
    while(True):
        money = input('how much do you want to give\n')
        who = input('to who\n')
        block = b.newTransaction(who,money)
        b.print()
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


#print('index '+str(blok1.index))
conversation.accepted.enc
main()
