from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
#import requests
import pytz


root = Tk() #GUI frame
root.title('Weather App')
root.geometry("900x500+300+200")
root.resizable(False,False)




#Bottom box
Frame_image = PhotoImage(file="images/BottomBox.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5,pady=5,side=BOTTOM)

#labels
label1 = Label(root,text="WIND",font=("Helvetica",15,'bold'),fg='white',bg='#1ab5ef')
label1.place(x=120,y=400)

label2=Label(root,text="HUMIDITY",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
label2.place(x=225,y=400)

label3 = Label(root,text="DESCRIPTION",font=("Helvetica",15,'bold'),fg='white',bg='#1ab5ef')
label3.place(x=430,y=400)

label1 = Label(root,text="PRESSURE",font=("Helvetica",15,'bold'),fg='white',bg='#1ab5ef')
label1.place(x=650,y=400)


root.mainloop()