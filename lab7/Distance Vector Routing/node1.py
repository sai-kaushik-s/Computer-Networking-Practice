from Node import Node
from constants import *
from helperFunctions import printDict


if __name__ == "__main__":
    node1RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node2", "node3", "node4"]
    node1 = Node(IP1, PORT)
    node1.server()
    node1RT["rtt"].append("0")
    print("node1, node1: " + node1RT["rtt"][-1])
    node1.restart()
    node1RT["rtt"].append(node1.client(IP2))
    print("node2, node1: " + node1RT["rtt"][-1])
    node1.restart()
    node1RT["rtt"].append(node1.client(IP3))
    print("node3, node1: " + node1RT["rtt"][-1])
    node1.restart()
    node1RT["rtt"].append(node1.client(IP4))
    print("node4, node1: " + node1RT["rtt"][-1])
    node1.restart()
