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
from time import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# A function to get the files
def getFiles():
    # Open the file dialog box
    dlg = QFileDialog()
    # Select all types of files
    dlg.setFileMode(QFileDialog.AnyFile)
    # If any file is selected in the dialog box
    if dlg.exec_():
        # Get the list of files selected
        filenames = dlg.selectedFiles()
        # Transfer the selected file
        fileTransfer(filenames[0])


# A function to the transfer the file to the receiver
def fileTransfer(filePath):
    # Create the client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Get the host name
    host = gethostname()
    # Get a port number
    port = 9001
    # Connect the client to the required host and port
    clientSocket.connect((host, port))
    # Open the file in read binary mode
    with open(filePath, 'rb') as fp:
        # Get the file name from the file path and send it
        clientSocket.send(bytes(os.path.basename(filePath), "utf-8"))
        # Initialize sequence to 0
        sequence = 0
        # Read the data
        data = fp.read(1024)
        # Run an infinite loop
        while True:
            # Convert the integer to binary and fill up to 24 bits
            sendData = bytes(format(sequence, 'b').zfill(24), "utf-8")
            # Add the data to the send data
            sendData += data
            # Send the send data
            clientSocket.send(sendData)
            # Get the current start time
            start = time()
            # Run an infinite loop
            while True:
                # Get the current end time
                end = time()
                # If the time difference is less than 5 seconds
                if end - start < 5:
                    # Try
                    try:
                        # Receive the acknowledgement
                        ack = clientSocket.recv(8).decode("utf-8")
                        # Break out of the loop
                        break
                    # If any exception occurs
                    except Exception as e:
                        # Print the exception
                        print(e)
                # If the time difference reaches 5 seconds
                else:
                    # Acknowledgement is yes
                    ack = "y"
                    # Break out of the loop
                    break
            # If the acknowledgement is "y"
            if ack == "y":
                # Retransmit the data
                continue
            # Read the next data in the file
            data = fp.read(1024)
            # If there is no data left
            if not data:
                # Break out of the loop
                break
            # Increment the current sequence number
            sequence += 1
    # Close the socket
    clientSocket.close()
    # Exit the program
    sys.exit()


# A class for the file dialog box
class fileDialog(QWidget):
    # Init function for the class
    def __init__(self, parent=None, *argv, **kwargs):
        super(fileDialog, self).__init__(parent, *argv, **kwargs)

        # Get the Qt vertical box layout
        layout = QVBoxLayout()
        # Set the window title
        self.setWindowTitle("Client")

        # Get the Qt push button
        self.btn1 = QPushButton("Select a file to send")
        # Onclick of the button, one file dialog
        self.btn1.clicked.connect(getFiles)
        # Add the button to the layout
        layout.addWidget(self.btn1, alignment=Qt.AlignVCenter)
        # Set the layout of the window
        self.setLayout(layout)


# Main driver program of the client
if __name__ == '__main__':
    # Start a Qt application
    app = QApplication(sys.argv)
    # Initialize the file dialog class
    ex = fileDialog()
    # Show the file dialog window
    ex.show()
    # Exit the application, on click of close
    sys.exit(app.exec_())
