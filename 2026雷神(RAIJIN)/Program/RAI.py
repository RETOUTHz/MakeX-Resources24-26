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
    "LB": encoder_motor_class("M4", "INDEX1"),
    "RF": encoder_motor_class("M6", "INDEX1"),
    "RB": encoder_motor_class("M1", "INDEX1"),
    "FEED": encoder_motor_class("M2", "INDEX1"),
    "FEED1": encoder_motor_class("M1", "INDEX1")

}

sv = {
    "tua": smartservo_class("M2", "INDEX1"),
    "shooter": smartservo_class("M4","INDEX1")
    }
"""
AUTOMATIC
"""
def auto():
    power_expand_board.set_power("DC6",-100)
    time.sleep(1.5)
    power_expand_board.set_power("DC6",-10)
    slide_right(50)
    time.sleep(0.9) 
    stop_moving()
    move_backward(50)
    time.sleep(0.3)
    stop_moving()
    move_forward(50)
    time.sleep(1.5)
    stop_moving()
    # turn_right(40)
    # time.sleep(1)
    # stop_moving()
    # gripper(100)
    # slide_left(40)
    # time.sleep(1)
    # stop_moving()
    # time.sleep(2)
    # stop_moving()
    # slide_right(40)
    # time.sleep(2)
    # stop_moving()
    # gripper(-100)
    # time.sleep(3)
    # stop_all()
     

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
    power_expand_board.set_power("DC5",a)
    power_expand_board.set_power("DC2",b)
    power_expand_board.set_power("DC4",-c)

def shoot(a:int):
    power_expand_board.set_power("DC3",a)
    power_expand_board.set_power("DC1",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",0)
    power_expand_board.set_power("DC1",0)


def shooting(a:int):
    power_expand_board.set_power("BL1",a)
    power_expand_board.set_power("BL2",a)

def shoot_angle(a:int):
    sv["shooter"].move_to(a,50)

def lift(a:int):
    power_expand_board.set_power("DC6",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC6",-10)

def gripper(a:int):
    power_expand_board.set_power("DC7",-a)
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

    lf = lf * 100 / 100
    rf = rf * 100 / 100
    lb = lb * 100 / 100
    rb = rb * 100 / 100

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
        power_expand_board.set_power("DC3",100)
        shoot_angle(90)   

    elif gamepad.is_key_pressed("L1"):
        feed(0,0,0)
        stop_all()

    elif gamepad.is_key_pressed("Up"):
        lift(-100)

    elif gamepad.is_key_pressed("Down"):
        lift(100)

    elif gamepad.is_key_pressed("Left"):
        gripper(-100)
        time.sleep(0.01)
        gripper(0)

    elif gamepad.is_key_pressed("Right"):
        gripper(100)

    elif gamepad.is_key_pressed("L2"):
        feed(-100,-100,-60)
        power_expand_board.set_power("DC3",100)
        gripper(-100)

    elif gamepad.is_key_pressed("R1"):
        shooting(65)
        shoot_angle(65)   

    elif gamepad.is_key_pressed("R2"):
        shooting(0)
    
    elif gamepad.is_key_pressed("+"):
        shooting(50)

    elif gamepad.is_key_pressed("≡"):
        shooting(40)

    elif gamepad.is_key_pressed("N2"):
        shoot(70)
        shoot_angle(0)   

    elif gamepad.is_key_pressed("N3"):
        shoot(-70)

    elif gamepad.is_key_pressed("N4"):
        shooting(100)

    

"""
MAIN
"""

while True:

    if power_manage_module.is_auto_mode():
        auto()
        while power_manage_module.is_auto_mode():
            pass

    else:
        controller_1()
