from Node import Node
from constants import *
from helperFunctions import printDict


if __name__ == "__main__":
    node4RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node1", "node2", "node3"]
    node4 = Node(IP4, PORT)
    node4RT["rtt"].append(node4.client(IP1))
    print("node1, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4RT["rtt"].append(node4.client(IP2))
    print("node2, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4RT["rtt"].append(node4.client(IP3))
    print("node3, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4.server()
    node4RT["rtt"].append("0")
    print("node4, node4: " + node4RT["rtt"][-1])
    node4.restart()

