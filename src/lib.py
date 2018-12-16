#lib for functions used by nodes and aut center
import hashlib
import sys
import random

#input  a string
def hash(text):
     return hashlib.sha256(text.encode()).hexdigest()

portNumber = 5001
MAX_BUFFER_SIZE=4096
ipAuthentification = "127.0.0.10"

#return the input of socket as text
def read_connection(conn):
    # the input is in bytes, so decode it
    input = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    text = input.decode("utf8").rstrip()
    print('receive '+text)
    return text

def send_connection(conn, text):
    conn.sendall(text.encode("utf8"))

#-------------------------------------------------------
class user():
    def __init__(self,userName,password):
        self.username=userName
        self.password=password
        self.nonce = 0

    def getNonce(self):
        self.nonce =random.getrandbits(80)
        return self.nonce

    def getHash(self):
        return hash(str(self.password)+str(self.nonce))

    def setNonce(self, nonce):
        self.nonce = nonce
        return self.getHash()

    def check(self, hash):
        return hash == self.getHash()
