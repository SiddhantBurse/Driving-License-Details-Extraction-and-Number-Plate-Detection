from tkinter import *
import tkinter as tk
import tkinter.messagebox
import numpy as np
import tkinter.font as tkFont
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import cv2
import imutils
import numpy
import sqlite3
import pytesseract
from demo2 import add2
from challan import pchallan
connection = sqlite3.connect('TS.db')
cursor = connection.cursor()
def call():
    text=t.car_no.get()
    cursor.execute('SELECT DRIVINGLICENSE FROM NP WHERE NUMBERPLATE=?',(text,))
    dl=cursor.fetchall()
    check=True
    if dl==[]:
        tkinter.messagebox.showwarning("Alert", "Car is not Registered")
        check=False
    else:
        msg=tkinter.messagebox.askquestion("Alert", f"Car is registered\nIs {dl[0][0]} the owner?")
        if msg=='yes':
            t.destroy()
            pchallan(dl[0][0],text)
        else:
            tkinter.messagebox.showinfo("Alert", "Scan the license")
            t.destroy()
            add2(text,0)
    if check==False:
        msg=tkinter.messagebox.askquestion("Alert", "Is driver the owner?")
        if msg=='yes':
            t.destroy()
            add2(text,1)
        if msg=='no':
            t.destroy()
            add2(text,0)
def openf():
   
    global t,filename,frame2,frame1
    filename = filedialog.askopenfilename(initialdir="carphotos/", title="Select file",
                                                filetypes=(("jpeg files", ".jpg"), ("all files", ".*")))
    t.load = Image.open(filename)
    t.load = t.load.resize((500, 250), Image.ANTIALIAS)
    t.photo = ImageTk.PhotoImage(t.load)
    t.img1 = Label(frame2, image=t.photo).pack()
    numberplate()
def numberplate():
    
    global filename,text
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\siddh\AppData\Local\Tesseract-OCR\Tesseract.exe"
    
    image = cv2.imread(filename)
    
    image = imutils.resize(image, width=500)
    
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("1 - Grayscale Conversion", gray)
    cv2.waitKey(0)
    
    lf=np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
    gray=cv2.filter2D(gray,-1,lf)
    cv2.imshow("Low Pass Filter", gray)
    cv2.waitKey(0)
    
    edged = cv2.Canny(gray, 170, 200)
    cv2.imshow("Canny Edges", edged)
    cv2.waitKey(0)
    
    cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
    cv2.imshow("All Contours", img1)
    cv2.waitKey(0)

    
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
    #NumberPlateCnt = None 

    
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
    cv2.imshow("Top 20 Contours", img2)
    cv2.waitKey(0)

    
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  # Select the contour with 4 corners
            NumberPlateCnt = approx #This is our approx Number Plate Contour

            
            x, y, w, h = cv2.boundingRect(c) #This will find out co-ord for plate
            new_img = gray[y:y + h, x:x + w] #Create new image
            break

    cv2.imshow("Cropped Image ", new_img)

    
    text = pytesseract.image_to_string(new_img, lang='eng')
    print("Number is :", text)
    t.carno = Label(frame1, text='Number').grid(row=1,column=0)
    t.car_no = Entry(frame1)
    t.car_no.grid(row=1,column=1)
    t.car_no.insert(INSERT,text)
    b2=Button(frame1, text='CONFIRM',command=call).grid(row=2,column=0,columnspan=2)
  
t = tk.Tk()
t.title('Dashboard')
w, h = t.winfo_screenwidth(), t.winfo_screenheight()
t.geometry("%dx%d+0+0" % (w, h))
frame=Frame(t)
frame.pack()
frame2=Frame(frame,width=200,height=50)
frame2.pack()
frame1=Frame(frame,width=200,height=50)
frame1.pack()
b1=Button(frame1, text="UPLOAD IMAGE",command=openf).grid(row=0, column=0, padx=100, pady=100,columnspan=2)
filename=''
text=''
mainloop()
