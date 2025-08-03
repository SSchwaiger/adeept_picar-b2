#!/usr/bin/env python3
# File name   : functions.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
import threading
import os
import ultra
import Kalman_filter
from gpiozero import InputDevice

kalman_filter_X =  Kalman_filter.Kalman_filter(0.01,0.1)


curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

def num_import_int(initial):        #Call this function to import data from '.txt' file
	global r
	with open(thisPath+"/RPIservo.py") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				r=line
	begin=len(list(initial))
	snum=r[begin:]
	n=int(snum)
	return n

pwm0_direction = 1
pwm0_init = num_import_int('init_pwm0 = ')
pwm0_max  = 180
pwm0_min  = 0
pwm0_pos  = pwm0_init

pwm1_direction = 1
pwm1_init = num_import_int('init_pwm1 = ')
pwm1_max  = 180
pwm1_min  = 0
pwm1_pos  = pwm1_init

pwm2_direction = 1
pwm2_init = num_import_int('init_pwm2 = ')
pwm2_max  = 180
pwm2_min  = 0
pwm2_pos  = pwm2_init

line_pin_left = 22
line_pin_middle = 27
line_pin_right = 17


class Functions(threading.Thread):
	def __init__(self, motor_ctrl, scGear, adc, *args, **kwargs):

		self.motor_ctrl = motor_ctrl
		self.scGear = scGear
		self.adc = adc

		self.functionMode = 'none'
		self.steadyGoal = 0

		self.scanNum = 3
		self.scanList = [0,0,0]
		self.scanPos = 1
		self.scanDir = 1
		self.rangeKeep = 30
		self.scanRange = 100
		self.scanServo = 1
		self.turnServo = 2
		self.turnWiggle = 200

		super(Functions, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.clear()



	def pwmGenOut(self, angleInput):
		return int(angleInput)

	def setup(self):
		global track_line_left, track_line_middle,track_line_right
		track_line_left = InputDevice(pin=line_pin_right)
		track_line_middle = InputDevice(pin=line_pin_middle)
		track_line_right = InputDevice(pin=line_pin_left)

	def radarScan(self):
		pwm0_min = -90
		pwm0_max =  90

		scan_speed = 1
		result = []

		pwm0_pos = pwm0_max
		self.scGear.moveAngle(1, 0)
		time.sleep(0.8)

		while pwm0_pos>pwm0_min:
			pwm0_pos-=scan_speed
			self.scGear.moveAngle(1, pwm0_pos)
			dist = ultra.checkdist()
			if dist > 200:
				continue
			theta = 90 - pwm0_pos 
			result.append([dist, theta])
			time.sleep(0.02)
	
		self.scGear.moveAngle(1, 0)
		return result


	def pause(self):
		self.functionMode = 'none'
		self.motor_ctrl.motorStop()
		self.__flag.clear()


	def resume(self):
		self.__flag.set()


	def automatic(self):
		self.functionMode = 'Automatic'
		self.resume()


	def trackLine(self):
		self.functionMode = 'trackLine'
		self.resume()


	def keepDistance(self):
		self.functionMode = 'keepDistance'
		self.resume()


	def trackLight(self):
		self.functionMode = 'trackLight'
		self.resume()


	def trackLineProcessing(self):
		status_right = track_line_right.value
		status_middle = track_line_middle.value
		status_left = track_line_left.value
		if status_middle == 0:
			if status_left == 0 and status_right == 1:
				self.scGear.moveAngle(0, 25)
				self.scGear.moveAngle(2, 0)
				time.sleep(0.1)
				self.motor_ctrl.move(30,1,"mid")
			elif status_left == 1 and status_right == 0:
				self.scGear.moveAngle(0,-25)
				self.scGear.moveAngle(2, 0)
				time.sleep(0.1)
				self.motor_ctrl.move(30,1,"mid")
			else:
				self.scGear.moveAngle(0, 0)
				self.scGear.moveAngle(2, 0)
				self.motor_ctrl.move(30,1,"mid")
		elif status_left == 0:
			self.scGear.moveAngle(0,25)
			self.scGear.moveAngle(2,0)
			time.sleep(0.1)
			self.motor_ctrl.move(30,1,"mid")
		elif status_right == 0:
			self.scGear.moveAngle(0,-25)
			self.scGear.moveAngle(2,0)
			time.sleep(0.1)
			self.motor_ctrl.move(30,1,"mid")
		else:
			self.motor_ctrl.move(30,1,"no")
		print(status_left,status_middle,status_right)
		time.sleep(0.1)


	
# Filter out occasional incorrect distance data.
	def distRedress(self): 
		mark = 0
		distValue = ultra.checkdist()
		while True:
			distValue = ultra.checkdist()
			if distValue > 900:
				mark +=  1
			elif mark > 5 or distValue < 900:
					break
			print(distValue)
		return round(distValue,2)

	def automaticProcessing(self):
		print('automaticProcessing')
		dist = self.distRedress()
		print(dist, "cm")
		if dist >= 50:			# More than 50CM, go straight.
			self.scGear.moveAngle(0, 0)
			time.sleep(0.3)
			self.motor_ctrl.move(40, 1, "mid")
			print("Forward")
		# More than 30cm and less than 50cm, detect the distance between the left and right sides.
		elif dist > 30 and dist < 50:	
			self.motor_ctrl.move(0, 1, "mid")
			self.scGear.moveAngle(1, -30)
			time.sleep(0.4)
			distLeft = self.distRedress()
			self.scanList[0] = distLeft

			# Go in the direction where the detection distance is greater.
			self.scGear.moveAngle(1, 30)
			time.sleep(0.4)
			distRight = self.distRedress()
			self.scanList[1] = distRight
			print(self.scanList)
			self.scGear.moveAngle(1, 0)
			if self.scanList[0] >= self.scanList[1]:
				self.scGear.moveAngle(0, -30)
				time.sleep(0.3)
				self.motor_ctrl.move(40, 1, "left")
				print("Left")
			else:
				self.scGear.moveAngle(0, 30)
				time.sleep(0.3)
				self.motor_ctrl.move(40, 1, "right")
				print("Right")
		else:		# The distance is less than 30cm, back.
			self.scGear.moveAngle(0, 0)
			time.sleep(0.3)
			self.motor_ctrl.move(40, -1, "mid")
			print("Back")
		time.sleep(0.4)	
		





	def keepDisProcessing(self):
		distanceGet = self.distRedress()

		print('keepDistanceProcessing: ' + str(distanceGet))
		if distanceGet > 40:
			self.motor_ctrl.move(60, 1, "mid")
		elif distanceGet < 30:
			self.motor_ctrl.move(60, -1, "mid")
		else:
			self.motor_ctrl.motorStop()
		time.sleep(0.3)


	def trackLightProcessing(self):
		light_value = self.adc.analogRead(1)
		print(f'Light tracking value: {light_value}')

		self.motor_ctrl.move(30, 1, "mid")
		
		if light_value < 110:
			self.scGear.steerRight()
		elif light_value > 140:
			self.scGear.steerLeft()
		else:
			self.scGear.steerStraight()
		
		time.sleep(0.1)
   
	def functionGoing(self):
		if self.functionMode == 'none':
			self.pause()
		elif self.functionMode == 'Automatic':
			self.automaticProcessing()
		elif self.functionMode == 'trackLine':
			self.trackLineProcessing()
		elif self.functionMode == 'keepDistance':
			self.keepDisProcessing()
		elif self.functionMode == 'trackLight':
			self.trackLightProcessing()


	def run(self):
		while 1:
			self.__flag.wait()
			self.functionGoing()
			pass


if __name__ == '__main__':
	fuc=Functions()
	try:
		fuc.setup()
		while True:
			fuc.keepDisProcessing()
	except KeyboardInterrupt:
		fuc.motor_ctrl.motorStop()
