#lib for functions used by nodes and aut center
import hashlib
import sys
import random



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
    print('receive '+text)
    return text

def send_bytes(conn, bytes):
    conn.sendall(bytes)


def send_connection(conn, text):
    conn.sendall(text.encode("utf8"))

#-------------------------USer------------------------------
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
    sendBLock='a'
