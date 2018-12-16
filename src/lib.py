#lib for functions used by nodes and aut center
import hashlib
import sys

#input  a string
def generateHash(text):
     return hashlib.sha256(text.encode()).hexdigest()

portNumber = 5001
MAX_BUFFER_SIZE=4096

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