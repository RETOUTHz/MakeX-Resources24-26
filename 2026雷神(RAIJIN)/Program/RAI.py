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
    "LF": encoder_motor_class("M2", "INDEX1"),
    "LB": encoder_motor_class("M1", "INDEX1"),
    "RF": encoder_motor_class("M5", "INDEX1"),
    "RB": encoder_motor_class("M4", "INDEX1"),
    "BL": encoder_motor_class("M6", "INDEX1"),
}

sv = {
    "tua": smartservo_class("M5", "INDEX1"),
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
    en["BL"].set_power(0)

"""
FUNCTION
"""
def feed(a:int,b:int):
    power_expand_board.set_power("DC1",a)
    en["BL"].set_power(b)
    
def shoot(a:int):
    power_expand_board.set_power("DC3",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",0)

def shooting(a:int):
    power_expand_board.set_power("BL1",a)
    power_expand_board.set_power("BL2",a)

def box_angle(a:int):
    sv["tua"].move_to(a,50)

def lift(a:int):
    power_expand_board.set_power("DC8",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC8",0)

def gripper(a:int):
    power_expand_board.set_power("DC7",a)

def doo(a:int,b:int):
    power_expand_board.set_power("DC5",a)
    power_expand_board.set_power("DC6",b)

def red_servo():
    if sv["tua"].get_value("current") > 1350:
        sv["tua"].set_power(0)
    
"""
MOVEMENT
"""

def control_movement_me():

    x = -gamepad.get_joystick("Lx") * 1
    y = gamepad.get_joystick("Ly") / 1.5
    r = -gamepad.get_joystick("Rx") / 1.2

    lf = + y + x + r
    rf = + y - x - r
    lb = + y - x + r
    rb = - y - x + r

    #max_power = max(abs(lf), abs(rf), abs(lb), abs(rb), 100)

    lf = lf * 0.8
    rf = rf * 0.8
    lb = lb * 0.8
    rb = rb * 1

    en["LF"].set_power(lf)
    en["LB"].set_power(lb)
    en["RF"].set_power(-rf)
    en["RB"].set_power(-rb)
  
def control_movement_on_left():
        rf = (gamepad.get_joystick("Ly") - -gamepad.get_joystick("Rx"))
        lb = (gamepad.get_joystick("Ly") + -gamepad.get_joystick("Rx"))
        lf = (-gamepad.get_joystick("Lx") + -gamepad.get_joystick("Rx"))
        rb = (gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx"))
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)

def control_movement_on_font():
        rf = (gamepad.get_joystick("Lx") - -(gamepad.get_joystick("Rx")*0.8))
        lb = (gamepad.get_joystick("Lx") + -(gamepad.get_joystick("Rx")*0.8))
        lf = (gamepad.get_joystick("Ly") + -(gamepad.get_joystick("Rx")*0.8))
        rb = (-gamepad.get_joystick("Ly") - (gamepad.get_joystick("Rx")*0.8))
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)

"""
MODE 1
"""

def controller_1():
    control_movement_on_font()
    
    if gamepad.is_key_pressed("N1"):
        feed(100,-100)
        box_angle(10)

    elif gamepad.is_key_pressed("L1"):
        shooting(45)

    elif gamepad.is_key_pressed("Up"):
        doo(-100,-100)
        time.sleep(0.1)
        doo(0,0)

    elif gamepad.is_key_pressed("Down"):
        doo(100,100)

    elif gamepad.is_key_pressed("L2"):
        feed(-100,100)

    elif gamepad.is_key_pressed("R1"):
        shooting(0)

    elif gamepad.is_key_pressed("R2"):
        shooting(55)
    
    elif gamepad.is_key_pressed("+"):
        shooting(50)    

    elif gamepad.is_key_pressed("≡"):
        pass
    elif gamepad.is_key_pressed("N2"):
        shoot(100)

    elif gamepad.is_key_pressed("N3"):
        shoot(-100)

    elif gamepad.is_key_pressed("N4"):
        stop_all()

    elif gamepad.is_key_pressed("Left"):
        box_angle(0)
    
    elif gamepad.is_key_pressed("Right"):
        box_angle(80)

def controller_2():
    control_movement_on_left()

    if gamepad.is_key_pressed("L1"):
        gripper(100)

    elif gamepad.is_key_pressed("Up"):
        lift(100)

    elif gamepad.is_key_pressed("Down"):
        left(-100)

    elif gamepad.is_key_pressed("R1"):
        gripper(-100)

def change_mode():
    global mode
    if gamepad.is_key_pressed("L_Thumb"):
        if mode == "1":
            mode = "2"
        else:
            mode = "1"
        time.sleep(0.3)

# def change_mode():
#     global mode
#     if gamepad.is_key_pressed("+"):
#         mode = "1" 
#     elif gamepad.is_key_pressed("≡"):
#         mode = "2"

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
            red_servo()
        else:
            controller_2()
            red_servo()