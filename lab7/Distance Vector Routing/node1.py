from Node import Node
from constants import *
from helperFunctions import printDict


# A function to send and receive Routing Tables
def sendRecvRTT():
    node1.sendRTT(node1RT["rtt"])
    node1.restart()
    n2 = node1.recvRTT(IP2)
    node1.restart()
    n3 = node1.recvRTT(IP3)
    node1.restart()
    n4 = node1.recvRTT(IP4)
    node1.restart()
    return n2, n3, n4


# A function to update the routing table
def updateRTTList():
    for _ in range(4):
        minList = []
        if node1RT["rtt"][_] != "0":
            minList.append(float(node1RT["rtt"][1]) + float(node2[_]))
            minList.append(float(node1RT["rtt"][2]) + float(node3[_]))
            minList.append(float(node1RT["rtt"][3]) + float(node4[_]))
            node1RT["rtt"][_] = str(min(minList))
            node1RT["next hop"][_] = nextOptions[minList.index(min(minList))]


# Main driver function of node1
if __name__ == "__main__":
    node1RT = {
        "rtt": [],
        "next hop": ["node1", "node2", "node3", "node4"]
    }
    nextOptions = ["node2", "node3", "node4"]
    # Get RTT from node1 to node2, node3 and node4
    node1 = Node(IP1, PORT)
    node1.server()
    node1RT["rtt"].append("0")
    node1.restart()
    node1RT["rtt"].append(node1.client(IP2))
    node1.restart()
    node1RT["rtt"].append(node1.client(IP3))
    node1.restart()
    node1RT["rtt"].append(node1.client(IP4))
    node1.restart()
    print("Initial Routing Table: ")
    printDict(node1RT)
    print("")
    # Get routing table and update it
    for i in range(3):
        node1.port += 1
        node2, node3, node4 = sendRecvRTT()
        updateRTTList()
        print("Iteration {it}: ".format(it=str(i+1)))
        printDict(node1RT)
        print("")
        node1.restart()
