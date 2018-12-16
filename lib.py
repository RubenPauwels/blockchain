#lib for functions used by nodes and aut center
import hashlib

#input  a string
def hash(text):
     return hashlib.sha256(text.encode()).hexdigest()

