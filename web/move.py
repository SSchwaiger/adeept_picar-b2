#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

class MotorController:
    def __init__(self):
        self.MOTOR_M1_IN1 = 15      #Define the positive pole of M1
        self.MOTOR_M1_IN2 = 14      #Define the negative pole of M1
        self.MOTOR_M2_IN1 = 12      #Define the positive pole of M2
        self.MOTOR_M2_IN2 = 13      #Define the negative pole of M2
        self.MOTOR_M3_IN1 = 11      #Define the positive pole of M3
        self.MOTOR_M3_IN2 = 10      #Define the negative pole of M3
        self.MOTOR_M4_IN1 = 8       #Define the positive pole of M4
        self.MOTOR_M4_IN2 = 9       #Define the negative pole of M4
        
        self.M1_Direction = 1
        self.M2_Direction = -1
        
        self.left_forward = 1
        self.left_backward = 0
        
        self.right_forward = 0
        self.right_backward = 1
        
        self.pwn_A = 0
        self.pwm_B = 0
        self.FREQ = 50
        
        self.motor1 = None
        self.motor2 = None
        self.motor3 = None
        self.motor4 = None
        self.pwm_motor = None
    
    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min)/(in_max - in_min) *(out_max - out_min) +out_min
    
    def setup(self): #Motor initialization
        i2c = busio.I2C(SCL, SDA)
        self.pwm_motor = PCA9685(i2c, address=0x5f) #default 0x40
        
        self.pwm_motor.frequency = self.FREQ
        
        self.motor1 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M1_IN1],self.pwm_motor.channels[self.MOTOR_M1_IN2] )
        self.motor1.decay_mode = (motor.SLOW_DECAY)
        self.motor2 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M2_IN1],self.pwm_motor.channels[self.MOTOR_M2_IN2] )
        self.motor2.decay_mode = (motor.SLOW_DECAY)
        self.motor3 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M3_IN1],self.pwm_motor.channels[self.MOTOR_M3_IN2] )
        self.motor3.decay_mode = (motor.SLOW_DECAY)
        self.motor4 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M4_IN1],self.pwm_motor.channels[self.MOTOR_M4_IN2] )
        self.motor4.decay_mode = (motor.SLOW_DECAY)
    
    def motorStop(self): #Motor stops
        self.motor1.throttle = 0
        self.motor2.throttle = 0
        self.motor3.throttle = 0
        self.motor4.throttle = 0
    
    def Motor(self, channel, direction, motor_speed):
        # channel,1~4:M1~M4
        if motor_speed > 100:
            motor_speed = 100
        elif motor_speed < 0:
            motor_speed = 0
        
        speed = self.map(motor_speed, 0, 100, 0, 1.0)
        
        self.pwm_motor.frequency = self.FREQ
        # Prevent the servo from affecting the frequency of the motor
        if direction == -1:
            speed = -speed
        if channel == 1:
            self.motor1.throttle = speed
        elif channel == 2:
            self.motor2.throttle = speed
        elif channel == 3:
            self.motor3.throttle = speed
        elif channel == 4:
            self.motor4.throttle = speed
    
    def move(self, speed, direction):
        #eg: move(100, 1)--->forward
        #    move(100, -1)---> backward
        #speed:0~100. direction:1/-1.
        if speed == 0:
            self.motorStop() #all motor stop.
        else:
            if direction == 1: 			# forward
                self.Motor(1, self.M1_Direction, speed)
            elif direction == -1: 		# backward
                self.Motor(1, -self.M1_Direction, speed)
    
    def video_Tracking_Move(self, speed, direction):   # 0 < radius <= 1  
        #eg: move(100, 1, "no")--->forward
        #    move(100, 1, "left")---> left forward
        #speed:0~100. direction:1/-1. turn: "left", "right", "no".
        if speed == 0:
            self.motorStop() #all motor stop.
        else:
            if direction == 1: 			# forward
                self.Motor(1, self.M1_Direction, speed)
                self.Motor(2, self.M2_Direction, speed)
            elif direction == -1: 		# backward
                self.Motor(1, -self.M1_Direction, speed)
                self.Motor(2, -self.M2_Direction, speed)
    
    def destroy(self):
        self.motorStop()
        if self.pwm_motor:
            self.pwm_motor.deinit()

# Backward compatibility - global instance and functions
_motor_controller = MotorController()

def map(x,in_min,in_max,out_min,out_max):
    return _motor_controller.map(x,in_min,in_max,out_min,out_max)

def setup():
    return _motor_controller.setup()

def motorStop():
    return _motor_controller.motorStop()

def Motor(channel,direction,motor_speed):
    return _motor_controller.Motor(channel,direction,motor_speed)

def move(speed, direction):
    return _motor_controller.move(speed, direction)

def video_Tracking_Move(speed, direction):
    return _motor_controller.video_Tracking_Move(speed, direction)

def destroy():
    return _motor_controller.destroy()

if __name__ == '__main__':
    try:
        speed_set = 20
        setup()
        move(speed_set, -1)
        time.sleep(3)
        motorStop()
        time.sleep(1)
        move(speed_set, 1)
        time.sleep(3)
        motorStop()
    except KeyboardInterrupt:
        destroy()