def notes():
    """
    NOTE
    ---Chungus Aerospace AIO Rocket Software---
    https://github.com/besser435/Chungus-Aerospace

    This program has everything that Chungus Aerospace needs.


    """

    # potential menu concept
    """
    This will display telem data, it should update about every second.
    Maybe put the menu in a for loop with a 1 second sleep
    Make a GUI rather than CLI UI, only if the hanging issue is solved. use pygame_menu or something

    CALC v2
    Status: Idle
    Pi Temp: 30c

    Options:
    1.  Prep for launch
    2.  Checklist
    3.  Display last launch data summary
    4.  Push last launch to GitHub (maybe automate this, or dont that could be a disaster) # engineering nighmare for me



    """

    """
    Last Launch Summary
    Total burn time:
    Apogee:
    Max speed:


    """


version = "v0.1.2"
date = "January 2022"



import random
import time 
import sys
import os  
from colorama import init   # pip install colorama
init()
from colorama import Fore, Back, Style
init(autoreset=True)
import requests
from requests.structures import CaseInsensitiveDict
import math 



# options
debug = 0

# storage
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"


def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal


def launch_software():
    print("Get lastest version from other file.")

    
def weather():
    global complete_url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    zip_code = "85054"
    use_zip = 1
    city_name = "phoenix"


    if use_zip == 0:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
    else:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + zip_code

    print("URL sent: " + complete_url)

    response = requests.get(complete_url)
    x = response.json()

    
    if x["cod"] != "404":
        if use_zip == 0:
            print("Check weather! Requesting cities can return the wrong info")
            print("Weather in " + city_name)
        else:
            print("Weather in " + str(zip_code))

        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        weather_description = z[0]["description"]
        current_pressure = y["pressure"]
        

        print("Temp in Kelvin = " + str(math.trunc(current_temperature)))
        print("Temp in Celsius = " + str(math.trunc(current_temperature - 273.15)))
        print("Temp in Fahrenheit = " + str(math.trunc((1.8 * current_temperature) - 459.67)))
        print("Description = " + str(weather_description))
        print("Pressure in millibars = " + str(current_pressure))
        print("Pressure in inches of Hg = " + str(round(current_pressure/33.864, 3)))
        #print(x) # prints raw json data
    else:
        print("City Not Found")

    
    def response_code():
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(complete_url, headers=headers)
        print()

        print("Response code: ", end="")
        print(resp.status_code, end="")
        if resp.status_code == 200:
            print(" = Processed request succsessfully")
    response_code()  

    input("Press enter to return to main menu")
    cc()
    main_menu()




def main_menu():    
    print("Chungus Aerospace Software By Besser")
    print(version)
    print(date)
    
    if debug:
        pass
    print()
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    print("1: Start Launch Wizard")
    print("2: Checklist")
    print("3: Display last launch summary")
    #print("4. Push last launch to GitHub")
    print("5. View current sensor data")
    print("6. View weather")
    print("Q: Quit")
  
    which_option = input("What would you like to do? ")

    if "1" == which_option:
        cc()
        
        
    elif "2" == which_option:
        cc()
        main_menu()
        

    elif "3" == which_option:
        cc()

    elif "4" == which_option:
        cc()

    elif "5" == which_option:
        cc()


    elif "6" == which_option:
        cc()
        weather()


    elif "q" == which_option:
        sys.exit()
    

    elif "a" == which_option:  # shortcut to current work
        pass 

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()

def debug_messages():
    if debug:
        pass

main_menu()
