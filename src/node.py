import lib
import datetime
import array as arr
#----------------------------------------------------------------------------------
b=blockchain()
class block():
    #this is a block
    def __init__(self,index,amount,timestamp_nostri,receiver,sender,PrevHash):

        self.index=index #height of the block
        self.amount=amount #amount of transaction
        self.timestamp=timestamp_nostri #time
        self.receiver=receiver
        self.sender=sender
        self.PrevHash=PrevHash #hash of the previous block
        #we putt everything together
        i=str(index)+str(amount)+str(timestamp_nostri)+receiver+sender+PrevHash
        self.Hash=lib.hash(i)
    def get_LastHash(self,):
        return Hash
#----------------------------------------------------------------------------------

test=block(2,4,datetime.datetime.now(),"kakak","sender","zeze")
print test.Hash
print test.timestamp

def controle (b,block):
    #voor het toevoegen, controleren of de hash's goed zijn
    #step 4 verification
    if b.get_Hash_lastblock = block.get_Hash
        integrity = 1;
    else
        integrity = 0;
    return integrity

#----------------------


class blockchain():
    def __init__(self):
        self.Blockchain_arr=[]
    def __add__(self, block):
        self.Blockchain_arr.append(block)

    def get_Hash_lastblock(self):
        self.Blockchain_arr
        aa="s"
        return aa




b.__add__(test)
b.Blockchain_arr.get(1)
