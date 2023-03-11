import tkinter as tk
from tkinter import ttk


class TKApplication(tk.Tk):
    def __init__(self,  title, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title
        self.wm_title(title)

        # Create a frame and assign it to a container.
        container = tk.Frame(self, height=400, width=600)

        # Define where the container is packed to.
        container.pack(side="top", fill="both", expand=True)

        # Configure the location of the container using a grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of frames
        self.frames = {}

        # Create the frames within the app window.
        for frame_def in (MainPage, SidePage, CompletionScreen):
            frame = frame_def(container, self)

            # This class acts as the root window for all the frames.
            self.frames[frame_def] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, container):
        frame = self.frames[container]
        # Raise the frame to the top
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # super().__init__(self, parent)
        label = tk.Label(self, text="Main Page")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Open Side Page",
            command=lambda: controller.show_frame(SidePage)
        )

        switch_window_button.pack(side="bottom", fill=tk.X)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        # super().__init__(self, parent)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Side Page")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Open Completion Page",
            command=lambda: controller.show_frame(CompletionScreen)
        )

        switch_window_button.pack(side="bottom", fill=tk.X)


class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        # super().__init__(self, parent)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Page")
        label.pack(padx=10, pady=10)

        switch_window_button = ttk.Button(
            self,
            text="Open Main Page",
            command=lambda: controller.show_frame(MainPage)
        )

        switch_window_button.pack(side="bottom", fill=tk.X)


if __name__ == "__main__":
    app = TKApplication("NiteChat Server")
    app.mainloop()
