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
    "RB": encoder_motor_class("M6", "INDEX1")  #Right_Back wheel
}

class movement:
    def control_movement_font():
        rf = (gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx")) * 0.75
        lb = (gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.75
        lf = (gamepad.get_joystick("Ly") + gamepad.get_joystick("Rx")) * 0.75
        rb = (gamepad.get_joystick("Ly") - gamepad.get_joystick("Rx")) * 0.75
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)
    
    def control_movement_right():
        rf = (gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx")) * 0.75
        lb = (gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.75
        lf = (gamepad.get_joystick("Ly") + gamepad.get_joystick("Rx")) * 0.75
        rb = (gamepad.get_joystick("Ly") - gamepad.get_joystick("Rx")) * 0.75
        en["RF"].set_power(rf)
        en["RB"].set_power(rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)

"""
CONTROLLER
"""
class controller():
    def mode1():
        movement.control_movement_font()
    
    def mode2():
        movement.control_movement_right()

"""
MAIN
"""
while True:
    controller.mode2()
