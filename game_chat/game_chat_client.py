from threading import Thread
import getpass as gpass
import socket
import nite_engine as ne
from nite_engine.display import *
from nite_engine.db_tools import *
from nite_engine.ui import *


class ChatClient:
    def __init__(self, username):
        self.username = username
        self.core = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.core.setblocking(0)
        self.core.settimeout(30)
        self.server_addr = ()
        self.rcv_thread = None

    def connect(self, host, port):
        self.server_addr = (host, port)
        self.core.connect((host, port))
        print("Connected to:", self.server_addr)
        self.send(self.username.encode('utf-8'))

    def start_receive_thread(self):
        self.rcv_thread = Thread(target=self.threaded_receiver, args=())
        self.rcv_thread.start()

    def threaded_receiver(self):
        while True:
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

            except socket.timeout as e:
                self.start_receive_thread()

            except Exception as e:
                break

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


if __name__ == "__main__":
    display = Display((1024, 768), "Nite-Chat")
    running = True

    ui_manager = UIManager()
    UIManager.DEBUGMODE = False
    UIManager.default_font = ne.font.SysFont("Arial", 18)
    test_entry = ui_manager.create_element("entry")
    test_entry.rect = (0, 0, 200, 20)

    while running:
        # EVENT
        events = ne.event.get()
        for event in events:
            if event.type == ne.QUIT:
                running = False

            elif event.type == ne.KEYDOWN:
                if event.key == ne.K_ESCAPE:
                    running = False

        ui_manager.on_event(events)

        # UPDATE
        ui_manager.on_update(display.dt)

        # DRAW
        display.clear((255, 255, 255))
        ui_manager.on_draw(display.surface)
        display.update()
