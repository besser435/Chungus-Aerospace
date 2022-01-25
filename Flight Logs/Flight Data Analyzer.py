"""


"""
version = "v0.1"


import sys
import os
import pandas as pd


def cd():  
    try:
        abspath = os.path.abspath(sys.argv[0])
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        print("CWD: " + os.getcwd())
        print()
    except:
        print("CD error")
cd()


file = pd.read_csv("launch.csv")


def main():
    altitude = file["Altitude (m)"].max()
    time = file["Elapsed Seconds"]


    print("Max altitude:                     " + str(altitude) + "m")

    print("Max vertical speed:               " + str(time))    




    print("Average time between data cycles: " )
    print("Average data cycles per second:   " )



main()


input("Press enter to close ")