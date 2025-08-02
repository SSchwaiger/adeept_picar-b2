#!/usr/bin/env python3
# File name   : robotLight.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
import sys
from gpiozero import PWMOutputDevice as PWM
from rpi_ws281x import Adafruit_NeoPixel, Color
import threading
def check_rpi_model():
    _, result = run_command("cat /proc/device-tree/model |awk '{print $3}'")
    result = result.strip()
    if result == '3':
        return 3
    elif result == '4':
        return 4
    elif result == '5':
        return 5
    else:
        return None

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result


def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class RobotWS2812(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.LED_COUNT	  	= 16	  # Number of LED pixels.
        self.LED_PIN		= 12	  # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA		= 10	  # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.colorBreathR = 0
        self.colorBreathG = 0
        self.colorBreathB = 0
        self.breathSteps = 10


        self.lightMode = 'none'		#'none' 'police' 'breath' 'rainbow'


        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        super(RobotWS2812, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    # Define functions which animate LEDs in various ways.
    def set_all_led_color_data(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(int(R),int(G),int(B))
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def setSomeColor(self, R, G, B, ID):
        color = Color(int(R),int(G),int(B))
        for i in ID:
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def pause(self):
        self.lightMode = 'none'
        self.set_all_led_color_data(0,0,0)
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def led_close(self):
        self.lightMode = 'none'
        self.set_all_led_color_data(0,0,0)
        self.__flag.clear()

    def police(self):
        self.lightMode = 'police'
        self.resume()

    def rainbow(self):
        self.lightMode = 'rainbow'
        self.resume()


    def policeProcessing(self):
        while self.lightMode == 'police':
            for i in range(0,3):
                self.setSomeColor(0,0,255,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,255)
                time.sleep(0.05)
                self.setSomeColor(0,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,0)
                time.sleep(0.05)
            if self.lightMode != 'police':
                break
            time.sleep(0.1)
            for i in range(0,3):
                self.setSomeColor(255,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(255,0,0)
                time.sleep(0.05)
                self.setSomeColor(0,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,0)
                time.sleep(0.05)
            time.sleep(0.1)


    def breath(self, R_input, G_input, B_input):
        self.lightMode = 'breath'
        self.colorBreathR = R_input
        self.colorBreathG = G_input
        self.colorBreathB = B_input
        self.resume()


    def breathProcessing(self):
        while self.lightMode == 'breath':
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color_data(self.colorBreathR*i/self.breathSteps, self.colorBreathG*i/self.breathSteps, self.colorBreathB*i/self.breathSteps)
                time.sleep(0.03)
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color_data(self.colorBreathR-(self.colorBreathR*i/self.breathSteps), self.colorBreathG-(self.colorBreathG*i/self.breathSteps), self.colorBreathB-(self.colorBreathB*i/self.breathSteps))
                time.sleep(0.03)

    def rainbowProcessing(self):
        rainbow_offset = 0
        while self.lightMode == 'rainbow':
            for i in range(self.strip.numPixels()):
                if self.lightMode != 'rainbow':
                    break
                # Calculate hue for each LED (0-255)
                hue = (i * 256 // self.strip.numPixels() + rainbow_offset) & 255
                # Convert to RGB using wheel function
                if hue < 85:
                    r = 255 - hue * 3
                    g = hue * 3
                    b = 0
                elif hue < 170:
                    hue -= 85
                    r = 0
                    g = 255 - hue * 3
                    b = hue * 3
                else:
                    hue -= 170
                    r = hue * 3
                    g = 0
                    b = 255 - hue * 3
                
                color = Color(int(r), int(g), int(b))
                self.strip.setPixelColor(i, color)
            
            self.strip.show()
            rainbow_offset = (rainbow_offset + 1) & 255
            time.sleep(0.02)

    def lightChange(self):
        if self.lightMode == 'none':
            self.pause()
        elif self.lightMode == 'police':
            self.policeProcessing()
        elif self.lightMode == 'breath':
            self.breathProcessing()
        elif self.lightMode == 'rainbow':
            self.rainbowProcessing()


    def run(self):
        while 1:
            self.__flag.wait()
            self.lightChange()
            pass






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
    # Test example for WS2812 LED functions
    print("Testing WS2812 LED functionality...")
    
    led = RobotWS2812()
    led.start()
    
    try:
        print("Testing rainbow mode for 10 seconds...")
        led.rainbow()
        time.sleep(10)
        
        print("Testing police mode for 5 seconds...")
        led.police()
        time.sleep(5)
        
        print("Testing breath mode (red) for 5 seconds...")
        led.breath(255, 0, 0)
        time.sleep(5)
        
        print("Testing breath mode (blue) for 5 seconds...")
        led.breath(0, 0, 255)
        time.sleep(5)
        
        print("Test completed. Turning off LEDs...")
        led.led_close()
        
    except KeyboardInterrupt:
        print("\nTest interrupted. Turning off LEDs...")
        led.led_close()
