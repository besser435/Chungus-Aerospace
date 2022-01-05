# used to tune the barometer

import requests
from requests.structures import CaseInsensitiveDict
import math # sad

version = "v0.2"
date = "December 2021"

def weather():
    global complete_url
    api_key = ""  # Enter the API key you got from the OpenWeatherMap website
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    zip_code = "85054"
    use_zip = 0
    city_name = "phoenix"
    

    if use_zip == 0:
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    else:
        complete_url = base_url + "appid=" + api_key + "&q=" + zip_code

    print("URL sent: " + complete_url)

    response = requests.get(complete_url)
    x = response.json()


    if x["cod"] != "404":
        if use_zip == 0:
            print("Check weather! Request cities can return the wrong info")
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
weather()


