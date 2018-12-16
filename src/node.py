
from src.lib import *
import datetime

import array as arr
import os.path

class readHostFile():
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
    # print(readIp_neighbors(2)[0])

# ----------------------------------------------------------------------------------

class block():
    # this is a block
    def __init__(self ,index ,amount ,timestamp_nostri ,receiver ,sender ,PrevHash):

        self.index =index  # height of the block
        self.amount =amount  # amount of transaction
        self.timestamp =timestamp_nostri  # time
        self.receiver =receiver
        self.sender =sender
        self.PrevHash =PrevHash  # hash of the previous block
        # we putt everything together
        i=str(index)+str(amount)+str(timestamp_nostri)+receiver +sender+ PrevHash
        self.Hash=hash(i)
    def Hash_calculate(self ,index ,amount ,timestamp_nostri ,receiver ,sender ,PrevHash):

        i = str(index) + str(amount) + str(timestamp_nostri) + receiver + sender + PrevHash
        ans = hash(i)
        return (ans)

    def blockToText():
        text = "Zever"
        return text
    print(blockToText())
    # def textToBlock():
    #     block_fromText = block;
    #     return block_fromText

# ---------------------------------------------------------------------------------




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
        if self.get_lastblock().Hash==block_incomming.PrevHash and (self.get_lastblock().index+1)==block_incomming.index :
            if block_incomming.Hash_calculate(block_incomming.index,block_incomming.amount,block_incomming.timestamp,block_incomming.receiver,block_incomming.sender,block_incomming.PrevHash)==block_incomming.Hash:
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





b = blockchain()
blok1 = block(1, 4, datetime.datetime.now(), "kakak", "sender", "zeze")
b.__add__(blok1)
blok2 = block(4, 4, datetime.datetime.now(), "Ruben", "sender", b.get_lastblock().Hash)
b.controle_add(blok2)



print(b.get_lastblock().receiver)
