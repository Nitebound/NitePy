import socket as sk
import tkinter as tk
from threading import Thread


class ChatServer:
    def __init__(self, host, port):
        self.host, self.port = self.address = host, port
        self.core = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.core.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, True)
        self.clients = []

    def start(self):
        try:
            print("Starting server...")
            self.core.bind(self.address)

        except sk.error as ex:
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
                        client[0].sendall(data)

            except Exception as e:
                print("Error:", e)
                break

        print(conn.getpeername(), "disconnected.")

        for client in self.clients:
            if client[0] == conn:
                self.clients.remove(client)

        conn.close()


class TKApp(tk.Tk):
    default_font = "Times New Roman"
    default_font_size = 12

    def __init__(self,  title, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.geometry("250x100")
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self, text="Server Control Panel")
        self.title_label['font'] = (TKApp.default_font, TKApp.default_font_size)
        self.title_label['fg'] = "black"
        self.title_label.pack()
        self.state_label = tk.Label(self, text="Server is offline")

        self.state_label['bg'] = "orange"
        self.state_label['fg'] = "white"
        self.state_label['font'] = (TKApp.default_font, TKApp.default_font_size)
        self.state_label['padx'] = 150
        self.state_label.pack()

        self.subframe1 = tk.Frame(self)
        self.toggle_button = tk.Button(self.subframe1, text="Start", command=self.toggle_state)
        self.toggle_button['font'] = (TKApp.default_font, TKApp.default_font_size)
        self.toggle_button.pack(fill=tk.X)
        self.subframe1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.subframe2 = tk.Frame(self)
        self.config_button = tk.Button(self.subframe2, text="Configure")
        self.config_button['font'] = (TKApp.default_font, TKApp.default_font_size)
        self.config_button.pack(fill=tk.X)
        self.subframe2.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.server = ChatServer("192.168.0.159", 8080)

    def threaded_server(self):
        self.server.start()

    def toggle_state(self):
        if self.toggle_button['text'] == "Start":
            self.toggle_button['text'] = "Stop"
            self.state_label['text'] = "Server is online"
            self.state_label['bg'] = "green"
            self.server_thread = Thread(target=self.threaded_server, args=())
            self.server_thread.start()

        elif self.toggle_button['text'] == "Stop":
            self.toggle_button['text'] = "Start"
            self.state_label['text'] = "Server is offline"
            self.state_label['bg'] = "orange"
            self.server.stop()
            self.server_thread.join()

server_app = TKApp("Nite Server")
server_app.mainloop()
