#Jordan Cormier, Hedie Yazdanparast
#Dr. Smith, CSCI 4900 
#Final Project
#GUI Weather App


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
import random
from PIL import Image, ImageTk

NUM_FORECAST_DAYS = 5

root = Tk()  #GUI frame
root.title('Weather App')
root.geometry("900x600+300+200") 

#Setting background image
background_image = Image.open("images/Weather Background.png")  # Replace with your image path
background_image = background_image.resize((2400, 2400), Image.LANCZOS)  # Resize to fit the window
bg_image = ImageTk.PhotoImage(background_image)

# Create a label for the background image
background_label = Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)  # Fill the entire window


#List of fun weather facts
fun_facts = [
    "Did you know there are over 10 different types of clouds?",
    "Lightning strikes the Earth about 100 times per second!",
    "The coldest temperature ever recorded was -128.6°F in Antarctica.",
    "Mawsynram, India, holds the record for the highest average rainfall.",
    "You can tell the temperature by counting a cricket's chirps!",
    "About 2,000 thunderstorms strike down on Earth every minute.",
    "Cape Farewell in Greenland is the windiest place on the planet.",
    "Waterspouts, or rotating columns of air over water, can make sea creatures rain down from the sky.",
    "Lightning often follows a volcanic eruption.",
    "A heatwave can make train tracks bend!",
]

#Function that displays a random fact
def display_random_fact():
    fact = random.choice(fun_facts)
    fact_label.config(text="Fun fact: "+fact)

#Label for fact
fact_label = Label(root, text="", font=("Arial", 20), bg="#34eb6b")
fact_label.place(x=500, y=650)  # Adjust position as needed


#Function that constantly updates the time while app is running
def update_time():
    city = textEntry.get()  #Getting the current city from the entry
    if city:  #Checking if a city is entered
        geolocator = Nominatim(user_agent="WeatherApp/1.0")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        location_name.config(text="TIME IN " + city.upper())

    #Scheduling function to run again after 60000 ms (1 minute)
    root.after(60000, update_time)


#Function to add a city to favorites
def add_to_favorites():
    city = textEntry.get()
    if city and city not in favorites:
        favorites.append(city)
        update_favorites_list()
        messagebox.showinfo('Weather App','Location added to Favorites.')
    else:
        messagebox.showinfo('Weather App', 'Location already in favorites or location invalid!')

    update_favorites_combobox()


#Function to update favorites combobox
def update_favorites_combobox():
    favorites_combobox['values'] = ["Favorites"] + favorites
    favorites_combobox.current(0)  # Reset to header


#Function to update favorites list
def update_favorites_list():
    favorites_combobox['values'] = favorites
    if favorites:
        favorites_combobox.current(0)


#Function to fetch weather data for favorite location
def get_weather_for_favorite(event):
    selected_city = favorites_combobox.get()
    textEntry.delete(0, END)
    textEntry.insert(0, selected_city)
    getWeather()


#Function to get weather forecast of searched location
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
        location_name.config(text="TIME IN "+city.upper())



        #Retrieving Weather Info
        load_dotenv() #Loading API key from .env file
        api_key = os.getenv('API_KEY')
        api = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial'

        json_data = requests.get(api).json() #Querying the request 
       
        for i in range(NUM_FORECAST_DAYS):
            day_data = json_data['list'][i * 8]  #8*3-hour intervals = 1 day

            #condition = day_data['weather'][0]['main']  Basic weather conditions
            #temp = int(day_data['main']['temp'])  #Convert from Kelvin to Celsius
            description = day_data['weather'][0]['description']  #More descriptive conditions
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

        update_time() #Updates clock in real time
        display_random_fact()

    except Exception as e:
        messagebox.showerror('Weather App','Invalid Location!')

    return


#Top search box
searchBox = PhotoImage(file="images/search.png")
myImage = Label(image=searchBox)
myImage.place(x=20, y=20)

#Text content of searched location
textEntry = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#B0B0B0", border=0, fg="white")
textEntry.place(x=50, y=40)
textEntry.focus()

#Search icon 
searchIcon = PhotoImage(file="images/search_icon.png")
myimage_icon = Button(image=searchIcon, borderwidth=0, cursor="hand2", bg="#B0B0B0",command=getWeather)
myimage_icon.place(x=400, y=34)


#Current location time
location_name = Label(root,font=("arial",15,"bold"))
location_name.place(x=500,y=35)
clock = Label(root,font=("Helvitica",20))
clock.place(x=500,y=65)

#Resizing add.png image
original_image = Image.open("images/add.png")
resized_image = original_image.resize((42, 42))  
add_image = ImageTk.PhotoImage(resized_image)

#Array for favorite locations
favorites = []

#Favorites label
favorites_label = Label(root, text="Add Location to Favorites", font=("Arial", 25, "bold"), bg="yellow")
favorites_label.place(x=900, y=50)  

#Favorites button
favorites_button = Button(root, image=add_image, borderwidth=0, bg="white", cursor="hand2",fg="black",command=add_to_favorites)
favorites_button.place(x=1309, y=50)  

# Dropdown menu for favorite locations
favorites_combobox = ttk.Combobox(root, font=("Arial", 20), state="readonly")
favorites_combobox.place(x=1370, y=55)
favorites_combobox['values'] = ["Favorites"]  #Default header
favorites_combobox.current(0)  #Setting the default selection
favorites_combobox.bind("<<ComboboxSelected>>", get_weather_for_favorite)


#Forecast Table Positioning
table_frame = Frame(root, bg="#0952e3", bd=2)
table_frame.place(x=550, y=270, width=820, height=370)

#Columns for Forecast table
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

    temp_label = Label(day_frame, text="HI/LOW:", font=("Helvetica", 15), fg="white", bg="#1ab5ef")
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
