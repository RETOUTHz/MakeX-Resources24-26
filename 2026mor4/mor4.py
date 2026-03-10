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
import mbuild
import time
import math

en = {
    "LF": encoder_motor_class("M2", "INDEX1"), #Left_Front wheel
    "LB": encoder_motor_class("M1", "INDEX1"), #Lef_Back wheel
    "RF": encoder_motor_class("M4", "INDEX1"), #Right_Front wheel 
    "RB": encoder_motor_class("M6", "INDEX1")  #Right_Back wheel
}

        
"""
MANUAL
"""
def controler():
    if not gamepad.get_joystick("Rx") == 0:
        en["RF"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
        en["RB"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
        en["LB"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))
        en["LF"].set_power(gamepad.get_joystick("Rx") / (1.95 * -1))

    elif not gamepad.get_joystick("Lx") == 0:
        en["RF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
        en["RB"].set_speed(gamepad.get_joystick("Lx") / (0.05))
        en["LB"].set_speed(gamepad.get_joystick("Lx") / (0.1))
        en["LF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
    
    elif not gamepad.get_joystick("Ly") == 0:
        en["LB"].set_power(gamepad.get_joystick("Ly") / 1.7)
        en["LF"].set_power(gamepad.get_joystick("Ly") / (1.635 * 1))
        en["RF"].set_power(gamepad.get_joystick("Ly") / (1.635* -1))
        en["RB"].set_power(gamepad.get_joystick("Ly") / (1.7 * -1))
    
    elif gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC1",-100)
        power_expand_board.set_power("DC2",100)

    elif gamepad.is_key_pressed("L1"):
        power_expand_board.set_power("DC1",0)
        power_expand_board.set_power("DC2",0)
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
        # controler()
        power_extand_board.set_power("DC1",100)
        power_extand_board.set_power("DC2",100)