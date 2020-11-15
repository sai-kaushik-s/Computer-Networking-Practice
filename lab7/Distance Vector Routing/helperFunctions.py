from time import time, sleep
from random import randint


def getRTTServer(node1):
    start = time()
    sleep(randint(3, randint(4, 9))/10)
    for i in range(100):
        node1.send(bytes('1', 'utf-8'))
    node1.recv(8).decode('utf-8')
    end = time()
    rtt = str((end - start) / 100)
    node1.send(bytes(rtt, 'utf-8'))


def getRTTClient(node1):
    for i in range(100):
        node1.recv(1).decode('utf-8')
    node1.send(bytes('2', 'utf-8'))
    return node1.recv(1024).decode('utf-8')
