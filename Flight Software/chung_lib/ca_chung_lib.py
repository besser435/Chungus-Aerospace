import adafruit_icm20x, adafruit_bmp3xx, csv, random, logging


#NOTE https://realpython.com/python-logging/ do this properly


class rocket_systems:
    def __init__(self, starting_alt=None):  
        self.starting_alt = None #NOTE not done
        self.spoof_current_alt = None
        self.spoof_current_accel = None
        pass

    # https://www.geeksforgeeks.org/getter-and-setter-in-python/


    @property
    def current_alt(self):
        if not self.spoof_current_alt:
            return 30 #adafruit_bmp3xx.altitude

    @property
    def current_accel(self):
        """Returns a tuple of the current acceleration in m/s^2, assuming values aren't spoofed."""
        if not self.spoof_current_accel:
            return (0, 0, 9.8) #adafruit_icm20x.acceleration
        #NOTE add spoofed setting. see acceleration function below
        
        # in the future this will read values from a file rather that
        # generating random values. This will be used to test flight code.
        if self.spoof_current_accel:    
            logging.warning("Spoofing current accel values. Not reading from sensor.")
            rand_x = random.randint(-20, 20)
            rand_y = random.randint(-20, 20)
            rand_z = random.randint(-20, 20)
            return (rand_x, rand_y, rand_z)
            

    @property
    def taken_off(self):
        if self.current_alt > self.starting_alt + 5:
            self.has_taken_off = True  # stores the state in the object once set
        return self.has_taken_off
    
    @property
    def landed(self):
        pass
        # see https://discord.com/channels/914767468331929653/938696892659929109/1127196921816154202
        # and new_landing_detection.py

    @property
    def test_func(self):
        return "test"
    
