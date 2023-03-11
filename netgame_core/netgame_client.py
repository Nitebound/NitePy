import socket
import pickle


# If pickle is used, objects can be sent as bytes, and will be reconstructed upon being received.
class NetgameClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)

    def connect(self):
        print("Connecting to server...")
        try:
            self.client.connect(self.address)
            print("Connected to", self.address)

        except Exception as e:
            print("Could not connect to", self.address)
            print("Error:", e)

    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv(2048)

        except socket.error as e:
            print("Error:", e)

    