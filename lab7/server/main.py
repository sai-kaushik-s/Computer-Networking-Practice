from threading import *
from Node import Node


def getRTT(node1, node2):
    serverThread = Thread(target=node1.server)
    serverThread.start()
    clientThread = Thread(target=node2.client, args=(node1.host,))
    clientThread.start()
    serverThread.join()
    clientThread.join()
    node1.restart()
    node2.restart()


if __name__ == "__main__":
    nodes = {
        "node1": Node('127.0.0.1', 9001),
        "node2": Node('127.0.0.2', 9001),
        "node3": Node('127.0.0.3', 9001),
        "node4": Node('127.0.0.4', 9001)
    }

    for i, x in nodes.items():
        for j, y in nodes.items():
            if i != j:
                print(i, j, end=": ")
                getRTT(x, y)
