r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import os
import sys
from socket import *
import time
from verify import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# List of file names
fileName = []


# A function to send the file to the receiver
def sendFile():
    # Get the host name
    host = gethostname()
    # Get the port number
    port = 9001

    # Set the timeout to 2 seconds
    timeOut = 2

    # Copy the file path to the string
    filePath = fileName[0]

    # Create the client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect the socket to the appropriate host and port
    clientSocket.connect((host, port))

    # Extract the file name from the file path and send it to the receiver
    clientSocket.send(bytes(os.path.basename(filePath), "utf-8"))

    # Lower bound of the window
    base = 1
    # Next sequence number
    nextSeqN = 1
    # Window size extracted from the form
    windowSize = int(ex.windowSpinBar.text())
    # Create the window list
    window = []

    # Open the file
    fp = open(filePath, 'rb')
    # Read the data
    data = fp.read(1024)
    # Set done as False
    done = False
    # Get the time of the last acknowledgement
    lastAckTime = time.time()

    # While there exists data in the window or not done
    while not done or window:
        # If there exists a space in the window and file is not done
        if (nextSeqN < base + windowSize) and not done:
            # Create the send packet with the data and sequence number
            sendPacket = makePkt(nextSeqN, data)
            # Send the created packet
            clientSocket.send(sendPacket)
            # Go the the next sequence number
            nextSeqN = nextSeqN + 1
            # Append the send packet to the window
            window.append(sendPacket)
            # Read the next data
            data = fp.read(1024)
            # If data is not available
            if not data:
                # Done is true
                done = True
        # Try receiving the acknowledgement
        try:
            # Receive the acknowledgement
            packet = clientSocket.recv(4096)
            # Parse and verify the received data
            recvPacket, isCorrupt = parseAndVerify(packet)
            # If the data is not corrupted
            if not isCorrupt:
                # While receive packet greater than the lower bound and window is not empty
                while recvPacket[0] > base and window:
                    # Update the time of latest acknowledgement
                    lastAckTime = time.time()
                    # Delete the first window
                    del window[0]
                    # Increment the base as the previous index is removed
                    base = base + 1
        # Exception if there is no acknowledgement
        except Exception as e:
            # Print the exception
            print(e)
            # If the time difference is greater than timeout
            if time.time() - lastAckTime > timeOut:
                # Loop through the window
                for i in window:
                    # Send each packet in the widow
                    clientSocket.send(i)
    # Close the file
    fp.close()
    # Close the socket
    clientSocket.close()
    # Exit the application
    sys.exit(0)


# Get the file from the dialog box
def getFiles():
    # Open the file dialog box
    dlg = QFileDialog()
    # Ant type of file can be selected
    dlg.setFileMode(QFileDialog.AnyFile)

    # If any file is selected
    if dlg.exec_():
        # Get the list of filenames
        filenames = dlg.selectedFiles()
        # Append the filename to global variable
        fileName.append(filenames[0])


# Class of the file dialog window
class fileDialog(QWidget):
    # Init function for the class
    def __init__(self, parent=None, *argv, **kwargs):
        super(fileDialog, self).__init__(parent, *argv, **kwargs)

        # Select vertical layout
        layout = QVBoxLayout()
        # Set the window title
        self.setWindowTitle("Client")
        # Get a Qt group box
        self.formGroupBox = QGroupBox("Server")
        # Get a Qt Spin box
        self.windowSpinBar = QSpinBox()
        # Get a Qt push button
        self.btn1 = QPushButton("Select")
        # Onclick of button, get the files
        self.btn1.clicked.connect(getFiles)
        # Get a Qt button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        # Onclick of button, send the file
        self.buttonBox.accepted.connect(sendFile)
        # Create the form
        self.createForm()
        # Add the form Group Box to the window
        layout.addWidget(self.formGroupBox, alignment=Qt.AlignVCenter)

        # Set the layout of the window
        self.setLayout(layout)

    # Create the form
    def createForm(self):
        # Select the Qt form layout
        layout = QFormLayout()

        # Add a row for the window spin bar
        layout.addRow(QLabel("Window Size"), self.windowSpinBar)
        # Add a row for the file selection button
        layout.addRow(QLabel("File to be sent"), self.btn1)
        # Add a row for the button box
        layout.addRow(QLabel(""), self.buttonBox)
        # Set the layout of the form group box
        self.formGroupBox.setLayout(layout)


# Main driver function for the client
if __name__ == "__main__":
    # Start a Qt application
    app = QApplication(sys.argv)
    # Initialize the file dialog class
    ex = fileDialog()
    # Show the file dialog window
    ex.show()
    # Exit the application, on click of close
    sys.exit(app.exec_())
