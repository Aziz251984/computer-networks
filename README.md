# computer-networks
this is the computer networks final project
so here is explanation for my code to send files csv json and image to the server
#servercode_comment
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
timeout = 100

# The Server class is defined to manage client connections and file handling.
class Server:
    # The class initializes an empty list, clients, to keep track of connected clients.
    def __init__(self):
        self.clients = []

    # The clientHandler method is defined to handle each client connection separately.
    def clientHandler(self, connection, addr):
        # Receive the client's data
        data = connection.recv(1024).decode()
        
        # and extract the client name, file name, and file type from a JSON object
        try:
            fileDetails = json.loads(data)
            clientName = fileDetails["name"]
            fileName = fileDetails["fileName"]
            fileType = fileDetails["fileType"]

            # Measures the start time of the file transfer.
            startTime = time.time()

            # Send an acknowledgment message, 'OK', back to the client.
            connection.sendall("OK".encode())

            receivedData = b""
            
            # Receive the file data in chunks until no more data is received.
            while True:
                chunk = connection.recv(1024)
                if not chunk:
                    break
                receivedData += chunk
            
            # Measures the end time of the file transfer and calculates the latency.
            endTime = time.time()
            latency = endTime - startTime

            print(f"Received '{fileType}' file '{fileName}' from '{clientName}'.")
            print(f"-> Latency: {latency} seconds")

            # Depending on the file type, it performs different operations:

            # If the file type is 'image',
            if fileType == "image":
                # it reconstructs the image from the received data,
                img = Image.frombytes('RGBA', (377, 369), receivedData, 'raw')
                
                # displays it,
                img.show()
                
                # and saves it to a file.
                img.save(f"{fileName}_{startTime}.png")

            # If the file type is 'csv',
            elif fileType == "csv":
                # it saves the received data to a CSV file
                with open(f"{fileName}_{startTime}.csv", "wb") as file:
                    file.write(receivedData)
                
                # and prints the content of the file row by row.
                with open(f"{fileName}_{startTime}.csv", "r") as file:
                    csvData = csv.reader(file)
                    for row in csvData:
                        print(row)

            # If the file type is 'json',
            elif fileType == "json":
                # it saves the received data to a JSON file
                with open(f"{fileName}_{startTime}.json", "wb") as file:
                    file.write(receivedData)
                
                # and prints the JSON data.
                with open(f"{fileName}_{startTime}.json", "r") as file:
                    jsonData = json.load(file)
                    print(jsonData)

        # If a JSON decoding error occurs, print an error message.
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")

        # Close the connection.
        connection.close()

    # The start function is defined to start the server.
    def start(self):
        print("Server initialized")
        
        # It binds the socket to the server's IP address and port.
        with socket(AF_INET, SOCK_STREAM) as sock:
            # It binds the socket to the server's IP address and port.
            sock.bind((serverIP, serverPort))
            
            # It starts listening for incoming connections.
            sock.listen()
            
            # In an infinite loop,
            while True:
                # it accepts a client connection,
                connection, addr = sock.accept()
                
                # prints the connected client's address,
                print(f"Connected to {addr}")

                # and starts a new thread to handle the client using the clientHandler method.
                thread = threading.Thread(target=self.clientHandler, args=(connection, addr))
                thread.star
#code_client_explanation
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
    # it also receives a response from the server
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
    # and handle user input.
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


# If the script is executed as the main program, call the main function.
if __name__ == "__main__":
    main()
