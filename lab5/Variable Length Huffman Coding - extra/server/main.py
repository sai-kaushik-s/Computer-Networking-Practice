r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
import socket
import pickle

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9001

serverSocket.bind((host, port))
serverSocket.listen(10)

clientSocket, clientAddress = serverSocket.accept()
print("Client connected from ", clientAddress, end="\n\n")

fileName = clientSocket.recv(1024).decode("utf-8")

huffman = pickle.loads(clientSocket.recv(102400))

fileData = ""
data = clientSocket.recv(1024).decode("utf-8")
while data:
    fileData += data
    data = clientSocket.recv(1024).decode("utf-8")

with open(fileName, "w") as fp:
    fp.write(huffman.decode(fileData))

clientSocket.close()
