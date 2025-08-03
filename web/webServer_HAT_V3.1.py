#!/usr/bin/env python3
# coding=utf-8
# File name   : webServer_HAT_V3.1.py
# Production  : picar-b2
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/16
import time
import threading
from move import MotorController
import os
import info
import RPIservo

import functions
import robotLight
from robotWS2812 import RobotWS2812
import serial_port
import switch
import Voice_Command
import camera_opencv
import socket
from ADS7830 import ADS7830

import asyncio
import websockets

import json
import app
import Voltage
import Voice_Command
from robotBuzzer import RobotBuzzer

functionMode = 0
speed_set = 20
rad = 0.5
turnWiggle = 60

scGear = RPIservo.ServoCtrl()
scGear.moveInit()

P_sc = RPIservo.ServoCtrl()
P_sc.start()

T_sc = RPIservo.ServoCtrl()
T_sc.start()

buzzer = RobotBuzzer(18)
adc = ADS7830()

modeSelect = 'PT'

init_pwm0 = scGear.initPos[0]
init_pwm1 = scGear.initPos[1]
init_pwm2 = scGear.initPos[2]
init_pwm3 = scGear.initPos[3]
init_pwm4 = scGear.initPos[4]

sherpa_ncnn = Voice_Command.Sherpa_ncnn()
sherpa_ncnn.start()
speech = Voice_Command.Speech()
speech.start()

batteryMonitor = Voltage.BatteryLevelMonitor(buzzer, adc)
batteryMonitor.start()

motor_ctrl = MotorController()
motor_ctrl.setup()

Voice_Command.set_motor_controller(motor_ctrl)
camera_opencv.set_motor_controller(motor_ctrl)

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

direction_command = 'no'
turn_command = 'no'

fuc = functions.Functions(motor_ctrl, scGear, adc)
fuc.setup()
fuc.start()

def servoPosInit():
    scGear.initConfig(2,init_pwm2,1)
    P_sc.initConfig(1,init_pwm1,1)
    T_sc.initConfig(0,init_pwm0,1)


