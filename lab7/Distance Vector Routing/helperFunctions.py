from time import time


def getRTTServer(node1):
    start = time()
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


def printDict(routingTable):
    print("{:<10} {:<10} {:<10}".format('Destination', 'RTT', 'Next Hop'))
    for _ in range(4):
        print("{:<10} {:<10} {:<10}".format('node' + str(_+1), routingTable["rtt"][_], routingTable["next hop"][_]))
