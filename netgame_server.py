import socket
from _thread import *
from player import Player
import pickle
import toolkit as tools


class NetgameServer:
    def __init__(self, host, port):
        self.host, self.port = self.address = host, port
        self.core = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.core.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.clients = []

    def start(self):
        try:
            print("Starting server...")
            self.core.bind(self.address)

        except socket.error as ex:
            print("Error starting the server: ", ex)

        self.core.listen(6)
        # Continue to listen for, and accept connections with clients.
        while True:
            conn, addr = self.core.accept()
            print("Connected to:", addr)
            self.clients.append(conn)

            for client in self.clients:
                print(client.getpeername())

            start_new_thread(self.threaded_client, (conn,))

    def stop(self):
        print("Stopping server...")
        self.core.close()

    def echo_all(self, data):
        for client in self.clients:
            client.sendall(data)

    def threaded_client(self, conn):
        # For each client that connects, a new thread is started which handles the connection to it
        # until the connection ends.
        reply = ""

        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    # The client has disconnected if no message is received.
                    break
                else:
                    # Do something with the received data
                    reply = str("Server received:" + data.decode("UTF-8")).encode("UTF-8")
                    print("Received: ", data)
                    print("Sending : ", reply)

                self.echo_all(reply)
                #conn.sendall(reply)  # Send data back to the client.

            except Exception as e:
                print("Error:", e)
                break

        print(conn.getpeername(), "disconnected.")
        self.clients.remove(conn)
        conn.close()


if __name__ == "__main__":
    server = NetgameServer("192.168.0.159", 8081)
    server.start()
    server.stop()

