import time, random
"""

counter = 0
def test():
    while True:
        global counter
        counter = counter + 1 
        time.sleep(0.1)
        rand = random.randint(0, 3)
        print("counter: " + str(counter))
        print("rand: " + str(rand))
        if rand == 1: 
            raise Exception("test exception")

    
#while True:
try:
    print("running test")
    test()
except Exception as e:
    print("error. " + str(e))
    print("restarting test")
    test()
 
"""

while True:
    while True:
        try:
            print("running test")
            rand = random.randint(0, 3)
            print("rand: " + str(rand))
            if rand == 1: 
                raise Exception("test exception")

        except Exception as e:
            print("error. " + str(e))
            #continue
        #break