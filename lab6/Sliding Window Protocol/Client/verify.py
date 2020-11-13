r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import hashlib
import pickle


# Get the md5 encoding of the input message
def getHash(packet):
    # MD5 is an algorithm used to generate a unique hash encoding of the source data
    h = hashlib.md5()
    # Update the source to the packet, which is a list of the sequence number and the data
    h.update(pickle.dumps(packet))
    # Return the encoded message
    return h.digest()


# Parse and verify the message
def parseAndVerify(packet):
    # Loads the pickled data
    recvPacket = pickle.loads(packet)
    # Store the hashed data
    c = recvPacket[-1]
    # Delete the hashed data
    del recvPacket[-1]
    # Get the md5 encoding of the received message and compare it to the encoding received
    isCorrupt = getHash(recvPacket) != c
    # Return the received packet and bool value whether the data is corrupted
    return recvPacket, isCorrupt


# Make the packet and encode it
def makePkt(seqN, data):
    # Create a list of sequence number and data
    packet = [seqN, data]
    # Get the hash encoding of the packet
    hashData = getHash(packet)
    # Append the hash encoding to the packet
    packet.append(hashData)
    # Return the pickle dump of the packet
    return pickle.dumps(packet)
