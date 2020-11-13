from socket import *
from time import *


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.node = socket(AF_INET, SOCK_STREAM)

    def restart(self):
        self.node.close()
        self.node = socket(AF_INET, SOCK_STREAM)

    def server(self):
        self.node.bind((self.host, self.port))
        self.node.listen()
        node1, addr = self.node.accept()
        start = time()
        node1.send(bytes('1', 'utf-8'))
        node1.recv(8).decode('utf-8')
        end = time()
        rtt = str(end - start)
        node1.send(bytes(rtt, 'utf-8'))
        node1.close()

    def client(self, host):
        self.node.connect((host, self.port))
        self.node.recv(8).decode('utf-8')
        self.node.send(bytes('2', 'utf-8'))
        rtt = self.node.recv(1024).decode('utf-8')
        print(rtt)
