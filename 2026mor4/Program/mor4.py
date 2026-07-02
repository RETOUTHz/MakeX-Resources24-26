"""
MakeSex 2026
"""
import novapi
from mbuild import power_manage_module
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.smart_camera import smart_camera_class
from mbuild.led_matrix import led_matrix_class
from mbuild.button import button_class
from mbuild.ai_camera import ai_camera_class
import mbuild
import time
import math

en = {
    "LF": encoder_motor_class("M2", "INDEX1"), #Left_Front wheel
    "LB": encoder_motor_class("M1", "INDEX1"), #Lef_Back wheel
    "RF": encoder_motor_class("M4", "INDEX1"), #Right_Front wheel 
    "RB": encoder_motor_class("M6", "INDEX1")  #Right_Back wheel
}

sv = {
    "shooter" : smartservo_class("M5","INDEX1")
}

mode = "1"
"""
CONTROLLER FUNCTION
"""
def feed(a:int,b:int,c:int):
    power_expand_board.set_power("DC1",a)
    power_expand_board.set_power("DC2",b)
    power_expand_board.set_power("DC3",c)

def stop_feed():
    power_expand_board.set_power("DC1",0)
    power_expand_board.set_power("DC2",0)
    power_expand_board.set_power("DC3",0)

def lift(a:int):
    power_expand_board.set_power("DC4",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC4",0)

def gripper(a:int):
    power_expand_board.set_power("DC5",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC5",0)

def red_servo():
    if sv["shooter"].get_value("current") > 1250:
        sv["shooter"].set_power(0)

def servo_move(angle):
        sv["shooter"].move_to(angle, 50)

def control_movement():

    x = gamepad.get_joystick("Lx")
    y = gamepad.get_joystick("Ly")
    r = gamepad.get_joystick("Rx") * 0.9

    lf = y + x + r
    rf = y - x - r
    lb = y - x + r
    rb = y + x - r

    max_power = max(abs(lf), abs(rf), abs(lb), abs(rb), 100)

    lf = lf * 100 / max_power
    rf = rf * 100 / max_power
    lb = lb * 100 / max_power
    rb = rb * 100 / max_power

    en["LF"].set_power(lf)
    en["LB"].set_power(lb)
    en["RF"].set_power(-rf) 
    en["RB"].set_power(-rb)
"""
MANUAL
"""
def controler_1():
    mode = "1"
    # if not gamepad.get_joystick("Rx") == 0:
    #     en["RF"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["RB"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["LB"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["LF"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))

    # elif not gamepad.get_joystick("Lx") == 0:
    #     en["RF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
    #     en["RB"].set_speed(gamepad.get_joystick("Lx") / (0.05))
    #     en["LB"].set_speed(gamepad.get_joystick("Lx") / (0.1))
    #     en["LF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
    
    # elif not gamepad.get_joystick("Ly") == 0:
    #     en["LB"].set_power(gamepad.get_joystick("Ly") / 1.7)
    #     en["LF"].set_power(gamepad.get_joystick("Ly") / (1.635 * 1))
    #     en["RF"].set_power(gamepad.get_joystick("Ly") / (1.635* -1))
    #     en["RB"].set_power(gamepad.get_joystick("Ly") / (1.7 * -1))
    if gamepad.is_key_pressed("N1"):
        feed(100,100,100)

    elif gamepad.is_key_pressed("N2"):
        feed(100,100,100)
        time.sleep(0.1)
        stop_feed()

    elif gamepad.is_key_pressed("N3"):
        feed(-100,-100,-100)
        time.sleep(0.1)
        stop_feed()

    elif gamepad.is_key_pressed("L1"):
        stop_feed()
    
    else:
        en["RF"].set_power(0)
        en["RB"].set_power(0)
        en["LB"].set_power(0)
        en["LF"].set_power(0)

def controler_2():
    mode = "2"
    # if not gamepad.get_joystick("Rx") == 0:
    #     en["RF"].set_power(-gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["RB"].set_power(-gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["LB"].set_power(-gamepad.get_joystick("Rx") / (1.95 * -1))
    #     en["LF"].set_power(-gamepad.get_joystick("Rx") / (1.95 * -1))

    # elif not gamepad.get_joystick("Lx") == 0:
    #     en["RF"].set_speed(-gamepad.get_joystick("Lx") / (0.1 * -1))
    #     en["RB"].set_speed(-gamepad.get_joystick("Lx") / (0.05))
    #     en["LB"].set_speed(-gamepad.get_joystick("Lx") / (0.1))
    #     en["LF"].set_speed(-gamepad.get_joystick("Lx") / (0.1 * -1))
    
    # elif not gamepad.get_joystick("Ly") == 0:
    #     en["LB"].set_power(-gamepad.get_joystick("Ly") / 1.7)
    #     en["LF"].set_power(-gamepad.get_joystick("Ly") / (1.635 * 1))
    #     en["RF"].set_power(-gamepad.get_joystick("Ly") / (1.635* -1))
    #     en["RB"].set_power(-gamepad.get_joystick("Ly") / (1.7 * -1))
    
    if gamepad.is_key_pressed("Up"):
        lift(100)
    
    elif gamepad.is_key_pressed("Down"):
        lift(-100)
        
    elif gamepad.is_key_pressed("N1"):
        gripper(100)
    
    elif gamepad.is_key_pressed("N2"):
        gripper(-100)
    
    elif gamepad.is_key_pressed("N3"):
        gripper(0)
    
    elif gamepad.is_key_pressed("L1"):
        stop_feed()

def change_mode():
    global mode
    if gamepad.is_key_pressed("+"):
        mode = "1"
    elif gamepad.is_key_pressed("≡"):
        mode = "2"
    

"""
MAIN
"""

while True:
    time.sleep(0.001)
    if power_manage_module.is_auto_mode():
        pass
        while not not power_manage_module.is_auto_mode():
            pass
    else:
        change_mode()
        if mode == "1":
            control_movement()
            controler_1()
        elif mode == "2":
            control_movement()
            controler_2()