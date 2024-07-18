from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import ttk
import cv2
from threading import Thread

camera_stream = None

def start_camera_window():
    global camera_stream

    # Initialize Tkinter window
    root = tk.Tk()
    root.title("Camera Stream")
    root.geometry("800x600")

    # Create a label to display video feed
    label = ttk.Label(root)
    label.pack(padx=10, pady=10, expand=True)

    # Function to update video feed
    def update_video_feed():
        global camera_stream

        # Capture video stream from OpenCV
        cap = cv2.VideoCapture(0)

        # Read and display video frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame from OpenCV format to PIL format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image = ImageTk.PhotoImage(image)

            # Update label with the new video frame
            label.config(image=image)
            label.image = image

            # Update Tkinter window
            root.update()

            # Break the loop when the window is closed
            if root.protocol("WM_DELETE_WINDOW"):
                break

        # Release the camera and destroy the Tkinter window
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()

    # Start the function to update video feed in a new thread
    Thread(target=update_video_feed).start()

    # Run the Tkinter main loop
    root.mainloop()