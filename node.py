import lib
import datetime
class block():
    #this is a block
    def __init__(self,index,amount,timestamp,receiver,sender,PrevHash):
        self.index=index
        self.amount=amount
        self.timestamp=timestamp
        self.receiver=receiver
        self.sender=sender
        self.PrevHash=PrevHash

        i=str(index)+str(amount)

        self.Hash=lib.hash("sqd")

b="ruben"
c="kkkkk"
d=5
ff= b+c+str(d)
print ff
ts=4
ts=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')



a=block(2,4,23,"kakak","sender","zeze")
print lib.hash("sqd")
print a.Hash