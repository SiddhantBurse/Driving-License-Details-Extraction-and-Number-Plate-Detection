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
    '''
    t.destroy()
    #os.system('demo2.py')
    add2(text)
    '''
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
    # Read the image file
    image = cv2.imread(filename)
 # Resize the image - change width to 500
    image = imutils.resize(image, width=500)

# Display the original image
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)

# RGB to Gray scale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("1 - Grayscale Conversion", gray)
    cv2.waitKey(0)

# Noise removal with iterative bilateral filter(removes noise while preserving edges)
    lf=np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
    gray=cv2.filter2D(gray,-1,lf)
    #gray = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("2 - Bilateral Filter", gray)
    cv2.waitKey(0)

# Find Edges of the grayscale image
    edged = cv2.Canny(gray, 170, 200)
    cv2.imshow("3 - Canny Edges", edged)
    cv2.waitKey(0)

# Find contours based on Edges
    cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Create copy of original image to draw all contours
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0,0,255), 3)
    cv2.imshow("4-Contours", img1)
    cv2.waitKey(0)

#sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCnt = None #we currently have no Number plate contour

# Top 30 Contours
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
    cv2.imshow("5- Top 30 Contours", img2)
    cv2.waitKey(0)

# loop over our contours to find the best possible approximate contour of number plate
    count = 0
    idx =7
    for c in cnts:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # print ("approx = ",approx)
        if len(approx) == 4:  # Select the contour with 4 corners
            NumberPlateCnt = approx #This is our approx Number Plate Contour

            # Crop those contours and store it in Cropped Images folder
            x, y, w, h = cv2.boundingRect(c) #This will find out co-ord for plate
            new_img = gray[y:y + h, x:x + w] #Create new image
            cv2.imwrite('cropimg/' + str(idx) + '.png', new_img) #Store new image
            idx+=1

            break


# Drawing the selected contour on the original image
#print(NumberPlateCnt)
    cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
    cv2.imshow("Final Image With Number Plate Detected", image)
    cv2.waitKey(0)

    Cropped_img_loc = 'cropimg/7.png'
    cv2.imshow("Cropped Image ", cv2.imread(Cropped_img_loc))

# Use tesseract to covert image into string
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
    print("Number is :", text)
    t.carno = Label(frame1, text='Number').grid(row=1,column=0)
    t.car_no = Entry(frame1)
    t.car_no.grid(row=1,column=1)
    t.car_no.insert(INSERT,text)
    b2=Button(frame1, text='Confirm',command=call).grid(row=2,column=0,columnspan=2)
    
t = tk.Tk()
t.title('Numberplate')
w, h = t.winfo_screenwidth(), t.winfo_screenheight()
t.geometry("%dx%d+0+0" % (w, h))
frame=Frame(t)
frame.pack()
frame2=Frame(frame,width=200,height=50)
frame2.pack()
frame1=Frame(frame,width=200,height=50)
frame1.pack()
b1=Button(frame1, text="Upload Image",command=openf).grid(row=0, column=0, padx=100, pady=100,columnspan=2)
filename=''
text=''
mainloop()
