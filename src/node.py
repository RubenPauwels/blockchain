
from src.lib import *
import datetime

import array as arr


# ----------------------------------------------------------------------------------

class block():
    # this is a block
    def __init__(self ,index ,amount ,timestamp_nostri ,receiver ,sender ,PrevHash):

        self.inde x =index  # height of the block
        self.amoun t =amount  # amount of transaction
        self.timestam p =timestamp_nostri  # time
        self.receive r =receiver
        self.sende r =sender
        self.PrevHas h =PrevHash  # hash of the previous block
        # we putt everything together i=str(inde x)+str(amo u nt)+str(tim e stamp_nostri)+receive r +sender+ P revHas h
        self.Hash=hash(i)

    def get_Hash(self):
        return self.Hash
    def \

    get_PrevHash(self):
        return self.PrevHash


# -


--------------------------------------------------------------------------------



def


controle (b, block):
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
        return "sqd"


b = blockchain()

test = block(2, 4, datetime.datetime.now(), "kakak", "sender", "zeze")
print(test.Hash)

b.__add__(test)
b.__add__(test)
test = block(2, 4, datetime.datetime.now(), "kaskak", "sender", "zeze")
print(test.Hash)
b.__add__(test)

yyy = b.get_lastblock
pr
int(yyy)