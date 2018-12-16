
from src.lib import *
import datetime
from src.lib import send_connection
from src.lib import read_connection
import socket
from src.lib import *
from threading import Thread
import src.lib
import socket

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
                # for i in ip_address_neighbors:
                #     print(i)

        return ip_address_neighbors

# ----------------------------------------------------------------------------------

class block():
    # this is a block
    def __init__(self, index, amount, timestamp, receiver, sender, prevHash):
        self.index =index  # height of the block
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

    def __add__(self, block_add):
        #add the given block to the blockchain
        self.Blockchain_arr.append(block_add)

    def get_lastblock(self):
        #return a copy of the last block opbject
        a=self.Blockchain_arr[self.Blockchain_arr.__len__()-1]
        return (a)
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
        else:
            index=b.get_lastblock().index
            print("blok not added, should be blok"+str(index+1))



#how to get the time
#datetime.datetime.now()


#------- TESTBENCH --------
b = blockchain()
dateTime = str(datetime.datetime.now())
blok1 = block(1, 4, dateTime, "kakak", "sender", "previousHash")


textFromBlock = blockToText(blok1)
print(textFromBlock+"\n")
blockRecoverd =textToBlock(textFromBlock)
textRecoverd = blockToText(blockRecoverd)
print(textRecoverd+"\n")


b.__add__(blok1)
blok2 = block(4, 4, dateTime, "Ruben", "sender", b.get_lastblock().hash)
b.controle_add(blok2)

print(b.get_lastblock().receiver)





def sendBlock():
    #asking last index to neighbours
    #for not sending the same block 2 times
    list=readIp_neighbors(NUMBER_NODE)
    for i in list:
        Thread(target=askIndex_threat, args=(i)).start()

def askIndex_threat(i):

    #open socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #open the socket
    iPaddresssServer=i
    soc.connect((iPaddresssServer, src.lib.portNumber))
    #what to send
    clients_input="a"
    send_connection(soc, clients_input)  # we must encode the string to bytes

    #what received
    result_string = read_connection(soc)
    content = result_string.split('/')

    #get last 4 chars of current last block
    tempp= b.get_lastblock().hash
    last4ofhashblockchain=tempp[-4:]

    if int(content[0])==b.get_lastblock().index and last4ofhashblockchain==content[1]:
        #send block to server
        test="sd"
    else:
        abortmission=#sqd#
    soc.close();