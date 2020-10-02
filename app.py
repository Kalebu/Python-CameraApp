import cv2
import time
import threading
from cv2 import cv2
from PIL import Image, ImageTk 
from tkinter import Label, Button, Tk, PhotoImage
        

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("My Camera")
        self.window.geometry("500x400")
        self.window.configure(bg="#ff2fff")
        self.window.resizable(1, 1)
        Label(self.window, width=400, height = 30,  bg="black").place(x=0, y =320)
        self.TakePhoto_b = Button(self.window, width = 20, text = "Shot", font = ("Times", 15),bg = "#2F4F4F", relief = 'flat', command=self.TakePhoto)
        self.ImageLabel = Label(self.window, width = 500, height= 320, bg = "#4682B4")
        self.ImageLabel.place(x=0, y=0)
        self.TakePhoto_b.place(x = 150, y = 360)
        self.take_picture = False
        self.PictureTaken = False
        self.Main()

    @staticmethod
    def LoadCamera():
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            ret, frame = camera.read()
        while ret:
            ret, frame = camera.read()
            if ret:
                yield frame
            else:
                yield False

    def TakePhoto(self):
        if not self.PictureTaken:
            print('Taking a Picture')
            self.take_picture = True
        else:
            print("Reconfiguring camera")
            self.TakePhoto_b.configure(text = "Shot")
            self.take_picture = False
 
    def Main(self):
        self.render_thread = threading.Thread(target=self.StartCamera)
        self.render_thread.daemon = True
        self.render_thread.start()

    def StartCamera(self):
        frame = self.LoadCamera()
        CaptureFrame = None
        while True:
            Frame = next(frame)
            print(self.take_picture)
            if frame and not self.take_picture:
                picture = Image.fromarray(Frame)
                picture = picture.resize((500, 400), resample=0)
                CaptureFrame = picture.copy()
                picture = ImageTk.PhotoImage(picture)
                self.ImageLabel.configure(image = picture)
                self.ImageLabel.photo = picture
                self.PictureTaken = False
                time.sleep(0.001)
            else:
                if not self.PictureTaken:
                    print("Your camera died")
                    CaptureFrame.save('myimage.png')
                    self.TakePhoto_b.configure(text = "Take Again")
                    self.PictureTaken = True
            

root = Tk()
App = CameraApp(root)
root.mainloop()
