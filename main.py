from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np


class WebcamBubbleApp:
    def __init__(self):

        # Create the root window
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.configure(bg="black")
        self.root.attributes("-topmost", 1)
        self.root.attributes("-transparentcolor", "black")
        self.root.geometry("350x350")

        # Initialize variables for dragging
        self.drag_data = {"x": 0, "y": 0, "clicked": False}

        # Load the image
        img = Image.open("bg.png")
        img = img.resize((300, 300), Image.ADAPTIVE)
        self.image = ImageTk.PhotoImage(img)

        # Bind mouse events for window dragging
        self.label = Label(self.root,
                           height=350,
                           width=350,
                           bg="black",
                           border=0
                           )
        self.label.configure(image=self.image)
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        
        self.label.pack()

        # Create a capture object
        self.capture = cv2.VideoCapture(0)
        self.update()

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
            frame_image = frame_image.resize((300, 300))

            # Create an alpha mask from the numpy mask array
            alpha_mask = Image.fromarray(mask).resize((300, 300))

            # Convert the frame_image into "RGBA" mode and add the alpha_mask as the alpha channel
            frame_image = frame_image.convert("RGBA")
            r, g, b, a = frame_image.split()
            frame_image = Image.merge("RGBA", (r, g, b, alpha_mask))

            # Convert the frame_image to PhotoImage and display it
            frame_image = ImageTk.PhotoImage(frame_image)
            self.label.configure(image=frame_image)
            self.label.image = frame_image

        self.root.after(10, self.update)

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
            x_pos = self.root.winfo_x() + deltax
            y_pos = self.root.winfo_y() + deltay
            self.root.wm_geometry(f"350x350+{x_pos}+{y_pos}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WebcamBubbleApp()
    app.run()
