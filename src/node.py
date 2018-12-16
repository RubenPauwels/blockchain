
from src.lib import *
import datetime

import array as arr


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



# ---------------------------------------------------------------------------------



def controle (b, block):
    # voor het toevoegen, controleren of de hash's goed zijn
    # step 4 verification
    if b.get_Hash_lastblock() == block.get_PrevHash():
        integrity = 1
    else:
        integrity = 0


# ----------------------


class blockchain():
    def __init__(self):
        self.Blockchain_arr = []

    def __add__(self, block):
        self.Blockchain_arr.append(block)

    def get_lastblock(self):
        a=self.Blockchain_arr[self.Blockchain_arr.__len__()-1]
        return (a)
    def controle(self,block_incomming):

        if self.get_lastblock().Hash==block_incomming.PrevHash and (self.get_lastblock().index+1)==block_incomming.index :
            if block_incomming.Hash_calculate()==block_incomming.Hash:
                self.Blockchain_arr.append(block_incomming)
                return 1
        else:
            return 0





b = blockchain()

blok1 = block(1, 4, datetime.datetime.now(), "kakak", "sender", "zeze")
b.__add__(blok1)
#blok2 = block(2, 4, datetime.datetime.now(), "Ruben", "sender", b.get_lastblock().Hash)
#b.controle(blok2)



print(b.get_lastblock().receiver)
