#import
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
import mbuild
import time
import math

"""
NovaPI
"""
en = {
    "LF": encoder_motor_class("M1", "INDEX1"), #Left_Front wheel
    "LB": encoder_motor_class("M2", "INDEX1"), #Left_Back wheel
    "RF": encoder_motor_class("M5", "INDEX1"), #Right_Front wheel 
    "RB": encoder_motor_class("M6", "INDEX1"),  #Right_Back wheel
    "FEED": encoder_motor_class("M4", "INDEX1")
}
"""
SYSTEM
"""
def blush(a:int):
    power_expand_board.set_power("BL1",a)

def lift(a:int):
    power_expand_board.set_power("DC7",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC7",-10)

def gripper(a:int):
    power_expand_board.set_power("DC8",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC8",10)

def feed(a:int):
    en["FEED"].set_power(-a)

def stop_all():
    power_expand_board.set_power("DC")

class movement:
    def control_movement_font():            
        rf = (gamepad.get_joystick("Lx") - -gamepad.get_joystick("Rx")) * 0.75
        lb = (gamepad.get_joystick("Lx") + -gamepad.get_joystick("Rx")) * 0.75
        lf = (gamepad.get_joystick("Ly") + -gamepad.get_joystick("Rx")) * 0.75
        rb = (gamepad.get_joystick("Ly") - -gamepad.get_joystick("Rx")) * 0.75
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)
    
    def control_movement_right():
        rf = (gamepad.get_joystick("Ly") - gamepad.get_joystick("Rx")) * 0.75
        lb = (gamepad.get_joystick("Ly") + gamepad.get_joystick("Rx")) * 0.75
        lf = (-gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.75
        rb = (-gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx")) * 0.75
        en["RF"].set_power(rf)
        en["RB"].set_power(rb)
        en["LB"].set_power(-lb)
        en["LF"].set_power(-lf)

"""
CONTROLLER
"""
class controller():
    mode = "1"
    def mode1():
        movement.control_movement_font()
        if gamepad.is_key_pressed("Up"):
            lift(-100)

        elif gamepad.is_key_pressed("Down"):
            lift(100)

        elif gamepad.is_key_pressed("Right"):
            gripper(50)

        elif gamepad.is_key_pressed("Left"):
            gripper(-50)

    def mode2():
        movement.control_movement_right()
        if gamepad.is_key_pressed("N1"):
            feed(100)

        elif gamepad.is_key_pressed("L1"):
            feed(0)

    def change_mode():
        if gamepad.is_key_pressed("+"):
            controller.mode = "1"
        elif gamepad.is_key_pressed("≡"):
            controller.mode = "2"

"""
MAIN
"""
while True:
    controller.change_mode()
    if controller.mode == "1":
        controller.mode1()
    else:
        controller.mode2()
