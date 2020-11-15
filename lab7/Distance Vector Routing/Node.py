from socket import *
from time import sleep
from pickle import dumps, loads

from helperFunctions import getRTTServer, getRTTClient

errors = []


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.node = socket(AF_INET, SOCK_STREAM)

    def restart(self):
        self.node.close()
        self.node = socket(AF_INET, SOCK_STREAM)

    def server(self, data=None):
        self.node.bind((self.host, self.port))
        self.node.listen(10)
        for z in range(3):
            node1, addr = self.node.accept()
            if data is None:
                getRTTServer(node1)
            else:
                node1.send(dumps(data))
            node1.close()

    def client(self, host, data=None):
        sleep(1)
        while True:
            try:
                self.node.connect((host, self.port))
                if data is None:
                    return getRTTClient(self.node)
                else:
                    return loads(self.node.recv(10240))
            except Exception as e:
                errors.append(e)
