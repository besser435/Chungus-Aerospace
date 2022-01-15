"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace


This is just a concept which includes a fancy front end.
Its just to get some ideas down for if we even want to build this.

This is called the launch computer software, but if we
switch over to a Pi it might just be consolidated into one 
package so there is no launch computer.

"""


version = "v0.1.1"
date = "January 2022"

# NOTE use my python template to add the menus

"""
FC = Flight Computer

Get weather data and send that to the FC to calibrate the baro altitude
Prep FC for launch, like start logging a second before the launch for example
Control launchpad LEDs
Send configuration options to the FC

 
Fancy menu UI stuff:
Make a GUI rather than CLI UI, only if the hanging issue is solved. use pygame_menu or something

Checklist
display telem.
Connection to the FC status
Begin launch sequence 
Fetch data on the FC SD card, delete from FC and store on the host
"""



# potential menu concept
"""
This will display telem data, it should update about every second.
Maybe put the menu in a for loop with a 1 second sleep

CALC v2
Status: Idle
Pi Temp: 30c


1.  Prep for launch
2.  Checklist
3.  Display last launch data summary



"""





# the following is just my python template.

def main_notes():   # to collapse the text below in the IDE  
    """
 

    
    https://github.com/besser435?tab=repositories
    """



import random
import time 
import sys
import os  
from colorama import init   # pip install colorama
init()
from colorama import Fore, Back, Style
init(autoreset=True)


# options
debug = 0

# storage


def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal


def main():
    pass







def debug():
    if debug:
        pass


def main_menu():    
    print(" By Besser")
    print(version)
    print(date)
    
    if debug:
        pass
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    print("1: ")
    print("2: ")
    print("3: ")
    print("Q: Quit")
  
    which_option = input("What would you like to do? ")

    if "1" == which_option:
        cc()
        
        
    elif "2" == which_option:
        cc()
        

    elif "3" == which_option:
        cc()


    elif "q" == which_option:
        sys.exit()
    

    elif "a" == which_option:  # shortcut to current work
        pass 

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()
main_menu()




main()
