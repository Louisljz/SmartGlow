# Imports
# GUI
from tkinter import *
from PIL import Image, ImageTk
# Computer Vision
import cv2
# YOLO object detection
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
# Connection with Arduino Uno
from cvzone.SerialModule import SerialObject
arduino = SerialObject('COM3')

# Initialize and Configure Tkinter Window
window = Tk()
window.geometry("1152x700")
window.configure(bg = "#FFFFFF")
window.title('IntelliGlow')
window.resizable(False, False)
icon_img = PhotoImage(file='icon.png')
window.iconphoto(True, icon_img)

# Initialize Webcam and YOLO Model
cap = cv2.VideoCapture(1)
yolo = YOLO('yolov8n.pt')
duration = 0 # For time interval between Lights ON/OFF 

# Camera and AI Function
def display_cam():
    global duration
    counter = 0 # Counts the number of people in every frame
    _, img = cap.read()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # YOLO Prediction
    results = yolo.predict(img, verbose=False)

    for r in results:
        annotator = Annotator(img)
        
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0] # Get Bbox Coordinates
            cls = yolo.names[int(box.cls)] # Get Label String
            conf = box.conf[0] # Get confidence score
            if cls == 'person' and conf > 0.5:
                counter += 1 # Increments number of person
                # Drawing bounding box
                annotator.box_label(b, color=(0, 255, 0)) 
    
    frame = annotator.result() # Return annotated image
    # Set Webcam Image in Tkinter Label
    cv2image = cv2.resize(frame, (540, 380))
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    cam.imgtk = imgtk
    cam.configure(image=imgtk)
    
    people_counter.set(f"Number of People in Classroom: {counter}")
    # If there is at least one person in classroom
    if counter >= 1:
        # Increments duration of the person staying in the room
        if duration < 10:
            duration += 1
    else: # If there is no person in classroom
        if duration > 0:
            # Decrements duration of the person leaving the room
            duration -= 1
    
    # Wait for some time, then communicate with arduino
    if duration == 10:
        arduino.sendData([1])
    elif duration == 0:
        arduino.sendData([0])
    
    cam.after(20, display_cam) # Updates Frame

# Display Background
bgimg = PhotoImage(file='background.png')
bg = Label(window, image = bgimg)
bg.place(x = 0, y = 0)

# People Counter Display
people_counter = StringVar()
counter_label = Label(window, textvariable=people_counter, font=("Arial", 20), 
                        background='green', foreground='white')
counter_label.place(x=675, y=300)

# Webcam Display
cam = Label(window)
cam.place(x = 100, y = 180)

display_cam()
window.mainloop()
arduino.sendData([0]) #turns lights off if program is terminated.
