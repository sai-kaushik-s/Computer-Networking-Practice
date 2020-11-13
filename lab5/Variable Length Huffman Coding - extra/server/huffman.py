r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
import heapq


class Node:
    def __init__(self, frequency, character=None):
        self.left = None
        self.right = None
        self.frequency = frequency
        self.character = character

    def encode(self, encoding):
        if self.left is None and self.right is None:
            yield self.character, encoding
        else:
            for v in self.left.encode(encoding + '0'):
                yield v
            for v in self.right.encode(encoding + '1'):
                yield v

    def __lt__(self, other):
        return self.frequency < other.frequency


class Huffman:
    def __init__(self, text):
        self.text = text

        frequency = {}
        for it in self.text:
            if it in frequency:
                frequency[it] += 1
            else:
                frequency[it] = 1

        priorityQueue = []
        for char in frequency:
            priorityQueue.append(Node(frequency[char], char))

        heapq.heapify(priorityQueue)

        if len(priorityQueue) == 1:
            self.root = Node(1)
            self.root.left = priorityQueue[0]
            self.encoding = {priorityQueue[0].character: '0'}
            return

        while len(priorityQueue) > 1:
            node1 = heapq.heappop(priorityQueue)
            node2 = heapq.heappop(priorityQueue)
            node3 = Node(node1.frequency + node2.frequency)
            node3.left = node1
            node3.right = node2
            heapq.heappush(priorityQueue, node3)

        self.root = priorityQueue[0]
        self.encoding = {}

        for char, code in self.root.encode(""):
            self.encoding[char] = code

    def __repr__(self):
        return "Huffman encoding of " + self.text + ": " + str(self.encoding)

    def encode(self):
        bits = ""
        for it in self.text:
            bits += self.encoding[it]
        return bits

    def decode(self, bits):
        node = self.root
        data = ""
        for it in bits:
            if it == "0":
                node = node.left
            else:
                node = node.right
            if node.character:
                data += node.character
                node = self.root
        return data
