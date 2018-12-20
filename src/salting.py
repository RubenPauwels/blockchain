import os
import random
from src.lib import user
from src.lib import readUser

userFilePath = "../config/users.txt"
userFile = open(userFilePath, "w")

for nodeNumber in range(1,7):

    nodeFile = "../config/host_node" + str(nodeNumber)

    if not os.path.isfile(nodeFile):
        print("File does not exist")
    else:


        with open(nodeFile) as f:
            content = f.readlines()

            salt = str(random.getrandbits(2))
            content[7] = "salting = " +salt+"\n"
            f.close()

            f = open(nodeFile, "w")
            for s in content:
                f.write(s)
            f.close()


            newUser = readUser(nodeNumber)

            userFile.write(newUser.username + " " + newUser.getHashSaltedPassword() + "\n")





userFile.close()