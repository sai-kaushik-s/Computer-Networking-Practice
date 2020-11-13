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

from huffman import Huffman

clientSocket = socket.socket()
host = socket.gethostname()
port = 9001

clientSocket.connect((host, port))

filePath = input("Enter the path of the file: ")
fileName = os.path.basename(filePath)
clientSocket.send(bytes(fileName, "utf-8"))

with open(filePath, "r") as fp:
    fileData = fp.read()

huffman = Huffman(fileData)
encodedData = huffman.encode()

clientSocket.send(pickle.dumps(huffman))

n = 1024
subStrings = [encodedData[i:i+n] for i in range(0, len(encodedData), n)]

for it in subStrings:
    clientSocket.send(bytes(it, "utf-8"))

clientSocket.close()
