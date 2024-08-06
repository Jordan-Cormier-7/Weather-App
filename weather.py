from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import pytz


root = Tk()  # GUI frame
root.title('Weather App')
root.geometry("900x600+300+200")
root.resizable(False, False)
#root.configure(bg='orange') #GUI background color

def getWeather():
    city=textEntry.get()

    geolocator = Nominatim(user_agent="WeatherApp/1.0")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lng = location.longitude, lat = location.latitude)
    #print(result)

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="TIME IN "+city.upper())


    #Retrieving Weather Info
    load_dotenv() #Loading API key from .env file
    api_key = os.getenv('API_KEY')
    api = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'

    json_data = requests.get(api).json() #Querying the request 
    first_entry = json_data['list'][0] #Data about the first day

    condition = first_entry['weather'][0]['main'] #Basic weather conditions
    description = first_entry['weather'][0]['description'] #More descriptive conditions

    print(f"\nCity: {city}")
    print(f"Day 1: Condition: {condition}")
    print(f"Day 1: Description: {description}")
   
    


#Top search box
searchBox = PhotoImage(file="images/search.png")
myImage = Label(image=searchBox)
myImage.place(x=20, y=20)

textEntry = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#B0B0B0", border=0, fg="white")
textEntry.place(x=50, y=40)
textEntry.focus()

searchIcon = PhotoImage(file="images/search_icon.png")
myimage_icon = Button(image=searchIcon, borderwidth=0, cursor="hand2", bg="#B0B0B0",command=getWeather)
myimage_icon.place(x=400, y=34)


#Current location time
name = Label(root,font=("arial",15,"bold"))
name.place(x=500,y=35)
clock = Label(root,font=("Helvitica",20))
clock.place(x=500,y=65)


# Middle table
table_frame = Frame(root, bg="#B0B0B0", bd=2)
table_frame.place(x=50, y=150, width=800, height=300)

# Columns for today's, tomorrow's, and the day after tomorrow's weather
#days = ["Today", "Tomorrow", "Day After Tomorrow"]
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
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
