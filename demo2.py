from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import cv2
import imutils
import numpy
import sqlite3
import pytesseract
from demo6 import lisc
from challan import pchallan
connection = sqlite3.connect('TS.db')
cursor = connection.cursor()
def add2(text,ch):
    global t
    print("demo2=",text)
    t = tk.Tk()
    t.title('Form')
    w, h = t.winfo_screenwidth(), t.winfo_screenheight()
    t.geometry("%dx%d+0+0" % (w, h))
    lab = Label(t,text=text)
    lab.pack()

    def openf():
        
        global t,filename,frame2,frame1
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("jpeg files", ".jpg"), ("all files", ".*")))
        t.load = Image.open(filename)
        t.load = t.load.resize((500, 250), Image.ANTIALIAS)
        t.photo = ImageTk.PhotoImage(t.load)
        t.img1 = Label(t, image=t.photo)
        t.img1.place(x=1000, y=150)
        
        
    def pro():
        data=lisc(filename)
        put(data)

    def put(data):
        c_id1.insert(INSERT,data[0])
        fname1.insert(INSERT,data[5])
        Dob1.insert(INSERT,data[3])
        bloodgrp1.insert(INSERT,data[4])
        date_i.insert(INSERT,data[1])
        validtill.insert(INSERT,data[2])
        Add.insert(INSERT,data[6])
        
        
    def add3():
       
        if ch==1:
            cursor.execute("INSERT INTO NP VALUES(?,?)", (text,c_id1.get()))
            connection.commit()
        cursor.execute('SELECT * FROM TRAFFIC WHERE DRIVINGLICENSE=?',(c_id1.get(),))
        dl=cursor.fetchall()
        if dl==[]:
            cursor.execute("INSERT INTO TRAFFIC VALUES(?,?,?,?,?,?,?)", (c_id1.get(), fname1.get(),Dob1.get(),bloodgrp1.get(),date_i.get(),validtill.get(),Add.get()))
            connection.commit()
            connection.close()
        a=c_id1.get()
        t.destroy()
        pchallan(a,text)
    c_id = Label(t, text='Number', borderwidth=2, relief="solid")
    c_id1 = Entry(t, font=tkFont.Font(family="Times New Roman", size=16), borderwidth=2,
                   relief="solid")
    fname = Label(t, text='Full Name', borderwidth=2, relief="solid")
    fname1 = Entry(t, font=tkFont.Font(family="Times New Roman", size=16), borderwidth=2,
                   relief="solid")
   
    DOB = Label(t, text='DOB', borderwidth=2, relief="solid")
    Dob1 = Entry(t, font=tkFont.Font(family="Times New Roman", size=16),  borderwidth=2,
                  relief="solid")
    bloodgrp = Label(t, text='Blood group', borderwidth=2, relief="solid")
    bloodgrp1 = Entry(t, font=tkFont.Font(family="Times New Roman", size=16),  borderwidth=2,
                  relief="solid")

    Date_i1 = Label(t, text='Date of issue', borderwidth=2, relief="solid")
    date_i = Entry(t, font=tkFont.Font(family="Times New Roman", size=16),  borderwidth=2,
                  relief="solid")

    
    validtill_1 = Label(t, text='Valid Till', borderwidth=2, relief="solid")
    validtill = Entry(t, font=tkFont.Font(family="Times New Roman", size=16),  borderwidth=2,
                  relief="solid")

    Add_1 = Label(t, text='Add', borderwidth=2, relief="solid")
    Add = Entry(t, font=tkFont.Font(family="Times New Roman", size=16),  borderwidth=2,
                  relief="solid")
    submitt = Button(t, text='SUBMIT', command=add3, borderwidth=2, relief="solid")
    uplod = Button(t, text='UPLOAD', command=openf, borderwidth=2, relief="solid")
    process = Button(t, text='PROCESS', command=pro, borderwidth=2, relief="solid")
    

    fname.place(x=50, y=150, width=200, height=70)
    fname1.place(x=275, y=150, width=400, height=70)
    

    DOB.place(x=50, y=250, width=200, height=70)
    Dob1.place(x=275, y=250, width=200, height=70)

    bloodgrp.place(x=50, y=550, width=200, height=70)
    bloodgrp1.place(x=275, y=550, width=200, height=70)

    Date_i1.place(x=50, y=350, width=200, height=70)
    date_i.place(x=275, y=350, width=200, height=70)
    
    validtill_1.place(x=50, y=450, width=200, height=70)
    validtill.place(x=275, y=450, width=200, height=70)

    Add_1.place(x=50, y=650, width=200, height=70)
    Add.place(x=275, y=650, width=700, height=70)

    c_id.place(x=50, y=50, width=200, height=70)
    c_id1.place(x=275, y=50, width=400, height=70)

    submitt.place(x=1170, y=630, width=100, height=70)
    uplod.place(x=1170, y=530, width=100, height=70)
    process.place(x=1170, y=730, width=100, height=70)
    
    
    
  

    
