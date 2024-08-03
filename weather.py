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

searchBox = PhotoImage(file="search.png")
myImage = Label(image = searchBox)
myImage.place(x = 20, y = 20)

textEntry = tk.Entry(root,justify="center", width=17,font=("poppins",25,"bold"), bg = "#B0B0B0", border=0, fg="white")
textEntry.place(x=50, y=40)
textEntry.focus()

searchIcon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=searchIcon, borderwidth=0, cursor="hand2", bg="#B0B0B0")
myimage_icon.place(x=400,y=34)


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