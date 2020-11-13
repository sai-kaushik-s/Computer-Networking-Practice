r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
import os
import pickle
import socket
from datetime import datetime
from time import sleep

from huffman import huffmanEncode

clientSocket = socket.socket()
host = socket.gethostname()
port = 9001

clientSocket.connect((host, port))

filePath = input("Enter the path of the file: ")
fileName = os.path.basename(filePath)

start = datetime.now()

clientSocket.send(bytes(fileName, "utf-8"))

with open(filePath, "r") as fp:
    fileData = fp.read()

encodedData, codes = huffmanEncode(fileData)
sleep(1)
clientSocket.send(pickle.dumps(codes))
clientSocket.send(pickle.dumps(encodedData))

end = datetime.now()

duration = end - start
print("The time taken to compress and send the file: %s seconds." % str(duration.seconds))
print("Number of bytes transmitted: %s MiB." % str(os.path.getsize(filePath)/1000000))
print("File %s transmitted successfully." % fileName)

clientSocket.close()
