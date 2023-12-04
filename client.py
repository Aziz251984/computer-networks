# This code is a client program that allows a user to send files
# (image, CSV, JSON) to a server. The client uses sockets
# to establish a connection with the server and send the file data

# Importing Required Modules
# The socket module is imported from the socket package to create and manage sockets.
from socket import *
# The json module is imported to handle JSON encoding and decoding.
import json
# The threading module is imported to enable concurrent handling of multiple client connections.
import threading
# The time module is imported to measure the latency of file transfers.
import time
# The csv module is imported to handle CSV file operations.
import csv
# The PIL module (Python Imaging Library) is imported to handle image-related operations.
from PIL import Image

# Server configuration
# Server IP corresponds to the loopback interface (localhost).
serverIP = '127.0.0.1'
# Server Port
serverPort = 8080
# Server timeout
tout = 100


# This class contains all the functionalities needed to create a client object
class Client:
    # initialize the client's name
    def __init__(self, name):
        self.name = name

    # function to send the meta information and files,
    # it also recieves responce from server
    def sendFiles(self, fileName, data, fileType):
        # A socket is created
        with socket(AF_INET, SOCK_STREAM) as sock:
            # The socket attempts to connect
            # to the server using the IP address and port number specified.
            try:
                sock.connect((serverIP, serverPort))
                # sock.timeout
            # If a connection error occurs, an exception is caught
            # and an error message is printed.
            except error as e:
                print(f"Connection Error: {e}")
                return
            # The file metadata (name, fileName, fileType) is defined
            # as a dictionary and sent to the server as a JSON-encoded
            # string.
            fileMeta = {
                "name": self.name,
                "fileName": fileName,
                "fileType": fileType,

            }

            sock.sendall(json.dumps(fileMeta).encode())
            # The client waits to receive a response from the server.
            response = sock.recv(1024).decode()
            print(response)

            # If the response is "OK", the file data is sent to the server.
            if response == "OK":
                sock.sendall(data)
            print("data sent")
            # Finally, the socket is closed.
            sock.close()

    # This method is defined to display a menu to the user
    #  and handle user input.
    def startMenu(self):
        print("Client Initialized.")
        print("Menu:")
        # The menu options include sending
        # an image,
        print("1. Send Image")
        # a CSV file,
        print("2. Send CSV")
        # a JSON file,
        print("3. Send JSON")
        # or exiting.
        print("4. Exit")

        # Depending on the user's choice,
        # the corresponding file is read,
        # encoded, and sent to the server
        # using the sendFiles method.
        while True:
            choice = input("Choose your option (1-4): ")

            if choice == '1':
                fileName = input("Enter the image file name: ")
                try:
                    img = Image.open(fileName)
                    print(img.size)
                    # img.show()
                    imgData = img.tobytes()
                    self.sendFiles(fileName, imgData, 'image')
                except FileNotFoundError:
                    print("ERROR: Image file not found")
                except Exception as error:
                    print(f"ERROR: {error}")

            elif choice == "2":
                fileName = input("Enter the CSV file name: ")
                try:
                    with open(fileName, 'r') as file:
                        csvData = file.read().encode()
                        self.sendFiles(fileName, csvData, 'csv')
                except FileNotFoundError:
                    print("ERROR: CSV file not found.")
                except Exception as error:
                    print(f"ERROR: {error}")

            elif choice == '3':
                fileName = input("Enter the JSON file name: ")
                try:
                    with open(fileName, 'r') as file:
                        jsonData = file.read().encode()
                        self.sendFiles(fileName, jsonData, 'json')
                except FileNotFoundError:
                    print("ERROR: JSON file not found")
                except Exception as error:
                    print(f"ERROR: {error}")

            elif choice == '4':
                print("Exiting")
                break
            else:
                print("Invalid choice. Please try again.")


# The main function prompts the user to enter their name,
# creates an instance of the Client class, and calls the startMenu method.
def main():
    name = input("Enter your name: ")
    client = Client(name)
    client.startMenu()


if __name__ == "__main__":
    main()
