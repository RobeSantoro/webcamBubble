from tkinter import *
from PIL import ImageTk, Image
import pyautogui as pg

class WebcamBubbleApp:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.configure(bg="white")
        self.root.attributes("-topmost", 1)
        self.root.attributes("-transparentcolor", "white")
        self.root.geometry("500x500")

        self.label = Label(self.root, height=500, width=500, bg="white", border=0)
        self.label.pack()

        self.place_bottom_left()

        img = Image.open("bg.png")
        img = img.resize((300, 300), Image.ADAPTIVE)
        self.image = ImageTk.PhotoImage(img)
        self.label.configure(image=self.image)

    def place_bottom_left(self):
        reso = pg.size()
        rx = reso[0]
        ry = reso[1]
        x = 0
        y = ry - 500
        self.root.geometry(f"500x500+{x}+{y}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WebcamBubbleApp()
    app.run()