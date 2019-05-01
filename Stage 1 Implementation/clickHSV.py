import sys
import cv2 as cv
import tkinter as tk
from PIL import Image
from PIL import ImageTk

h = []
s = []
v = []
imgCV = cv.imread(sys.argv[1])
#print (imgCV.shape)
root = tk.Tk()
geometry = "%dx%d+0+0"%(imgCV.shape[0], imgCV.shape[1])
root.geometry()

def rightclick(event):
	print("lowerbound :")
	print(min(h) , min(s) , min(v))
	print("upperbound :")
	print(max(h) , max(s) , max(v))


def leftclick(event):
    #print("left")
    #print root.winfo_pointerxy()
    #print (event.y, event.x)
    #print("BGR color")
    #print (imgCV[event.y, event.x])
    # convert color from BGR to HSV color scheme
    hsv = cv.cvtColor(imgCV, cv.COLOR_BGR2HSV)
    #print("HSV color")
   #print (hsv[event.y, event.x])
    h.append(hsv[event.y, event.x][0])
    s.append(hsv[event.y, event.x][1])
    v.append(hsv[event.y, event.x][2])
# import image
img = ImageTk.PhotoImage(Image.open(sys.argv[1]))
panel = tk.Label(root, image = img)
panel.bind("<Button-1>", leftclick)
panel.bind("<Button-3>", rightclick)


#panel.pack(side = "bottom", fill = "both", expand = "no")
panel.pack(fill = "both", expand = 1)
root.mainloop()