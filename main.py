import ctypes
import os
import threading
import tkinter

import cv2
import numpy as np
from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkFrame,
                           CTkImage, CTkLabel, CTkToplevel,
                           deactivate_automatic_dpi_awareness,
                           set_appearance_mode, set_default_color_theme,
                           set_widget_scaling, set_window_scaling)
from PIL import Image


class SettingsWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Load images
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "assets")
        folder_image = CTkImage(
            light_image=Image.open(os.path.join(
                image_path, "folder_dark.png")),
            dark_image=Image.open(os.path.join(
                image_path, "folder_light.png")),
        )

        self.attributes("-topmost", 1)
        self.title("WebCam Bubble Settings")

        window_width = 520
        window_height = 150
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)

        # Center the window on the screen
        screen_width = self.winfo_screenwidth() * parent.scale.get()
        screen_height = self.winfo_screenheight() * parent.scale.get()

        self.wm_geometry(
            f"+{screen_width//2-window_width}+{screen_height//2-window_height}")

        # Build Settings Frame
        self.settings_frame = CTkFrame(self)
        self.settings_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
            ipadx=10,
        )

        # Title Label
        CTkLabel(
            self.settings_frame,
            text="Select OBS executable path",
            font=("Arial", 14),
        ).pack(
            side="top",
            anchor="n",
            pady=10,
        )

        # OBS Path Label
        CTkLabel(
            self.settings_frame,
            text="OBS Path",
        ).pack(
            side="left",
            anchor="w",
            padx=10,
        )

        # OBS Path Entry
        CTkEntry(
            self.settings_frame,
            textvariable=parent.obs64_path,
            width=350,
        ).pack(
            side="left",
            anchor="w",
            padx=10,
        )

        # OBS Path Button
        CTkButton(
            self.settings_frame,
            width=30,
            text="",
            image=folder_image,
            command=lambda: self.set_path(parent),
        ).pack(
            side="left",
        )

    def set_path(self, parent):
        """ Open a file dialog to select the obs executable path."""

        # Get the path to the OBS executable
        obs_path = tkinter.filedialog.askopenfilename(
            initialdir="C:/Program Files/obs-studio/bin/64bit",
            title="Select OBS executable",
            filetypes=(("executables", "*.exe"), ("all files", "*.*")),
        )

        # Set the path to the obs executable
        if obs_path is not None and obs_path != "":
            parent.obs64_path.set(obs_path)

        return

