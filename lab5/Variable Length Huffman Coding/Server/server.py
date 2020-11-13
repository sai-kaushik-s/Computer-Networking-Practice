r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
import socket
import pickle
from datetime import datetime

from huffman import HuffmanCoding
import os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9001

serverSocket.bind((host, port))
serverSocket.listen(10)

clientSocket, clientAddress = serverSocket.accept()
print("Client connected from ", clientAddress)

start = datetime.now()

fileName = clientSocket.recv(1024).decode("utf-8")

huffman = pickle.loads(clientSocket.recv(10240))

with open("1.bin", "wb") as fp:
    data = clientSocket.recv(1024)
    while data:
        fp.write(data)
        data = clientSocket.recv(1024)

outputFile = huffman.decompress("1.bin", fileName)

end = datetime.now()

duration = end - start
print("The time taken to receive and decomress the file: %s seconds." % str(duration.seconds))
print("Number of bytes received: %s MiB." % str(os.path.getsize("1.bin")/1000000))
print("File %s received successfully." % fileName)

os.remove("1.bin")

clientSocket.close()
