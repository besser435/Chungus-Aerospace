
"""
Check Fraud
Launchpad software
This might be written in Java later, idk


https://github.com/besser435?tab=repositories
"""

version = "v0.2"
date = "November 2022" 

debug = 1

import time, sys, os, board
if debug == False: 
    import neopixel, board
    from gpiozero import DigitalOutputDevice
    from gpiozero import InputDevice

from colorama import init   # pip install colorama
init()
from colorama import Fore, Back, Style
init(autoreset=True)


# Setup
if debug == False: 
    # Neopixel
    led_neo = neopixel.NeoPixel(board.D12, 8)     # NeoPixel on D12
    # Beeper
    beeper = DigitalOutputDevice(21)
    # Ignition relay
    ign_relay = DigitalOutputDevice(21)


# options
#debug is above the imports
launch_countdown = 2
ignition_time = 1

# storage


def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal


def beeper_f(state):
    #global beeper
    if debug == False:
        if state == 1:
            beeper.on()
        elif state == 0:
            beeper.off()


def relay(state):
    #global ign_relay
    if debug == False:
        if state == 1:
            ign_relay.on()
        elif state == 0:
            ign_relay.off()
    else:
        print(Fore.LIGHTRED_EX + "(DEBUG) Ignition relay will be " + str(state))


def ignition():
    print(Fore.LIGHTGREEN_EX + "Relay on")
    #led_neo.fill((255, 0, 0))
    relay(1)
    time.sleep(ignition_time)

    relay(0)
    print(Fore.LIGHTGREEN_EX + "Relay off")
    #led_neo.fill((0, 0, 0))
    print()
    main_menu()


def countdown_led():
    for i in range:
        led_neo[i](255, 0, 0)
    

def delay_countdown():  # The type param is so other code can also use the countdown
    global launch_countdown
    #global LAUNCH_COUNTDOWN_INIT
    cc()

    confirm_countdown = input("Are you sure you want to start the countdown? y/n ")
    if confirm_countdown == "y":
        cc()




        countdown_time = input("How long should the countdown be? ")
        try:
            countdown_time = int(countdown_time)
            cc()
        except:
            print(Fore.RED + "Not a number! ")
            main_menu()
        launch_countdown = countdown_time
        #LAUNCH_COUNTDOWN_INIT = launch_countdown # delete this
        




        print(Fore.CYAN + "Starting Countdown. Press CTRL + C to cancel")   
        print()

        for i in range(launch_countdown):
            launch_countdown -= 1
            print(Fore.LIGHTYELLOW_EX + str(launch_countdown))
            #led_neo.fill((255, 0, 0))
            beeper_f(1)
            time.sleep(0.5)

            #led_neo.fill((0, 0, 0))
            beeper_f(0)
            time.sleep(0.5)

            #check if the connection between my pc and the Pi is active.
            #that way if the connection stops it automatically stops the countdown
            #this is incase we need to cancel the countdown
        #launch_countdown = LAUNCH_COUNTDOWN_INIT # reset the countdown
        ignition()
    else:
        cc()
        print(Fore.YELLOW + "Countdown aborted")
        main_menu()


def ignite_now():
    # once delay_countdown() is done, copy and paste that code here
    pass


def main_menu():    

    # print(f"Check Fraud Launchpad Software {version} {date}")
    print("Check Fraud Launchpad Software")
    print(version)
    print(date)
    if debug == True: print(Fore.LIGHTRED_EX + "DEBUG MODE")
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    print("1: Begin Ignition Countdown")
    print("2: Ignite Now")
    #print("3: ")
    print("Q: Quit")
  
    which_option = input("What would you like to do? ")

    if "1" is which_option:
        delay_countdown()
        cc()
        
    elif "2" is which_option:
        cc()

    elif "3" is which_option:
        cc()

    elif "q" is which_option:
        sys.exit()
    
    elif "a" is which_option:  # shortcut to current work
        pass 

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()
main_menu()




