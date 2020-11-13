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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Open the received file
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


# A class for the window box
class window(QWidget):
    # Init function for the class
    def __init__(self, parent=None, *argv, **kwargs):
        super(window, self).__init__(parent, *argv, **kwargs)

        # Get the Qt vertical box layout
        layout = QVBoxLayout()
        # Set the window title
        self.setWindowTitle("Server")

        # Get a Qt push button
        self.btn1 = QPushButton("View the received file")
        # Onclick of the button, open the received file
        self.btn1.clicked.connect(openFile)
        # Add the button to the layout
        layout.addWidget(self.btn1, alignment=Qt.AlignVCenter)
        # Set the layout of the window
        self.setLayout(layout)


# Main driver function for the server
if __name__ == "__main__":
    # Create a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Get the host name
    host = gethostname()
    # Get the port number
    port = 9001
    # Bind the server to the above host and port
    serverSocket.bind((host, port))
    # Listen for incoming connection requests
    serverSocket.listen(10)
    # Accept the incoming connection
    clientSocket, clientAddress = serverSocket.accept()

    # Receive the file name
    fileName = clientSocket.recv(1024).decode("utf-8")
    # Initial sequence is 0
    seq = 0

    # Open the file
    with open(fileName, "wb") as fp:
        # Run an infinite loop
        while True:
            # Receive the data
            recvData = clientSocket.recv(1048)
            # If no data was received
            if not recvData:
                # Break out of the loop
                break
            # Get the sequence number
            sequence = int(recvData[:24], 2)
            # If there is a sequence mismatch
            if seq != sequence:
                # Send for retransmission
                clientSocket.send(bytes("y", "utf-8"))
                # Continue the loop
                continue
            # Send not next sequence
            clientSocket.send(bytes("n", "utf-8"))
            # Increment the sequence
            seq += 1
            # Get the file data from the received data
            data = recvData[24:]
            # Write the file data
            fp.write(data)

    # Start a Qt application
    app = QApplication(sys.argv)
    # Initialize the window class
    ex = window()
    # Show the window
    ex.show()
    # Exit the application, on click of close
    sys.exit(app.exec_())
