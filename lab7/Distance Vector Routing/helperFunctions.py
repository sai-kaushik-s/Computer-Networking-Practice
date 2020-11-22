# A function to print the routing table
def printDict(routingTable):
    print("{:<15} {:<25} {:<10}".format('Destination', 'RTT', 'Next Hop'))
    for _ in range(4):
        print("{:<15} {:<25} {:<10}".format('node' + str(_+1), routingTable["rtt"][_], routingTable["next hop"][_]))
