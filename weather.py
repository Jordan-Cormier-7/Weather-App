from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

root = Tk()  # GUI frame
root.title('Weather App')
root.geometry("900x600+300+200")
root.resizable(False, False)
#root.configure(bg='orange') #GUI background color

# Top search box
searchBox = PhotoImage(file="images/search.png")
myImage = Label(image=searchBox)
myImage.place(x=20, y=20)

textEntry = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#B0B0B0", border=0, fg="white")
textEntry.place(x=50, y=40)
textEntry.focus()

searchIcon = PhotoImage(file="images/search_icon.png")
myimage_icon = Button(image=searchIcon, borderwidth=0, cursor="hand2", bg="#B0B0B0")
myimage_icon.place(x=400, y=34)



# Middle table
table_frame = Frame(root, bg="#B0B0B0", bd=2)
table_frame.place(x=50, y=150, width=800, height=300)

# Columns for today's, tomorrow's, and the day after tomorrow's weather
days = ["Today", "Tomorrow", "Day After Tomorrow"]
for i, day in enumerate(days):
    day_frame = Frame(table_frame, bg="#1ab5ef", bd=2)
    day_frame.grid(row=0, column=i, padx=10, pady=10)

    day_label = Label(day_frame, text=day, font=("Helvetica", 20, 'bold'), fg="white", bg="#1ab5ef")
    day_label.pack(pady=10)

    temp_label = Label(day_frame, text="Temperature:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    temp_label.pack()

    temp_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    temp_value_label.pack()

    desc_label = Label(day_frame, text="Description:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    desc_label.pack()

    desc_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    desc_value_label.pack()

    humidity_label = Label(day_frame, text="Humidity:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    humidity_label.pack()

    humidity_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    humidity_value_label.pack()

    wind_label = Label(day_frame, text="Wind:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    wind_label.pack()

    wind_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    wind_value_label.pack()



# Bottom box
Frame_image = PhotoImage(file="images/BottomBox.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Labels at the bottom
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg='white', bg='#9400D3')
label1.place(x=120, y=500)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#9400D3")
label2.place(x=250, y=500)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg='white', bg='#9400D3')
label3.place(x=430, y=500)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg='white', bg='#9400D3')
label4.place(x=650, y=500)

root.mainloop()