class WebCamBubbleApp(CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("WebCam Bubble")  # CTk title() method
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        self.size = tkinter.IntVar(self, value=300)
        self.margin = tkinter.IntVar(self, value=100)

        deactivate_automatic_dpi_awareness()

        # Check if the OS is Windows 10 or MacOS
        if os.name == "nt":
            # Set process DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            # Create a tkinter window
            root = tkinter.Tk()
            # Get the reported DPI from the window's HWND
            dpi = ctypes.windll.user32.GetDpiForWindow(root.winfo_id())
            # Destroy the window
            root.destroy()
        elif os.name == "posix":
            # Get the reported DPI from the window's HWND
            dpi = 96

        self.scale = tkinter.IntVar(self, value=dpi/96)

        set_widget_scaling(self.scale.get())
        set_window_scaling(self.scale.get())

        # Setting up the self window
        self.overrideredirect(1)
        self.attributes("-topmost", 1)

        if os.name == "nt":
            # Set the window to be transparent
            self.wm_attributes("-transparentcolor", "black")
        elif os.name == "posix":
            # Set the window to be transparent
            self.wm_attributes("-transparent", "true")

        self.geometry(
            f"{self.size.get()+self.margin.get()}x{self.size.get()+self.margin.get()}")

        # OBS executable path

        if os.name == "nt":
            self.obs64_path = tkinter.StringVar(self,
                                                value="C:/Program Files/obs-studio/bin/64bit/obs64.exe")
        elif os.name == "posix":
            self.obs64_path = tkinter.StringVar(self,
                                                value="/Applications/OBS.app/Contents/MacOS/OBS")

        # Load images
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "assets")
        settings_image = CTkImage(
            light_image=Image.open(os.path.join(image_path, "gear-grey.png")),
            dark_image=Image.open(os.path.join(image_path, "gear-white.png")),
        )

        # Load the image
        img = Image.open(os.path.join(image_path, "bg.png"))
        # img = img.resize((self.size.get(), self.size.get()), Image.ADAPTIVE)
        self.image = CTkImage(img)

        # Bind mouse events for window dragging
        self.label = CTkLabel(self,
                              height=self.size.get() + self.margin.get(),
                              width=self.size.get() + self.margin.get(),
                              bg_color="black",  # Set the background color to black to make it transparent
                              text="",
                              )
        self.label.pack()

        # Get the screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Calcluate the position of the window on the bottom right corner of the screen
        self.x = self.screen_width * self.scale.get() - (
            (self.size.get() + self.margin.get()) * self.scale.get()
        )

        self.y = self.screen_height * self.scale.get() - (
            (self.size.get() + self.margin.get()) * self.scale.get()
        )

        # Place the window on the bottom right corner of the screen
        self.wm_geometry(f"+{self.x}+{self.y}")

        # Add a button that open the settings window
        self.open_settings_button = CTkButton(
            self,
            image=settings_image,
            text="",
            width=40,
            height=40,
            bg_color="black",
            command=self.open_settings_window
        )
        self.open_settings_button.place(
            anchor="se",
            relx=0.75,
            rely=0.85,
        )

        # Add a button that starts/stops recording
        self.record_button = CTkButton(
            self,
            text="REC",
            width=40,
            height=40,
            bg_color="black",
            command=self.record_screen
        )
        self.record_button.place(
            anchor="sw",
            relx=0.25,
            rely=0.85,
        )

        # Initialize settings window as None
        self.settings_window = None
        self.is_recording = False

        # Create a capture object
        self.capture = cv2.VideoCapture(0)
        self.update()

        # Initialize variables for dragging
        self.drag_data = {"x": 0, "y": 0, "clicked": False}

        # Bind mouse events for window dragging
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<B1-Motion>", self.on_drag)

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["clicked"] = True

    def stop_drag(self, event):
        self.drag_data["clicked"] = False

    def on_drag(self, event):
        if self.drag_data["clicked"]:
            x = self.winfo_pointerx() - self.drag_data["x"]
            y = self.winfo_pointery() - self.drag_data["y"]
            self.geometry(f"+{x}+{y}")

    def update(self):
        ret, frame = self.capture.read()

        if ret:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Create a square frame
            height, width, _ = frame.shape
            square_size = min(height, width)

            # Crop the center of the frame
            delta = abs(height - width) // 2
            if height > width:
                frame = frame[delta:delta + square_size, :]
            else:
                frame = frame[:, delta:delta + square_size]

            # Create a circular mask
            mask = np.zeros((square_size, square_size), dtype=np.uint8)
            center = (square_size // 2, square_size // 2)
            radius = square_size // 2
            cv2.circle(mask, center, radius, 255, -1)

            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the numpy frame into a PIL Image
            frame_image = Image.fromarray(frame)

            # Resize the frame_image to fit the application window
            frame_image = frame_image.resize(
                (self.size.get(), self.size.get()))

            # Create an alpha mask from the numpy mask array
            alpha_mask = Image.fromarray(mask).resize(
                (self.size.get(), self.size.get()))

            # Convert the frame_image into "RGBA" mode and add the alpha_mask as the alpha channel
            frame_image = frame_image.convert("RGBA")
            r, g, b, a = frame_image.split()
            frame_image = Image.merge("RGBA", (r, g, b, alpha_mask))

            # Convert the frame_image to CTkImage and display it
            converted_frame_image = CTkImage(
                frame_image, size=(self.size.get(), self.size.get()))

            # Update the image in the label
            self.label.configure(image=converted_frame_image,
                                 height=self.size.get()+self.margin.get(),
                                 width=self.size.get()+self.margin.get(),
                                 )

        self.after(30, self.update)

    def open_settings_window(self):
        # Check if settings window already exists
        if self.settings_window is not None:
            # If the window is already open, just bring it into focus
            self.settings_window.focus_set()
        else:
            # If not, create a new settings window and store a reference to it
            self.settings_window = SettingsWindow(self)
            # Make sure to clear the reference when the settings window is closed
            self.settings_window.protocol(
                "WM_DELETE_WINDOW", self.on_settings_window_close)

    def on_settings_window_close(self):
        # Your settings window close logic here...
        # For instance, you may want to save settings when the window is closed

        # Clear the reference to the settings window
        self.settings_window.destroy()
        self.settings_window = None

    def record_screen(self):

        if self.is_recording:
            self.is_recording = False

            # Change the working directory to the OBS directory
            os.chdir(os.path.dirname(self.obs64_path.get()))

            # Create the OBS Command
            cmd = f'"{self.obs64_path.get()}" --stoprecording'
            print("Stop recording")
            print(cmd)

            # Create a new thread to stop recording
            thread = threading.Thread(target=os.system, args=(cmd,))
            thread.start()

            self.record_button.configure(fg_color="#14375e")
            self.record_button.configure(text="REC")

            # # Get the directory of the python script
            # script_dir = os.path.dirname(os.path.realpath(__file__))

            # # Use OBS Command to stop recording
            # path = os.path.join(script_dir, "OBSCommand")

            # cmd = f'{path}\\OBSCommand.exe /stoprecording && taskkill /f /im obs64.exe'

            # print()
            # print(cmd)
            # print()

            # # Create a new thread to stop recording
            # thread = threading.Thread(target=os.system, args=(cmd,))
            # thread.start()

        else:
            self.is_recording = True

            # Change the working directory to the OBS directory
            os.chdir(os.path.dirname(self.obs64_path.get()))

            # Create the OBS Command
            cmd = f'"{self.obs64_path.get()}" --startrecording --minimize-to-tray'
            print("Start recording")
            print(cmd)

            # Create a new thread to run OBS
            thread = threading.Thread(target=os.system, args=(cmd,))
            thread.start()

            self.record_button.configure(
                fg_color="#ff2100",
                hover_color="#b20000")
            self.record_button.configure(text="●")


if __name__ == "__main__":
    app = WebCamBubbleApp()
    app.mainloop()
