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
def read_connection(conn):
    # decode input and strip the end of line
    text = read_bytes(conn).decode("utf8").rstrip()
    print('['+conn.getpeername()[0]+'] receive: '+text)
    return text
def send_bytes(conn, bytes):
    conn.sendall(bytes)
def send_connection(conn, text):
    print('[' + conn.getpeername()[0] + '] send: ' + text)
    conn.sendall(text.encode("utf8"))

#-------------------------neighbor--------------------------------------
class neighbor():
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        self.hasResponded=False
        self.responseValue = False
        self.connection =None
    def reset(self):
        self.hasResponded = False
        self.responseValue = False
    def setTrue(self):
        self.hasResponded = True
        self.responseValue = True
    def setConnection(self, conn):
        self.connection = conn


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
                salt = content[7].split('=')[1].translate({ord(c): None for c in ' \n"'})
                secr = content[6].split('=')[1].translate({ord(c): None for c in ' \n"'})
                newUser = user(name)
                newUser.setPasswordAndSalt(secr,salt)
        return newUser


def readUserName(nodeNumber):
    filename = "../config/host_node" + str(nodeNumber)
    if not os.path.isfile(filename):
        print("File does not exist " + filename)
    else:
        with open(filename) as f:
            content = f.readlines()
            name = content[2].split('=')[1].translate({ord(c): None for c in ' \n"'})
    return name


def blockToText(block):
    text =str(block.index)+'/'+str(block.amount)+'/'+str(block.timestamp)+'/'+str(block.receiver)+'/'+str(block.sender)\
          +'/'+str(block.prevHash)+'/'+str(block.hash)
    return text
def textToBlock(text):
    content = text.split('/')
    blockFromText = block(int(content[0]), int(content[1]), content[2], content[3], content[4], content[5])
    return blockFromText


#-------------------------Block & Blockchain------------------------------
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
        print("--  receiver\t" + self.receiver)
        print("--  sender\t\t"+self.sender)
        print("--  prevHash\t"+self.prevHash)
        print("--  hash\t\t"+self.hash)



class blockchain():
    def __init__(self):
        self.Blockchain_arr = []
        genesisBlock = block(0, 0, '0', 'I', 'you', 'genesis')
        self.Blockchain_arr.append(genesisBlock)
        self.blockWaitingToBeAdd=None

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
        #no 2 threads can do this at the same time
        with self.lock:
            # controle if block may be added, if yes add
            if self.controle(block_incomming):
                self.__add__(block_incomming)
                return 1
            elif block_incomming.index==self.get_lastblock().index:
                return 1
            else:
                index = self.get_lastblock().index
                print("blok not added, should be blok" + str(index + 1))
                return 0
    #make a block on top of the blockchain and set it on a waiting position until it can be add by calling 'addWaitingBlock'
    def setWaitingBlock(self, to, amount, NUMBER_NODE):
        lastBlock = self.get_lastblock()
        dateTime = str(datetime.datetime.now())
        # if (lastBlock.index == 0):
        #     name = lastBlock.sender
        # else:
        #     name = readUserName(int(lastBlock.receiver))
        name = readUserName(NUMBER_NODE)
        self.blockWaitingToBeAdd = block(lastBlock.index + 1, amount, dateTime, to ,name, lastBlock.hash) #block(index,amount,time, RECEIVER, SENDER, hash)
        return self.blockWaitingToBeAdd

    #add the block that is waiting to ba add on top of the blockchain
    def confirmWaitingBlock(self):
        if self.controle_add(self.blockWaitingToBeAdd):
            self.blockWaitingToBeAdd=None
            return 1
        else:
            self.blockWaitingToBeAdd = None
            print ("big problem block cant be add in blockchain")
            return 0

    def setWaitingBlockAsText(self, text):
        blockToAdd = textToBlock(text)
        if self.controle(blockToAdd):
            self.blockWaitingToBeAdd = blockToAdd
            return 1
        else:
            return 0

    def getWaitingBlockAsText(self):
        return blockToText(self.blockWaitingToBeAdd)

    def controle_add_text(self,text):
        blockToAdd = textToBlock(text)
        self.controle_add(blockToAdd)


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

#------------------------------------------------------USER--------------------------------------------------------------------
class user():
    def __init__(self, username):
        self.username=username
        self.nonce = 0

    def setPasswordAndSalt(self,password,salt):
        print("password:"+password)
        print("salt:"+salt)
        self.saltedPasswordHash = generateHash(password + salt)

        print("saltedPasswordHash:"+self.saltedPasswordHash)

    def setHashSaltedPassword(self, saltedUserNameHash):
        self.saltedPasswordHash=saltedUserNameHash

    def generateNewNonce(self):
        self.nonce =str(random.getrandbits(80))
        return self.nonce

    def getHashSaltedPassword(self):
        return self.saltedPasswordHash

    def getHashWithNonce(self):
        return str(generateHash(self.saltedPasswordHash + self.nonce))

    def setNonce(self, nonce):
        print("nonce:"+nonce)
        self.nonce = nonce
        return self.getHashWithNonce()

    def check(self, hash):
        return hash == self.getHashWithNonce()





#-------------------------identifiers for conversations---------------------------------------------
from enum import Enum

class conversation(Enum):
    sendNewBLock="I want to send you my new block, can you check it?"
    confirmNewBlock='my new block is confirmed by everyone, add it to your blockchain'
    notConfirmNewBlock = "my new block is not confirmed by everyone, don't it to your blockchain"
    askStatusOfBLockchain="this is my latest block? If I have a newer block than you I will send it you"
    ImUpToDate = "I'm up to date"
    ImNotUpToDate = "I'm not up to date"
    accepted = "accepted"
    notAccepted = "not accepted"
    showBlockchain = "b"


#https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
def inputUser(text):
    return input("\x1b[47;30m"+ text+"\x1b[0m")

def printUser(text):
    print("\x1b[47;30m" + text + "\x1b[0m")