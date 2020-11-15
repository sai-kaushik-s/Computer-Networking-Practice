from Node import Node
from constants import *
from helperFunctions import printDict


if __name__ == "__main__":
    node3RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node1", "node2", "node4"]
    node3 = Node(IP3, PORT)
    node3RT["rtt"].append(node3.client(IP1))
    print("node1, node3: " + node3RT["rtt"][-1])
    node3.restart()
    node3RT["rtt"].append(node3.client(IP2))
    print("node2, node3: " + node3RT["rtt"][-1])
    node3.restart()
    node3.server()
    node3RT["rtt"].append("0")
    print("node3, node3: " + node3RT["rtt"][-1])
    node3.restart()
    node3RT["rtt"].append(node3.client(IP4))
    print("node4, node3: " + node3RT["rtt"][-1])
    node3.restart()
