r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
import os
import socket
import pickle
from datetime import datetime

from huffman import HuffmanCoding
from time import sleep

clientSocket = socket.socket()
host = socket.gethostname()
port = 9001

clientSocket.connect((host, port))

filePath = input("Enter the path of the file: ")
fileName = os.path.basename(filePath)

start = datetime.now()

clientSocket.send(bytes(fileName, "utf-8"))

huffman = HuffmanCoding(filePath)
compressedFilePath = huffman.compress()
sleep(1)

clientSocket.send(pickle.dumps(huffman))

with open(compressedFilePath, "rb")as fp:
    data = fp.read(1024)
    while data:
        clientSocket.send(data)
        data = fp.read(1024)

end = datetime.now()

duration = end - start
compressionRatio = os.path.getsize(filePath)/os.path.getsize(compressedFilePath)
print("The compression ratio: %s." % compressionRatio)
print("The time taken to compress and send the file: %s seconds." % str(duration.seconds))
print("Number of bytes transfered: %s MiB." % str(os.path.getsize(compressedFilePath)/1000000))
print("File %s transferred successfully." % fileName)

os.remove(compressedFilePath)

clientSocket.close()
