import adafruit_icm20x, adafruit_bmp3xx, csv, random, logging, numpy as np, time


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
    
class orientation:

    radconv = np.pi / 180
    def rate_gyro_quaternion(angular_vx, angular_vy, angular_vz, quat_initial, time_0):
        """Calculate orientation in quaternions using rate gyro with angular velocities (deg/s), initial orientation, initial time, returning new orientation and time"""
        quat_v = np.array([0, angular_vx, angular_vy, angular_vz]) * radconv # Representation of angular velocity measurements as quaternions
        # Quaternion multiplication
            # Product for each element
        quat_v_relative_1 = quat_initial[0] * quat_v[0] - quat_initial[1] * quat_v[1] - quat_initial[2] * quat_v[2] - quat_initial[3] * quat_v[3]
        quat_v_relative_2 = quat_initial[0] * quat_v[1] + quat_initial[1] * quat_v[0] + quat_initial[2] * quat_v[3] - quat_initial[3] * quat_v[2]
        quat_v_relative_3 = quat_initial[0] * quat_v[2] - quat_initial[1] * quat_v[3] + quat_initial[2] * quat_v[0] + quat_initial[3] * quat_v[1]
        quat_v_relative_4 = quat_initial[0] * quat_v[3] + quat_initial[1] * quat_v[2] - quat_initial[2] * quat_v[1] + quat_initial[3] * quat_v[0]
    
        quat_v_relative = np.array([quat_v_relative_1, quat_v_relative_2, quat_v_relative_3, quat_v_relative_4]) * 0.5  # Array with each new quaternion element, representing change relative to earth

        time_1 = time.monotonic()
        quat_orientation_int = np.add(quat_orientation_int, quat_v_relative * (time_1 - time_0))    # Riemann sum integral 
        norm = np.sqrt(quat_orientation_int[0]**2 + quat_orientation_int[1]**2 + quat_orientation_int[2]**2 + quat_orientation_int[3]**2) # Normalization for quaternion
        quat_orientation = quat_orientation_int / norm   # Final quaternion measurement
        return quat_orientation, time_1