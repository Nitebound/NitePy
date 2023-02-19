import socket
from threading import Thread


class ChatServer:
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

            ct = Thread(target=self.threaded_client, args=(conn,))
            ct.start()
            self.clients.append([conn, ct])

    def stop(self):
        print("Stopping server...")
        for client in self.clients:
            client.join()
        self.core.close()

    def threaded_client(self, conn):
        client_username = conn.recv(1024).decode('utf-8')
        print(client_username, "connected!")

        for client in self.clients:
            data = client_username + "|" + " <joined>"
            client[0].sendall(data.encode('utf-8'))

        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    # The client has disconnected if no message is received.
                    for client in self.clients:
                        data = client_username + "|" + " <disconnected>"
                        client[0].sendall(data.encode('utf-8'))
                        client[1].join()
                    break
                else:
                    for client in self.clients:
                        client.sendall(data)

            except Exception as e:
                print("Error:", e)
                break

        print(conn.getpeername(), "disconnected.")

        for client in self.clients:
            if client[0] == conn:
                self.clients.remove(client)

        conn.close()


if __name__ == "__main__":
    server = ChatServer("192.168.0.159", 8081)
    server.start()
    server.stop()

