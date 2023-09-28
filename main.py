from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np


class WebcamBubbleApp:
    def __init__(self):

        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.configure(bg="white")
        self.root.attributes("-topmost", 1)
        self.root.attributes("-transparentcolor", "white")
        self.root.geometry("500x500")

        self.label = Label(self.root, height=500,
                           width=500, bg="white", border=0)
        self.label.pack()

        self.capture = cv2.VideoCapture(0)

        img = Image.open("bg.png")
        img = img.resize((300, 300), Image.ADAPTIVE)
        self.image = ImageTk.PhotoImage(img)
        self.label.configure(image=self.image)

        self.update()

        # Initialize variables for dragging
        self.drag_data = {"x": 0, "y": 0, "clicked": False}

        # Bind mouse events for window dragging
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<B1-Motion>", self.on_drag)

    def update(self):
        ret, frame = self.capture.read()
        if ret:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Create a circular mask
            mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
            center = (frame.shape[1] // 2, frame.shape[0] // 2)
            radius = min(frame.shape[1] // 2, frame.shape[0] // 2)
            cv2.circle(mask, center, radius, 255, -1)

            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the numpy frame into a PIL Image
            frame_image = Image.fromarray(frame)

            # Resize the frame_image to fit the application window
            frame_image = frame_image.resize((500, 500))

            # Create an alpha mask from the numpy mask array
            alpha_mask = Image.fromarray(mask).resize((500, 500))

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
            self.root.wm_geometry(f"500x500+{x_pos}+{y_pos}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WebcamBubbleApp()
    app.run()