def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    global r
    newline=""
    str_num=str(new_num)
    with open(thisPath+"/RPIservo.py","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open(thisPath+"/RPIservo.py","w") as f:
        f.writelines(newline)


def ap_thread():
    os.system("sudo create_ap wlan0 eth0 Adeept_Robot 12345678")


def functionSelect(command_input, response):
    global functionMode
    if 'scan' == command_input:
        WS2812.led_close()
        # scGear.moveAngle(2, 0)
        if modeSelect == 'PT':
            radar_send = fuc.radarScan()
            response['title'] = 'scanResult'
            response['data'] = radar_send
            time.sleep(0.3)

    elif 'findColor' == command_input:
        if modeSelect == 'PT':
            flask_app.modeselect('findColor')

    elif 'motionGet' == command_input:
        flask_app.modeselect('watchDog')

    elif 'stopCV' == command_input:
        flask_app.modeselect('none')
        switch.switch(1,0)
        switch.switch(2,0)
        switch.switch(3,0)
        time.sleep(0.2)
        scGear.moveAngle(0, 0)
        scGear.moveAngle(1, 0)
        scGear.moveAngle(2, 0)
        motor_ctrl.motorStop()

    elif 'KD' == command_input:
        servoPosInit()
        fuc.keepDistance()
    

    elif 'automatic' == command_input:
        if modeSelect == 'PT':
            scGear.moveAngle(0, 0)
            scGear.moveAngle(1, 0)
            scGear.moveAngle(2, 0)
            fuc.automatic()
        else:
            fuc.pause()

    elif 'automaticOff' == command_input:
        fuc.pause()
        motor_ctrl.motorStop()
        time.sleep(0.2)
        
        scGear.moveAngle(0, 0)
        motor_ctrl.motorStop()

    elif 'trackLine' == command_input:
        servoPosInit()
        WS2812.led_close()
        fuc.trackLine()

    elif 'trackLineOff' == command_input:
        scGear.moveAngle(0, 0)
        fuc.pause()
        motor_ctrl.motorStop()

    elif 'trackLight' == command_input:
        servoPosInit()
        WS2812.led_close()
        fuc.trackLight()

    elif 'trackLightOff' == command_input:
        scGear.moveAngle(0, 0)
        fuc.pause()
        motor_ctrl.motorStop()

    elif 'police' == command_input:
        WS2812.police()

    elif 'policeOff' == command_input:
        WS2812.breath(255,0,255)

    elif 'rainbow' == command_input:
        WS2812.rainbow()

    elif 'rainbowOff' == command_input:
        WS2812.breath(255,0,255)

    elif 'serialPort' == command_input:
        serialPort.command()

    elif 'serialPortOff' == command_input:
        serialPort.pause()

    elif 'speech' == command_input:
        speech.speech()
        pass

    elif 'speechOff' == command_input:
        speech.pause()
        pass


def switchCtrl(command_input, response):
    if 'Switch_1_on' in command_input:
        switch.switch(1,1)

    elif 'Switch_1_off' in command_input:
        switch.switch(1,0)

    elif 'Switch_2_on' in command_input:
        switch.switch(2,1)

    elif 'Switch_2_off' in command_input:
        switch.switch(2,0)

    elif 'Switch_3_on' in command_input:
        switch.switch(3,1)

    elif 'Switch_3_off' in command_input:
        switch.switch(3,0) 


def robotCtrl(command_input, response):
    global direction_command, turn_command
    if 'forward' == command_input:
        direction_command = 'forward'
        motor_ctrl.move(speed_set, 1, "mid")
        RL.both_on(0,255,0)
    
    elif 'backward' == command_input:
        direction_command = 'backward'
        motor_ctrl.move(speed_set, -1, "mid")
        RL.both_on(255,0,0)

    elif 'DS' in command_input:
        direction_command = 'no'
        motor_ctrl.motorStop()
        if turn_command == 'left':
            RL.RGB_left_on(0,255,0)
        elif turn_command == 'right':
            RL.RGB_right_on(0,255,0)
        elif turn_command == 'no':
            RL.both_off()


    elif 'left' == command_input:
        turn_command = 'left'
        scGear.moveAngle(0, 40)
        scGear.moveAngle(3, 40)
        # time.sleep(0.15)
        # move.move(30, 1, "mid")
        RL.RGB_left_on(0,0,255)
        time.sleep(0.15)

    elif 'right' == command_input:
        turn_command = 'right'
        scGear.moveAngle(0,-40)
        scGear.moveAngle(3,-40)
        # time.sleep(0.15)
        # move.move(30, 1, "mid")
        RL.RGB_right_on(0,0,255)
        time.sleep(0.15)

    elif 'TS' in command_input:
        #turn_command = 'no'
        scGear.moveAngle(0, 0)
        #move.motorStop()
        if direction_command == 'forward':
            RL.both_on(0,255,0) # green
        elif direction_command == 'backward':
            RL.both_on(255,0,0) # red
            
        elif direction_command == 'no':
            RL.both_off()

    elif 'lookleft' == command_input:
        P_sc.singleServo(1, 1, 7)

    elif 'lookright' == command_input:
        P_sc.singleServo(1,-1, 7)

    elif 'LRstop' in command_input:
        P_sc.stopWiggle()

    elif 'up' == command_input:
        T_sc.singleServo(2, 1, 7)

    elif 'down' == command_input:
        T_sc.singleServo(2,-1, 7)

    elif 'UDstop' in command_input:
        T_sc.stopWiggle()

    elif 'home' == command_input:
        P_sc.moveServoInit([init_pwm1])
        T_sc.moveServoInit([init_pwm0])
        scGear.moveServoInit([init_pwm2])


def configPWM(command_input, response):
    global init_pwm0, init_pwm1, init_pwm2, init_pwm3, init_pwm4

    if 'SiLeft' in command_input:
        numServo = int(command_input[7:])
        if numServo == 0:
            init_pwm0 -= 1
            T_sc.setPWM(0,init_pwm0)
        elif numServo == 1:
            init_pwm1 -= 1
            P_sc.setPWM(1,init_pwm1)
        elif numServo == 2:
            init_pwm2 -= 1
            scGear.setPWM(2,init_pwm2)

    if 'SiRight' in command_input:
        numServo = int(command_input[8:])
        if numServo == 0:
            init_pwm0 += 1
            T_sc.setPWM(0,init_pwm0)
        elif numServo == 1:
            init_pwm1 += 1
            P_sc.setPWM(1,init_pwm1)
        elif numServo == 2:
            init_pwm2 += 1
            scGear.setPWM(2,init_pwm2)

    if 'PWMMS' in command_input:
        numServo = int(command_input[6:])
        if numServo == 0:
            T_sc.initConfig(0, init_pwm0, 1)
            replace_num('init_pwm0 = ', init_pwm0)
        elif numServo == 1:
            P_sc.initConfig(1, init_pwm1, 1)
            replace_num('init_pwm1 = ', init_pwm1)
        elif numServo == 2:
            scGear.initConfig(2, init_pwm2, 2)
            replace_num('init_pwm2 = ', init_pwm2)


    if 'PWMINIT' == command_input:
        print(init_pwm1)
        servoPosInit()

    elif 'PWMD' in command_input:
        init_pwm0,init_pwm1,init_pwm2,init_pwm3,init_pwm4=90,90,90,90,90
        T_sc.initConfig(0,90,1)
        replace_num('init_pwm0 = ', 90)

        P_sc.initConfig(1,90,1)
        replace_num('init_pwm1 = ', 90)

        scGear.initConfig(2,90,1)
        replace_num('init_pwm2 = ', 90)


def wifi_check():
    try:
        s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
    except:
        ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
        ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
        ap_threading.start()                                  #Thread starts
    
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)

