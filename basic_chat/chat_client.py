import socket
from threading import Thread
import database_tools as dtools
import getpass as gpass


class ChatClient:
    def __init__(self, username):
        self.username = username
        self.core = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.core.setblocking(False)
        self.core.settimeout(30)
        self.server_addr = ()
        self.rcv_thread = None
        self._closing = False

    def connect(self, host, port):
        self.server_addr = (host, port)
        self.core.connect((host, port))
        print("Connected to:", self.server_addr)
        self.send(self.username.encode('utf-8'))

    def start_receive_thread(self):
        if self.rcv_thread is not None:
            self.rcv_thread.join()
        self.rcv_thread = Thread(target=self.threaded_receiver, args=())
        self.rcv_thread.start()

    def threaded_receiver(self):
        while True:
            if not self._closing:
                try:
                    data = self.core.recv(1024).decode('utf-8')
                    data_parts = data.split('|')
                    sender_username = data_parts[0]
                    message = data_parts[1]

                    if not data:
                        self.rcv_thread.join()
                        break
                    else:
                        print(sender_username, ":", message)

                except socket.timeout as _:
                    self.start_receive_thread()

    def close(self):
        print("Closing the connection...")
        self.core.close()
        self.rcv_thread.join()
        print("Connection closed")

    def send(self, data):
        self.core.sendall(data)

    def receive(self):
        data = self.core.recv(1024)
        return data

    def send_message(self, message):
        data = self.username + "|" + message
        self.send(data.encode('utf-8'))




def login_loop():
    _user = input("Username: ")
    _password = gpass.getpass(prompt="Password: ", stream=None)

    if dtools.login(_user, _password):
        print("Logged in as", _user)
        return _user
    else:
        print("Login failed... please try again")
        login_loop()


if __name__ == "__main__":
    user = login_loop()

    client = ChatClient(user)
    client.connect("192.168.0.102", 8081)
    client.start_receive_thread()

    while True:
        entry = input("")
        if entry == '*':
            client._closing = True
            break
        else:
            client.send_message(entry)

    client.close()
