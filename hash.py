print("hello world")
import hashlib

#input  a string
def hashb(text):
     return hashlib.sha256(text.encode()).hexdigest()



print(hashlib.algorithms_available)
print(hashlib.algorithms_guaranteed)
text="Hello World"
hash_object = hashlib.sha256(b'Hello World')
print(hashlib.sha256(text.encode()).hexdigest())


print(text.encode())
print(hashb(text))



