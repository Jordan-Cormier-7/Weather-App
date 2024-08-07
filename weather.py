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
from PIL import Image, ImageTk

NUM_FORECAST_DAYS = 5

root = Tk()  # GUI frame
root.title('Weather App')
root.geometry("900x600+300+200")
root.resizable(False, False)
#root.configure(bg='orange') #GUI background color

def update_time():
    city = textEntry.get()  # Get the current city from the entry
    if city:  # Check if a city is entered
        geolocator = Nominatim(user_agent="WeatherApp/1.0")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="TIME IN " + city.upper())

    # Schedule the function to run again after 60000 ms (1 minute)
    root.after(60000, update_time)



def getWeather():

    try:
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
        api = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial'

        json_data = requests.get(api).json() #Querying the request 
       
        for i in range(NUM_FORECAST_DAYS):
            day_data = json_data['list'][i * 8]  #8*3-hour intervals = 1 day

            condition = day_data['weather'][0]['main']  #Basic weather conditions
            description = day_data['weather'][0]['description']  #More descriptive conditions
            temp = int(day_data['main']['temp'])  #Convert from Kelvin to Celsius
            humidity = day_data['main']['humidity']
            wind_speed = day_data['wind']['speed']
            date_txt = day_data['dt_txt'].split(" ")[0] #Get the date part only

            #Calculating high and low for each day
            high = -1000
            low = 1000
            for hour in range(0,8):
                temp_max = json_data['list'][i * 8 + hour]['main']['temp_max']
                temp_min = json_data['list'][i * 8 + hour]['main']['temp_min']

                if temp_max > high:
                    high = temp_max

                if temp_min < low:
                    low = temp_min

            

            #Convert date_txt to a datetime object and get the day of the week
            date_obj = datetime.strptime(date_txt, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A")

            day_frames[i]['date_label'].config(text=day_of_week)
            day_frames[i]['temp_value_label'].config(text=f"{int(high)}°F/{int(low)}°F")
            day_frames[i]['desc_value_label'].config(text=description.capitalize())
            day_frames[i]['humidity_value_label'].config(text=f"{humidity}%")
            day_frames[i]['wind_value_label'].config(text=f"{wind_speed} mph")

        update_time()

    except Exception as e:
        messagebox.showerror('Weather App','Invalid Location!')

    return
   
    


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

# resize the add.png image
original_image = Image.open("images/add.png")
resized_image = original_image.resize((32, 32))  
add_image = ImageTk.PhotoImage(resized_image)


# Favorites button
favorites_button = Button(root, image=add_image, borderwidth=0, bg="#B0B0B0", cursor="hand2")
favorites_button.place(x=797, y=50)  

# Create the Favorites label
favorites_label = Label(root, text="Favorites", font=("Arial", 25, "bold"), bg="#B0B0B0", fg="black")
favorites_label.place(x=680, y=51)  


# Middle table
table_frame = Frame(root, bg="#B0B0B0", bd=2)
table_frame.place(x=50, y=150, width=800, height=300)

# Columns for today's, tomorrow's, and the day after tomorrow's weather
days = ["---"]*5
day_frames = []

for i, day in enumerate(days):
    day_frame = Frame(table_frame, bg="#1ab5ef", bd=2)
    day_frame.grid(row=0, column=i, padx=10, pady=10)
    day_frames.append({
        'frame': day_frame,
        'date_label': None,
        'temp_value_label': None,
        'desc_value_label': None,
        'humidity_value_label': None,
        'wind_value_label': None
    })

    date_label = Label(day_frame, text=day, font=("Helvetica", 20, 'bold'), fg="white", bg="#1ab5ef")
    date_label.pack(pady=10)
    day_frames[i]['date_label'] = date_label

    temp_label = Label(day_frame, text="Temperature:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    temp_label.pack()

    temp_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    temp_value_label.pack()
    day_frames[i]['temp_value_label'] = temp_value_label

    desc_label = Label(day_frame, text="Description:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    desc_label.pack()

    desc_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    desc_value_label.pack()
    day_frames[i]['desc_value_label'] = desc_value_label

    humidity_label = Label(day_frame, text="Humidity:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    humidity_label.pack()

    humidity_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    humidity_value_label.pack()
    day_frames[i]['humidity_value_label'] = humidity_value_label

    wind_label = Label(day_frame, text="Wind:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    wind_label.pack()

    wind_value_label = Label(day_frame, text="N/A", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
    wind_value_label.pack()
    day_frames[i]['wind_value_label'] = wind_value_label


root.mainloop()