#!/usr/bin/env python3
# File name   : robotLight.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
import threading
from gpiozero import PWMOutputDevice as PWM

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class RobotLight(threading.Thread):
    def __init__(self, *args, **kwargs):

        self.left_R = 19
        self.left_G = 0
        self.left_B = 13

        self.right_R = 5
        self.right_G = 6
        self.right_B = 1
        
        self.Left_G = PWM(pin=self.left_R,initial_value=1.0, frequency=2000)
        self.Left_B = PWM(pin=self.left_G,initial_value=1.0, frequency=2000)
        self.Left_R = PWM(pin=self.left_B,initial_value=1.0, frequency=2000)
        
        self.Right_G = PWM(pin=self.right_R,initial_value=1.0, frequency=2000)
        self.Right_B = PWM(pin=self.right_G,initial_value=1.0, frequency=2000)
        self.Right_R = PWM(pin=self.right_B,initial_value=1.0, frequency=2000)


    def setRGBColor(self,LED_num, R,G,B):   # For example : (1,  255,0,0)
        if LED_num ==1 :
            R_val = map(R, 0, 255, 0, 1.00)
            G_val = map(G, 0, 255, 0, 1.00)
            B_val = map(B, 0, 255, 0, 1.00)
            self.Left_R.value = 1.0-R_val
            self.Left_G.value = 1.0-G_val
            self.Left_B.value = 1.0-B_val

        elif LED_num == 2:
            R_val = map(R, 0, 255, 0, 1.00)
            G_val = map(G, 0, 255, 0, 1.00)
            B_val = map(B, 0, 255, 0, 1.00)
            self.Right_R.value = 1.0-R_val
            self.Right_G.value = 1.0-G_val
            self.Right_B.value = 1.0-B_val

    def both_on(self,R,G,B):
        self.setRGBColor(1, R,G,B)
        self.setRGBColor(2, R,G,B)

    def RGB_left_on(self,R,G,B):
        self.setRGBColor(1, R,G,B)
        self.setRGBColor(2, 0,0,0)

    def RGB_right_on(self,R,G,B):
        self.setRGBColor(1, 0,0,0)
        self.setRGBColor(2, R,G,B)

    def both_off(self):
        self.setRGBColor(1, 0,0,0)
        self.setRGBColor(2, 0,0,0)

if __name__ == '__main__':
    # Test example for RGB LED functions
    print("Testing RGB LED functionality...")
    
    rgb_light = RobotLight()
    
    try:
        print("Testing both LEDs red...")
        rgb_light.both_on(255, 0, 0)
        time.sleep(2)
        
        print("Testing left LED green...")
        rgb_light.RGB_left_on(0, 255, 0)
        time.sleep(2)
        
        print("Testing right LED blue...")
        rgb_light.RGB_right_on(0, 0, 255)
        time.sleep(2)
        
        print("Turning off all LEDs...")
        rgb_light.both_off()
        
    except KeyboardInterrupt:
        print("\nTest interrupted. Turning off LEDs...")
        rgb_light.both_off()