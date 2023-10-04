# WebCamBubbleApp

WebCamBubbleApp is a python program that provides a webcam bubble feed on your desktop. It stays on top of all other windows, providing a handy visual monitor.

The application comes with two essential buttons:

1. screen recording button (Launches OBS in the background and starts recording your screen)
2. adjust settings button (Launches a settings window where you can set the path to your OBS executable file)

The application is crafted using Python libraries like Tkinter, OpenCV, and the customtkinter library.

## Requirements

- OBS (Open Broadcaster Software) installed on your system with websocket server enabled.

## Features

1. **Webcam Display:** The application fetches your webcam feed and displays it within a neat circular bubble on your desktop screen. It adjusts dynamically to the size and margins of your screen layout and stays on top of all other windows for easy access.

2. **Draggable Window:** The window which holds the webcam feed can be dragged around your screen area to position it according to your preference.

## Usage

Using the application involves running the script. Upon execution, you will see:

1. The Webcam Bubble showing your webcam feed.
2. On hitting the record button, OBS will be launched in the background and a recording will be started.
3. If you installed OBS in a custom location, you can set the path to the executable file in the settings window.

## Build with Pyinstaller

```bash
pyinstaller --clean --noconfirm --onefile --windowed --add-data ".\OBSCommand;OBSCommand/" --add-data ".\webcam_env\Lib\site-packages\customtkinter;customtkinter/" --add-data ".\assets\*;assets/" --name WebcamBubble main.py
```