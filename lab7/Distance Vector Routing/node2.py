from Node import Node
from constants import *
from helperFunctions import printDict


if __name__ == "__main__":
    node2RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node1", "node3", "node4"]
    node2 = Node(IP2, PORT)
    node2RT["rtt"].append(node2.client(IP1))
    print("node1, node2: " + node2RT["rtt"][-1])
    node2.restart()
    node2.server()
    node2RT["rtt"].append("0")
    print("node2, node2: " + node2RT["rtt"][-1])
    node2.restart()
    node2RT["rtt"].append(node2.client(IP3))
    print("node3, node2: " + node2RT["rtt"][-1])
    node2.restart()
    node2RT["rtt"].append(node2.client(IP4))
    print("node4, node2: " + node2RT["rtt"][-1])
    node2.restart()
