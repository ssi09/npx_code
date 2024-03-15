# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 14:40:47 2024

@author: Kyungsoo
"""



import RPi.GPIO as GPIO
from time import time, sleep
from datetime import datetime
from pwm import PWM
import multiprocessing as mp
from random import randint


# Task Constants
START_WAIT_TIME = 2

# Camera Constants
PWM_PERIOD = 5363000 # Reliably gets 200 fps
PWM_DUTY = round(PWM_PERIOD/2)

# File Path Constants
PATH = '/home/pi/r4w/'

# GPIO Pin Constants
PIN_CAM_INPUT = 17
PIN_SYNC_TRIG = 22

        
def run_sync():
    """Randomly activates the sync pin that is transmitted to both 
       Neuropixels and OpenEphys. Frequency is 1 Hz, random duty cycle. 
    
    Args:
        None.
    
    Returns:
        None.
    """
    while True:
        on_time = randint(150,700)/1000
        GPIO.output(PIN_SYNC_TRIG, GPIO.HIGH)
        sleep(on_time)
        GPIO.output(PIN_SYNC_TRIG, GPIO.LOW)
        sleep(1-on_time)

def kill_process(process):
    """Terminates a process and ensures it is no longer alive.
    
    Args:
        process is a multiprocessing.Process() object
    
    Returns:
        None.
    """
    while True:
        process.terminate()
        if process.is_alive() == False:
            break

def main():
    """sleep recording """

    try:
        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_CAM_INPUT, GPIO.IN)
        GPIO.setup(PIN_SYNC_TRIG, GPIO.OUT)
        GPIO.output(PIN_SYNC_TRIG, GPIO.LOW)
        
        # Camera Setup - connect both cameras to the same output
        camera = PWM(1) #Defaults to GPIO19
        camera.export()
        camera.period = PWM_PERIOD
        camera.duty_cycle = PWM_DUTY
        
        #sync start
        sync_process = mp.Process(target=run_sync,args=())
        sync_process.start()
        
        camera.enable = True
        
        # sleep recording
        
        sleep(10)
        camera.enable = False
        camera.unexport()
        
     
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Beginning exit process.")

    
    finally:
        print("Cleaning up and closing program...")
        camera.enable = False
        camera.unexport()
        kill_process(sync_process)
        GPIO.cleanup()
        print("Cleanup done.")
                            
if __name__ == '__main__':
    main()
                
            
