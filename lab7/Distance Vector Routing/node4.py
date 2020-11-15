from Node import Node, PORT


def getRTTList(n4):
    n1 = n4.client('127.0.0.1', data=[])
    n4.restart()
    n2 = n4.client('127.0.0.2', data=[])
    n4.restart()
    n3 = n4.client('127.0.0.3', data=[])
    n4.restart()
    n4.server(data=node4RT["rtt"])
    n4.restart()
    return n1, n2, n3


def updateRTTList():
    for _ in range(4):
        minList = []
        if node4RT["rtt"][_] != "0":
            minList.append(float(node4RT["rtt"][0]) + float(node1[_]))
            minList.append(float(node4RT["rtt"][1]) + float(node2[_]))
            minList.append(float(node4RT["rtt"][2]) + float(node3[_]))
            node4RT["rtt"][_] = str(min(minList))
            node4RT["next hop"][_] = nextOptions[minList.index(min(minList))]


if __name__ == "__main__":
    node4RT = {
            "rtt": [],
            "next hop": ["node1", "node2", "node3", "node4"]
        }
    nextOptions = ["node1", "node2", "node3"]
    node4 = Node('127.0.0.4', PORT)
    node4RT["rtt"].append(node4.client('127.0.0.1'))
    print("node1, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4RT["rtt"].append(node4.client('127.0.0.2'))
    print("node2, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4RT["rtt"].append(node4.client('127.0.0.3'))
    print("node3, node4: " + node4RT["rtt"][-1])
    node4.restart()
    node4.server()
    node4RT["rtt"].append("0")
    print("node4, node4: " + node4RT["rtt"][-1])
    node4.restart()
    for i in range(3):
        node4.port += 1
        node1, node2, node3 = getRTTList(node4)
        updateRTTList()
        print(node4RT)
