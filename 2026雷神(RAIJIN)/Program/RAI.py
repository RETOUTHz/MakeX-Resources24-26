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
    "RF": encoder_motor_class("M1", "INDEX1"),
    "RB": encoder_motor_class("M5", "INDEX1"),
    "FEED": encoder_motor_class("M2", "INDEX1"),
    "FEED1": encoder_motor_class("M1", "INDEX1")

}

sv = {
    "tua": smartservo_class("M2", "INDEX1"),
    "shooter": smartservo_class("M4","INDEX1")
    }
"""\
AUTOMATIC
"""
def auto():
    move_forward(59)
    time.sleep(1.5)
    stop_moving()   

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
    en["RF"].set_power(-a)
    en["RB"].set_power(a)

def slide_left(a:int):
    en["LF"].set_power(-a)
    en["LB"].set_power(a)
    en["RF"].set_power(a)
    en["RB"].set_power(-a)

def stop_moving():
    en["LF"].set_power(0)
    en["LB"].set_power(0)
    en["RF"].set_power(0)
    en["RB"].set_power(0)

"""
FUNCTION
"""
def feed(a:int,b:int,c:int):
    en["FEED"].set_power(a)
    power_expand_board.set_power("DC2",b)
    power_expand_board.set_power("DC4",-c)

def shoot(a:int):
    power_expand_board.set_power("DC3",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",0)

def shooting(a:int):
    power_expand_board.set_power("BL1",a)
    power_expand_board.set_power("BL2",a)

def shoot_angle(a:int):
    sv["shooter"].move_to(a,50)

def lift(a:int):
    sv["tua"].set_power(a)
    time.sleep(0.1)
    sv["tua"].set_power(0)
    
"""
MOVEMENT
"""

def control_movement():

    x = -gamepad.get_joystick("Lx") * 0.5
    y = gamepad.get_joystick("Ly") / 1.6
    r = -gamepad.get_joystick("Rx") / 1.6

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
    
    elif gamepad.is_key_pressed("L1"):
        feed(0,0,0)

    elif gamepad.is_key_pressed("Up"):
        lift(50)

    elif gamepad.is_key_pressed("Down"):
        lift(-50)

    elif gamepad.is_key_pressed("L2"):
        feed(-100,-100,-60)
    
    elif gamepad.is_key_pressed("R1"):
        shooting(90)
        shoot_angle(65)   


    elif gamepad.is_key_pressed("R2"):
        shooting(0)
    
    elif gamepad.is_key_pressed("+"):
        shooting(30)
        shoot_angle(50)   

    elif gamepad.is_key_pressed("≡"):
        shooting(80)
        shoot_angle(10)   

    elif gamepad.is_key_pressed("N2"):
        shoot(100)

    elif gamepad.is_key_pressed("N3"):
        shoot(-100)

    elif gamepad.is_key_pressed("N4"):
        feed(0,0,100)

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