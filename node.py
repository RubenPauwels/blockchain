import lib
class block():
    #this is a block
    def __init__(self,index,amount,timestamp,receiver,sender,PrevHash):
        self.index=index
        self.amount=amount
        self.timestamp=timestamp
        self.receiver=receiver
        self.sender=sender
        self.PrevHash=PrevHash
        self.Hash="sqd"



a=block(2,4,23,"kakak","sender","zeze")
print lib.hash("sqd")
