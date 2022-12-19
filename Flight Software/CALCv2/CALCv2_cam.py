from picamera import PiCamera
import time
def camera():
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 60

    #https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7#:~:text=Set%20the%20image%20exposure%20mode
    camera.exposure_mode = "antishake"

    #https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7#:~:text=Change%20the%20image%20white%20balance
    camera.awb_mode = "auto"


    
    camera.start_preview()
    print("Starting preview")
    time.sleep(3)
    countdown_cam_check = 1 # camera is ready to record
    # this probably adds a race condition when threaded rip
    camera.start_recording("/home/pi/Desktop/video.h264")
    print("Starting recording")
    time.sleep(10)
    
    #camera.wait_recording(5) 
    # https://picamera.readthedocs.io/en/release-1.13/recipes1.html#:~:text=start_recording(%27my_video.h264%27)-,camera.wait_recording(60),-camera.stop_recording()
    camera.stop_recording()
    camera.stop_preview()
    print("Stopped camera")
camera()