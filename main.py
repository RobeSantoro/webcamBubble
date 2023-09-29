import os
import threading
from tkinter import IntVar, StringVar, filedialog

import cv2
import numpy as np
from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkFrame,
                           CTkImage, CTkLabel, CTkToplevel,
                           set_appearance_mode, set_default_color_theme)
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
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.wm_geometry(
            f"+{screen_width//2-window_width//2}+{screen_height//2-window_height//2}")

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
        self.title_label = CTkLabel(
            self.settings_frame,
            text="Select OBS executable path",
            font=("Arial", 14),
        ).pack(
            side="top",
            anchor="n",
            pady=10,
        )

        # OBS Path Label
        self.obs_path_label = CTkLabel(
            self.settings_frame,
            text="OBS Path",
        ).pack(
            side="left",
            anchor="w",
            padx=10,
        )

        # OBS Path Entry
        self.obs_path_entry = CTkEntry(
            self.settings_frame,
            textvariable=parent.obs64_path,
            width=350,
        ).pack(
            side="left",
            padx=10,
        )

        # OBS Path Button
        self.obs_path_button = CTkButton(
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
        obs_path = filedialog.askopenfilename(
            initialdir="C:/Program Files/obs-studio/bin/64bit",
            title="Select OBS executable",
            filetypes=(("executables", "*.exe"), ("all files", "*.*")),
        )

        # Set the path to the obs executable
        parent.obs64_path.set(obs_path)


class WebCamBubbleApp(CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.obs64_path = StringVar(self,
                                    value="C:/Program Files/obs-studio/bin/64bit/obs64.exe")

        self.title("WebCam Bubble")  # CTk title() method
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        # Load images
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "assets")
        settings_image = CTkImage(
            light_image=Image.open(os.path.join(image_path, "gear-grey.png")),
            dark_image=Image.open(os.path.join(image_path, "gear-white.png")),
        )

        self.size = 300
        self.margin = 100

        # Setting up the self window
        self.overrideredirect(1)
        self.attributes("-topmost", 1)

        # Make the background transparent when black
        self.attributes("-transparentcolor", "black")

        self.geometry(
            f"{self.size}x{self.size}+{self.margin}+{self.margin}")

        # Get the screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Initialize variables for dragging
        self.drag_data = {"x": 0, "y": 0, "clicked": False}

        # Load the image
        img = Image.open("bg.png")
        # img = img.resize((self.size, self.size), Image.ADAPTIVE)
        self.image = CTkImage(img)

        # Bind mouse events for window dragging
        self.label = CTkLabel(self,
                              height=self.size+self.margin,
                              width=self.size+self.margin,
                              bg_color="black",  # Set the background color to black to make it transparent
                              text="",
                              )
        self.label.pack()

        # Bind mouse events for window dragging
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<B1-Motion>", self.on_drag)

        # Place the webcambubble on the bottom right corner of the screen
        self.wm_geometry(
            f"{self.size+self.margin}x{self.size+self.margin}+{self.screen_width-self.size-self.margin}+{self.screen_height-self.size-self.margin}")

        # Create a capture object
        self.capture = cv2.VideoCapture(0)
        self.update()

        # Add a button that open the settings window
        self.open_settings_button = CTkButton(
            self,
            image=settings_image,
            text="",
            width=30,
            height=30,
            # corner_radius=15,
            bg_color="black",
            command=self.open_settings_window)

        # Place the button along the circumference of the circle
        self.open_settings_button.place(
            relx=0.75,
            rely=0.85,
            anchor="se",
        )

        self.record_button = CTkButton(
            self,
            text="rec",
            width=30,
            height=30,
            bg_color="black",
            command=self.record_screen)

        self.record_button.place(
            anchor="sw",
            relx=0.25,
            rely=0.85,
        )

        # Initialize settings window as None
        self.settings_window = None
        self.is_recording = False

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
            frame_image = frame_image.resize((self.size, self.size))

            # Create an alpha mask from the numpy mask array
            alpha_mask = Image.fromarray(mask).resize((self.size, self.size))

            # Convert the frame_image into "RGBA" mode and add the alpha_mask as the alpha channel
            frame_image = frame_image.convert("RGBA")
            r, g, b, a = frame_image.split()
            frame_image = Image.merge("RGBA", (r, g, b, alpha_mask))

            # Convert the frame_image to CTkImage and display it
            converted_frame_image = CTkImage(
                frame_image, size=(self.size, self.size))

            # Update the image in the label
            self.label.configure(image=converted_frame_image,
                                 height=self.size+self.margin,
                                 width=self.size+self.margin,
                                 )

        self.after(30, self.update)

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["clicked"] = True

    def stop_drag(self, event):
        self.drag_data["clicked"] = False

    def on_drag(self, event):
        if self.drag_data["clicked"]:
            x, y = event.x, event.y
            deltax = x - self.drag_data["x"]
            deltay = y - self.drag_data["y"]

            # Move the window to the new position
            x_pos = self.winfo_x() + deltax
            y_pos = self.winfo_y() + deltay
            self.wm_geometry(
                f"{self.size+self.margin}x{self.size+self.margin}+{x_pos}+{y_pos}")

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

            self.record_button.configure(fg_color="#14375e")
            self.record_button.configure(text="rec")

            # Get the directory of the python script
            script_dir = os.path.dirname(os.path.realpath(__file__))

            # Use OBS Command to stop recording
            path = os.path.join(script_dir, "OBSCommand")

            cmd = f'{path}\\OBSCommand.exe /stoprecording && taskkill /f /im obs64.exe'

            print()
            print(cmd)
            print()

            # Create a new thread to stop recording
            thread = threading.Thread(target=os.system, args=(cmd,))
            thread.start()

        else:
            self.is_recording = True

            self.record_button.configure(
                fg_color="#ff2100", hover_color="#b20000")
            self.record_button.configure(text="●")

            # Change the working directory to the OBS directory
            os.chdir(os.path.dirname(self.obs64_path.get()))

            # Create the OBS Command
            cmd = f'"{self.obs64_path.get()}" --startrecording --minimize-to-tray --multi'

            # Create a new thread to run OBS
            thread = threading.Thread(target=os.system, args=(cmd,))
            thread.start()


if __name__ == "__main__":
    app = WebCamBubbleApp()
    app.mainloop()
