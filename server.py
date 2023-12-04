# This code is a server that listens for incoming connections
# and handles client requests to receive files.
import io
# Importing Required Moidules
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
    # The class initializes an empty list,
    # clients, to keep track of connected clients.
    def __init__(self):
        self.clients = []

    # The clientHandler method is defined to handle each client connection separately
    def clientHandler(self, connection, addr):
        # Receive the client's data
        data = connection.recv(1024).decode()
        # connection.sendall("OK".encode())
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
            # Receive the file data in chunks
            # until no more data is received.
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
                thread.start()


# The main function is defined to instantiate a Server object
# and start the server when the script is executed as the main program.
def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
