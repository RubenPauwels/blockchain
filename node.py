import lib
import datetime
class block():
    #this is a block
    def __init__(self,index,amount,timestamp_nostri,receiver,sender,PrevHash):
        self.index=index
        self.amount=amount
        self.timestamp=timestamp_nostri
        self.receiver=receiver
        self.sender=sender
        self.PrevHash=PrevHash

        i=str(index)+str(amount)+str(timestamp_nostri)+receiver+sender+PrevHash

        self.Hash=lib.hash(i)
test=block(2,4,datetime.datetime.now(),"kakak","sender","zeze")
print test.Hash
print test.timestamp


class blockchain():
    def __init__(self):
        