async def recv_msg(websocket):
    global speed_set, modeSelect, motor_ctrl

    while True: 
        response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

        data = ''
        data = await websocket.recv()
        try:
            data = json.loads(data)
        except Exception as e:
            print('not A JSON')

        if not data:
            continue

        if isinstance(data,str):
            robotCtrl(data, response)

            switchCtrl(data, response)

            functionSelect(data, response)

            configPWM(data, response)

            if 'get_info' == data:
                response['title'] = 'get_info'
                response['data'] = [info.get_cpu_tempfunc(), info.get_cpu_use(), info.get_ram_info()]

            if 'wsB' in data:
                try:
                    set_B=data.split()
                    speed_set = int(set_B[1])
                except:
                    pass

            #CVFL
            elif 'CVFL' == data:
                flask_app.modeselect('findlineCV')

            elif 'CVFLColorSet' in data:
                color = int(data.split()[1])
                flask_app.camera.colorSet(color)

            elif 'CVFLL1' in data:
                pos = int(data.split()[1])
                flask_app.camera.linePosSet_1(pos)

            elif 'CVFLL2' in data:
                pos = int(data.split()[1])
                flask_app.camera.linePosSet_2(pos)

            elif 'CVFLSP' in data:
                err = int(data.split()[1])
                flask_app.camera.errorSet(err)

        elif(isinstance(data,dict)):
            if data['title'] == "findColorSet":
                color = data['data']
                flask_app.colorFindSet(color[0],color[1],color[2])

        print(data)
        response = json.dumps(response)
        await websocket.send(response)

async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)

if __name__ == '__main__':
    switch.switchSetup()
    switch.set_all_switch_off()
    WS2812_mark = None

    global flask_app
    flask_app = app.webapp()
    flask_app.startthread()
    
    # Set motor controller for all modules that need it

    # Play startup sound
    buzzer.play_startup_sound()

    try:
        # global WS2812
        WS2812_mark = 1
        WS2812 = RobotWS2812()
        WS2812.start()
        WS2812.breath(70,70,255)
    except:
        WS2812.led_close()
        pass

    serialPort = serial_port.SerialPortReader(WS2812, buzzer, motor_ctrl)
    serialPort.start()
    serialPort.command()

    RL=robotLight.RobotLight()

    while  1:
        wifi_check()
        try:                  #Start server,waiting for client
            start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
            asyncio.get_event_loop().run_until_complete(start_server)
            print('waiting for connection...')
            break
        except Exception as e:
            print(e)
            if WS2812_mark:
                WS2812.set_all_led_color_data(0,0,0)
                WS2812.show()
            else:
                pass
    try:
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(e)
        if WS2812_mark:
            WS2812.set_all_led_color_data(0,0,0)
            WS2812.show()
        else:
            pass
        motor_ctrl.destroy()
