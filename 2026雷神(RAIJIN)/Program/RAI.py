"""
MakeSex 2026
"""

import time
import math
import novapi
import mbuild

from mbuild import power_manage_module
from mbuild import power_expand_board
from mbuild import gamepad

from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class

"""
INITIALISATION
"""

en = {
    "LF": encoder_motor_class("M3", "INDEX1"),
    "LB": encoder_motor_class("M5", "INDEX1"),
    "RF": encoder_motor_class("M1", "INDEX1"),
    "RB": encoder_motor_class("M6", "INDEX1"),
}

sv = {
    "tua": smartservo_class("M2", "INDEX1"),
    "shooter": smartservo_class("M4","INDEX1")
    }

mode = "1"

"""
AUTOMATIC
"""
def auto():
    # slide_left(50)
    # time.sleep(0.9) 
    # stop_moving()
    # move_backward(50)
    # time.sleep(0.3)
    # stop_moving()
    # move_forward(50)
    # time.sleep(1.5)
    # stop_moving()
    pass

     

def move_forward(a:int):
    en["LF"].set_power(a)
    en["LB"].set_power(a)
    en["RF"].set_power(-a)
    en["RB"].set_power(-a)

def move_backward(a:int):
    en["LF"].set_power(-a)
    en["LB"].set_power(-a)
    en["RF"].set_power(a)
    en["RB"].set_power(a)

def turn_right(a:int):
    en["LF"].set_power(a)
    en["LB"].set_power(a)
    en["RF"].set_power(a)
    en["RB"].set_power(a)

def turn_left(a:int):
    en["LF"].set_power(-a)
    en["LB"].set_power(-a)
    en["RF"].set_power(-a)
    en["RB"].set_power(-a)

def slide_right(a:int):
    en["LF"].set_power(a)
    en["LB"].set_power(-a)
    en["RF"].set_power(a)
    en["RB"].set_power(-a)

def slide_left(a:int):
    en["LF"].set_power(-a)
    en["LB"].set_power(a)
    en["RF"].set_power(-a)
    en["RB"].set_power(a)

def stop_moving():
    en["LF"].set_power(0)
    en["LB"].set_power(0)
    en["RF"].set_power(0)
    en["RB"].set_power(0)

def stop_all():
    power_expand_board.set_power("DC1",0)
    power_expand_board.set_power("DC2",0)
    power_expand_board.set_power("DC3",0)
    power_expand_board.set_power("DC4",0)
    power_expand_board.set_power("DC5",0)
    power_expand_board.set_power("DC6",0)
    power_expand_board.set_power("DC7",0)
    power_expand_board.set_power("DC8",0)

"""
FUNCTION
"""
def feed(a:int,b:int,c:int):
    power_expand_board.set_power("DC1",-a)
    power_expand_board.set_power("DC2",b)
    power_expand_board.set_power("DC5",c)

def shoot(a:int):
    power_expand_board.set_power("DC3",-a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",0)

def shooting(a:int):
    power_expand_board.set_power("BL1",a)
    power_expand_board.set_power("BL2",a)

def shoot_angle(a:int):
    sv["shooter"].move_to(a,50)

def lift(a:int):
    power_expand_board.set_power("DC4",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC4",0)

def gripper(a:int):
    power_expand_board.set_power("DC6",a)

def doo(a:int):
    power_expand_board.set_power("DC7",a)
    power_expand_board.set_power("DC8",-a)
    
"""
MOVEMENT
"""

def control_movement():

    x = -gamepad.get_joystick("Lx") * 1
    y = gamepad.get_joystick("Ly") / 1.5
    r = -gamepad.get_joystick("Rx") / 1.5

    lf = y + x + r
    rf = y - x - r
    lb = y - x + r
    rb = y + x - r

    #max_power = max(abs(lf), abs(rf), abs(lb), abs(rb), 100)

    lf = lf * 1
    rf = rf * 0.8
    lb = lb * 1
    rb = rb * 2

    en["LF"].set_power(lf)
    en["LB"].set_power(lb)
    en["RF"].set_power(-rf)
    en["RB"].set_power(-rb)


"""
MODE 1
"""

def controller_1():
    control_movement()
    if gamepad.is_key_pressed("N1"):
        feed(100,100,100)
        shoot_angle(90)   

    elif gamepad.is_key_pressed("L1"):
        feed(0,0,0)
        stop_all()

    elif gamepad.is_key_pressed("Up"):
        lift(-100)

    elif gamepad.is_key_pressed("Down"):
        lift(100)

    elif gamepad.is_key_pressed("Left"):
        doo(-90)
        time.sleep(0.1)
        doo(0)

    elif gamepad.is_key_pressed("Right"):
        doo(90)

    elif gamepad.is_key_pressed("L2"):
        feed(-100,-100,-60)

    elif gamepad.is_key_pressed("R1"):
        shooting(60)
        shoot_angle(65)   

    elif gamepad.is_key_pressed("R2"):
        shooting(0)
    
    elif gamepad.is_key_pressed("+"):
        shooting(45)    

    elif gamepad.is_key_pressed("≡"):
        shooting(40)

    elif gamepad.is_key_pressed("N2"):
        shoot(80)

    elif gamepad.is_key_pressed("N3"):
        shoot(-80)

    elif gamepad.is_key_pressed("N4"):
        shooting(80)

def controller_2():
    control_movement()

    if gamepad.is_key_pressed("Up"):
        lift(-75)

    elif gamepad.is_key_pressed("Down"):
        lift(75)

    elif gamepad.is_key_pressed("R1"):
        gripper(-100)

    elif gamepad.is_key_pressed("L1"):
        gripper(100)
        time.sleep(0.1)
        gripper(0)

    elif gamepad.is_key_pressed("N4"):
        stop_all()


def change_mode():
    global mode
    if gamepad.is_key_pressed("L_Thumb"):
        if mode == "1":
            mode = "2"
        else:
            mode = "1"
        time.sleep(0.3)


"""
MAIN
"""

while True:

    if power_manage_module.is_auto_mode():
        auto()
        while power_manage_module.is_auto_mode():
            pass

    else:
        change_mode()
        if mode == "1" :
            controller_1()
        else:
            controller_2()
