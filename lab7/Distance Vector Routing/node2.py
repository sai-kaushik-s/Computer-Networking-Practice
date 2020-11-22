from Node import Node
from constants import *
from helperFunctions import printDict


# A function to send and receive Routing Tables
def sendRecvRTT():
    n1 = node2.recvRTT(IP1)
    node2.restart()
    node2.sendRTT(node2RT["rtt"])
    node2.restart()
    n3 = node2.recvRTT(IP3)
    node2.restart()
    n4 = node2.recvRTT(IP4)
    node2.restart()
    return n1, n3, n4


# A function to update the routing table
def updateRTTList():
    for _ in range(4):
        minList = []
        if node2RT["rtt"][_] != "0":
            minList.append(float(node2RT["rtt"][0]) + float(node1[_]))
            minList.append(float(node2RT["rtt"][2]) + float(node3[_]))
            minList.append(float(node2RT["rtt"][3]) + float(node4[_]))
            node2RT["rtt"][_] = str(min(minList))
            node2RT["next hop"][_] = nextOptions[minList.index(min(minList))]


# Main driver function of node2
if __name__ == "__main__":
    node2RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node1", "node3", "node4"]
    # Get RTT from node2 to node1, node3 and node4
    node2 = Node(IP2, PORT)
    node2RT["rtt"].append(node2.client(IP1))
    node2.restart()
    node2.server()
    node2RT["rtt"].append("0")
    node2.restart()
    node2RT["rtt"].append(node2.client(IP3))
    node2.restart()
    node2RT["rtt"].append(node2.client(IP4))
    node2.restart()
    print("Initial Routing Table: ")
    printDict(node2RT)
    print("")
    # Get routing table and update it
    for i in range(3):
        node2.port += 1
        node1, node3, node4 = sendRecvRTT()
        updateRTTList()
        print("Iteration {it}: ".format(it=str(i+1)))
        printDict(node2RT)
        print("")
        node2.restart()
