#lib for functions used by nodes and aut center
import hashlib
import sys
import random
import datetime
import os


#input  a string
def generateHash(text):
     return hashlib.sha256(text.encode()).hexdigest()

portNumber = 5001
MAX_BUFFER_SIZE=4096
ipAuthentification = "127.0.0.10"


#return the input of socket as bytes
def read_bytes(conn):
    # the input is in bytes, so decode it
    input = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    return input

#return the input of socket as text
def read_connection(conn,ipSource="unknow"):
    # decode input and strip the end of line
    text = read_bytes(conn).decode("utf8").rstrip()
    print('['+ipSource+'] receive: '+text)
    return text
def send_bytes(conn, bytes):
    conn.sendall(bytes)
def send_connection(conn, text,ipSource="unknow"):
    print('[' + ipSource + '] send: ' + text)
    conn.sendall(text.encode("utf8"))

#-------------------------neighbor--------------------------------------
class neighbor():
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        self.hasResponded=False
        self.responseValue = False
    def reset(self):
        self.hasResponded = False
        self.responseValue = False
    def setTrue(self):
        self.hasResponded = True
        self.responseValue = True


#-------------------------Textfile readers------------------------------
#input 1-6#output IP-adress
def readIp_node(nodeNumber):

        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist")
        else:
            with open(filename) as f:
                content = f.readlines()

                ip_address = content[1].split('= ')
                ip_address = ip_address[1].translate({ord(c): None for c in ' \n"'})

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

 #input 1-6#list of class Neighbor
def readIp_neighbors(nodeNumber):
        filename = "../config/host_node"+str(nodeNumber)
        if not os.path.isfile(filename):
            print("File does not exist")
        else:
            with open(filename) as f:
                content = f.readlines()
                list = content[9 :]
                ip_address_neighbors=[]
                for i in range(len(list)):
                    ipAddress = list[i].translate({ord(c): None for c in ' \n"'}) #remove white space and enter
                    if ipAddress: #only ad not emptu ip
                        ip_address_neighbors.append(neighbor(ipAddress))
                    #print(i)

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


def blockToText(block):
    text =str(block.index)+'/'+str(block.amount)+'/'+str(block.timestamp)+'/'+str(block.receiver)+'/'+str(block.sender)\
          +'/'+str(block.prevHash)+'/'+str(block.hash)
    return text
def textToBlock(text):
    content = text.split('/')
    print(content)
    blockFromText = block(int(content[0]), int(content[1]), content[2], content[3], content[4], content[5])
    return blockFromText


#-------------------------Block & Blockcha------------------------------
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
        ans = generateHash(i)
        return (ans)

    def print(self):
        print("--  index\t\t"+str(self.index))
        print("--  amount\t\t"+str(self.amount))
        print("--  timestamp\t"+self.timestamp)
        print("--  sender\t\t"+self.sender)
        print("--  receiver\t"+self.receiver)
        print("--  prevHash\t"+self.prevHash)
        print("--  hash\t\t"+self.hash)


class blockchain():
    def __init__(self):
        self.Blockchain_arr = []
        genesisBlock = block(0, 0, '0', 'I', 'you', 'genesis')
        self.Blockchain_arr.append(genesisBlock)

    def __add__(self, block_add):
        # add the given block to the blockchain
        self.Blockchain_arr.append(block_add)

    def get_lastblock(self):
        # return a copy of the last block opbject
        a = self.Blockchain_arr[-1]
        return a

    def controle(self, block_incomming):
        # function that gives back 0 or 1, to check if a block may be added to the blockchain
        if self.get_lastblock().hash == block_incomming.prevHash and (
                self.get_lastblock().index + 1) == block_incomming.index:
            if block_incomming.Hash_calculate(block_incomming.index, block_incomming.amount, block_incomming.timestamp,
                                              block_incomming.receiver, block_incomming.sender,
                                              block_incomming.prevHash) == block_incomming.hash:
                return 1
        else:
            return 0

    def controle_add(self, block_incomming):
        # controle if block may be added, if yes add
        if self.controle(block_incomming):
            self.__add__(block_incomming)
            return 1
        else:
            index = self.get_lastblock().index
            print("blok not added, should be blok" + str(index + 1))
            return 0

    def newTransaction(self, to, amount):
        lastBlock = self.get_lastblock()
        dateTime = str(datetime.datetime.now())
        newblock = block(lastBlock.index + 1, amount, dateTime, 'me', to, lastBlock.hash)
        self.__add__(newblock)
        return newblock
    def print(self):
        print("--------------------------------------------------------------------------------")
        print("---------------------------Blockchain-------------------------------------------")
        print("--------------------------------------------------------------------------------")
        for i in range(len(self.Blockchain_arr)):
            print("---------------------------block "+str(i)+"----------------------------------------------")
            self.Blockchain_arr[i].print()
        print("--------------------------------------------------------------------------------")
        print("---------------------------end of Blockchain------------------------------------")
        print("--------------------------------------------------------------------------------")

#------------------------------------------------------USer--------------------------------------------------------------------
class user():
    def __init__(self,userName,password):
        self.username=userName
        self.password=password
        self.nonce = 0

    def getNonce(self):
        self.nonce =str(random.getrandbits(80))
        return self.nonce

    def getHash(self):
        return generateHash(self.password+self.nonce)

    def setNonce(self, nonce):
        self.nonce = nonce
        return self.getHash()

    def check(self, hash):
        return hash == self.getHash()

#-------------------------identifiers for conversations---------------------------------------------
from enum import Enum

class conversation(Enum):
    sendBLock="send block"
    upToDate = "up to date"
    accepted = "accepted"
    notAccepted = "no accepted"
    showBlockchain = "e"
