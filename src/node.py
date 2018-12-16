
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




b = blockchain()

test = block(2, 4, datetime.datetime.now(), "kakak", "sender", "zeze")
print(test.Hash)

b.__add__(test)
test = block(1, 4, datetime.datetime.now(), "kaskak", "sender", "zeze")
b.__add__(test)




print(test.Hash)

print(b.get_lastblock().Hash)
