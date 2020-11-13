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

from huffman import huffmanDecode

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9001

serverSocket.bind((host, port))
serverSocket.listen(10)

clientSocket, clientAddress = serverSocket.accept()
print("Client connected from", clientAddress, end="\n\n")

start = datetime.now()

fileName = clientSocket.recv(1024).decode("utf-8")

codes = pickle.loads(clientSocket.recv(102400))
encodedData = pickle.loads(clientSocket.recv(7500790))

with open(fileName, "w") as fp:
    fp.write(huffmanDecode(codes, encodedData))

end = datetime.now()

duration = end - start
print("The time taken to receive and decompress the file: %s seconds." % str(duration.seconds))
print("Number of bytes received: %s MiB." % str(os.path.getsize(fileName)/1000000))
print("File %s received successfully." % fileName)

clientSocket.close()
