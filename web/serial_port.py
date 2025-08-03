import serial
import threading
import time
import RPIservo
import move

scGear = RPIservo.ServoCtrl()
scGear.start()

class SerialPortReader(threading.Thread):
    def __init__(self, lights, *args, **kwargs):

        self.lights = lights

        super(SerialPortReader, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    def command(self):
        try:
            self.port = serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1)
            self.port.reset_input_buffer()
       
            self.commandMode = 'active'
            self.resume()
        except:
            print("Serial port is not available")

    def pause(self):
        self.commandMode = 'none'
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def commandProcessing(self):
        while self.commandMode == 'active':
            if self.port.in_waiting > 0:
                line = self.port.readline().decode("utf-8").rstrip()
                print(line)

                if(line == 'rainbow'):
                    self.lights.rainbow()
                elif(line == 'police'):
                    self.lights.police()
                elif(line == 'breath'):
                    self.lights.breath(255, 0, 128)
                elif(line == 'left'):
                    scGear.moveAngle(0, 40)
                elif(line == 'right'):
                    scGear.moveAngle(0, -40)
                elif(line == 'straight'):
                    scGear.moveAngle(0, 0)
                elif(line == 'forward'):
                    move.move(30, 1, "mid")
                elif(line == 'backward'):
                    move.move(30, -1, "mid")
                elif(line == 'stop'):
                    move.motorStop()

            time.sleep(0.03)

            if self.commandMode != 'active':
                break

    def commandChange(self):
        if self.commandMode == 'none':
            self.pause()
        elif self.commandMode == 'active':
            self.commandProcessing()


    def run(self):
        while 1:
            self.__flag.wait()
            self.commandChange()
            pass



if __name__ == '__main__':
    # Test example for WS2812 LED functions
    print("Testing WS2812 LED functionality...")
    
    led = SerialPortReader()
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
