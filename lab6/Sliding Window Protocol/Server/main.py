r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import os
import platform
import subprocess
import sys
from socket import *
import time
from verify import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Open the file in the default application
def openFile():
    # If the platform is Windows
    if platform.system() == 'Windows':
        # Start the file
        os.startfile(fileName)
    # If the platform is Linux
    else:
        # Call the file
        subprocess.call(('xdg-open', fileName))
    # Exit the program
    sys.exit()


# Class of the server window
class window(QWidget):
    # Init function for the class
    def __init__(self, parent=None, *argv, **kwargs):
        super(window, self).__init__(parent, *argv, **kwargs)

        # Select vertical layout
        layout = QVBoxLayout()
        # Let the window title
        self.setWindowTitle("Server")
        # Get a Qt push button
        self.btn1 = QPushButton("View the received file")
        # Onclick of the button, view the file
        self.btn1.clicked.connect(openFile)
        # Add the button to the layout
        layout.addWidget(self.btn1, alignment=Qt.AlignVCenter)

        # Set the layout of the window
        self.setLayout(layout)


# Main driver function for the server
if __name__ == "__main__":
    # Get the host name
    host = gethostname()
    # Get the port number
    port = 9001

    # Create the server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind the server to the host and port
    serverSocket.bind((host, port))

    # Listen for connection requests
    serverSocket.listen(10)
    # Accept the connection request from a client
    clientSocket, clientAddress = serverSocket.accept()

    # Expected sequence number
    expSeqN = 1

    # Receive the file name
    fileName = clientSocket.recv(1024).decode("utf-8")

    # Open the file
    fp = open(fileName, "wb")
    # Initialize is EOF as false
    isEOF = False
    # Get the time of the last packet time
    lastPacketTime = time.time()

    # Run an infinite loop
    while True:
        # If eof is reached
        if isEOF:
            # Break out of the loop
            break
        # Try
        try:
            # Receive the file file packet
            packet = clientSocket.recv(4096)
            # Parse and verify the received packet
            recvPacket, isCorrupt = parseAndVerify(packet)
            # If the received data is not corrupted
            if not isCorrupt:
                # If the received sequence number is the same as expected sequence number
                if recvPacket[0] == expSeqN:
                    # If the file data exists
                    if recvPacket[1]:
                        # Write the data
                        fp.write(recvPacket[1])
                    # If file data does not exits
                    else:
                        # EOF is reached
                        isEOF = True
                    # Increment the expected sequence number
                    expSeqN = expSeqN + 1
                    # Make the acknowledgement packet
                    sendPacket = makeACK(expSeqN)
                    # Send the acknowledgement packet
                    clientSocket.send(sendPacket)
                # If sequence numbers is mismatched
                else:
                    # Make the acknowledgement packet
                    sendPacket = makeACK(expSeqN)
                    # Send the acknowledgement packet
                    clientSocket.send(sendPacket)
        # If the file was not received
        except Exception as e:
            # Print the error
            exceptions = [e]
            break
    # Close the file
    fp.close()

    # Start a Qt application
    app = QApplication(sys.argv)
    # Initialize the window class
    ex = window()
    # Show the window
    ex.show()
    # Exit the application, on click of close
    sys.exit(app.exec_())
