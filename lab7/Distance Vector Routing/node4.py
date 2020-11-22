from Node import Node
from constants import *
from helperFunctions import printDict


# A function to send and receive Routing Tables
def sendRecvRTT():
    n1 = node4.recvRTT(IP1)
    node4.restart()
    n2 = node4.recvRTT(IP2)
    node4.restart()
    n3 = node4.recvRTT(IP3)
    node4.restart()
    node4.sendRTT(node4RT["rtt"])
    node4.restart()
    return n1, n2, n3


# A function to update the routing table
def updateRTTList():
    for _ in range(4):
        minList = []
        if node4RT["rtt"][_] != "0":
            minList.append(float(node4RT["rtt"][0]) + float(node1[_]))
            minList.append(float(node4RT["rtt"][1]) + float(node2[_]))
            minList.append(float(node4RT["rtt"][2]) + float(node3[_]))
            node4RT["rtt"][_] = str(min(minList))
            node4RT["next hop"][_] = nextOptions[minList.index(min(minList))]


# Main driver function of node4
if __name__ == "__main__":
    node4RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node1", "node2", "node3"]
    # Get RTT from node4 to node1, node2 and node3
    node4 = Node(IP4, PORT)
    node4RT["rtt"].append(node4.client(IP1))
    node4.restart()
    node4RT["rtt"].append(node4.client(IP2))
    node4.restart()
    node4RT["rtt"].append(node4.client(IP3))
    node4.restart()
    node4.server()
    node4RT["rtt"].append("0")
    node4.restart()
    print("Initial Routing Table: ")
    printDict(node4RT)
    print("")
    # Get routing table and update it
    for i in range(3):
        node4.port += 1
        node1, node2, node3 = sendRecvRTT()
        updateRTTList()
        print("Iteration {it}: ".format(it=str(i+1)))
        printDict(node4RT)
        print("")
        node4.restart()
