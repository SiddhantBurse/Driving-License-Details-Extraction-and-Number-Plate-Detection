from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
import sqlite3
from datetime import date
from datetime import time
from datetime import datetime
connection = sqlite3.connect('TS.db')
cursor = connection.cursor()
def alert():
    global t
    tkinter.messagebox.showinfo("Alert", "Challan Generated")
    t.destroy()
def pchallan(dnum,tex):
    global t
    t = tk.Tk()
    t.title('CRIMINALADD')
    w, h = t.winfo_screenwidth(), t.winfo_screenheight()
    t.geometry("%dx%d+0+0" % (w, h))
    Label(t, text='E-Challan',font=tkFont.Font(family="Times New Roman", size=30)).grid(row=0,column=0,columnspan=2)
    cursor.execute('SELECT FNAME, ADDR FROM TRAFFIC WHERE DRIVINGLICENSE=?',(dnum,))
    det=cursor.fetchall()
    Label(t, text='DL No.:',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=1,column=0)
    Label(t, text=dnum,font=tkFont.Font(family="Times New Roman", size=20)).grid(row=1,column=1)
    Label(t, text='NAME',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=2,column=0)
    Label(t, text=det[0][0],font=tkFont.Font(family="Times New Roman", size=20)).grid(row=2,column=1)
    Label(t, text='Car No.:',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=3,column=0)
    Label(t, text=tex,font=tkFont.Font(family="Times New Roman", size=20)).grid(row=3,column=1)
    Label(t, text='ADDRESS',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=4,column=0)
    Label(t, text=det[0][1],font=tkFont.Font(family="Times New Roman", size=20)).grid(row=4,column=1)
    Label(t, text='DATE OF CRIME',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=5,column=0)
    Label(t, text=date.today(),font=tkFont.Font(family="Times New Roman", size=20)).grid(row=5,column=1)
    Label(t, text='TIME OF CRIME',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=6,column=0)
    Label(t, text=datetime.now().strftime('%I:%M:%S %p'),font=tkFont.Font(family="Times New Roman", size=20)).grid(row=6,column=1)
    Label(t, text='FINE',font=tkFont.Font(family="Times New Roman", size=20)).grid(row=7,column=0)
    Label(t, text="RS.1000",font=tkFont.Font(family="Times New Roman", size=20)).grid(row=7,column=1)
    Button(t,text='Okay',command=alert).grid(row=8,column=0,columnspan=2)
    
