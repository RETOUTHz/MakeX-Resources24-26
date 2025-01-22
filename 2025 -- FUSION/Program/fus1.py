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
    "LF": encoder_motor_class("M2", "INDEX1"), #Left_Front wheel
    "LB": encoder_motor_class("M1", "INDEX1"), #Lef_Back wheel
    "RF": encoder_motor_class("M4", "INDEX1"), #Right_Front wheel 
    "RB": encoder_motor_class("M6", "INDEX1")  #Right_Back wheel
}

sv = {
    "s6" : smartservo_class("M6","INDEX1")
}

"""
Auto seclet
"""
def select():
    Auto.Left_block_auto()
    #Auto.Right_block_auto()
    #Auto.Emergency()
"""
RANGGING
"""
debug = led_matrix_class("PORT2","INDEX1")
lk = ranging_sensor_class("PORT4", "INDEX1")
bk = ranging_sensor_class("PORT2", "INDEX3")
rk = ranging_sensor_class("PORT2", "INDEX2")
fk = ranging_sensor_class("PORT2", "INDEX1")

"""
SYSTEM
"""
def feed():
    power_expand_board.set_power("DC7",100)


"""
CONTROLLER
"""
class controller():
    def mode1():
        if not gamepad.get_joystick("Rx") == 0:
            en["RF"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["RB"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["LB"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["LF"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))

        elif not gamepad.get_joystick("Lx") == 0:
            en["RF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
            en["RB"].set_speed(gamepad.get_joystick("Lx") / (0.05))
            en["LB"].set_speed(gamepad.get_joystick("Lx") / (0.1))
            en["LF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
    
        elif not gamepad.get_joystick("Ly") == 0:
            en["LB"].set_speed(gamepad.get_joystick("Ly") / 1.7)
            en["LF"].set_speed(gamepad.get_joystick("Ly") / (1.635 * 1))
            en["RF"].set_speed(gamepad.get_joystick("Ly") / (1.635* -1))
            en["RB"].set_speed(gamepad.get_joystick("Ly") / (1.7 * -1))
    
    def mode2():
        if not gamepad.get_joystick("Rx") == 0:
            en["RF"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["RB"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["LB"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))
            en["LF"].set_speed(gamepad.get_joystick("Rx") / (1.95 * -1))

        elif not gamepad.get_joystick("Lx") == 0:
            en["RF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
            en["RB"].set_speed(gamepad.get_joystick("Lx") / (0.05))
            en["LB"].set_speed(gamepad.get_joystick("Lx") / (0.1))
            en["LF"].set_speed(gamepad.get_joystick("Lx") / (0.1 * -1))
    
        elif not gamepad.get_joystick("Ly") == 0:
            en["LB"].set_speed(gamepad.get_joystick("Ly") / 1.7)
            en["LF"].set_speed(gamepad.get_joystick("Ly") / (1.635 * 1))
            en["RF"].set_speed(gamepad.get_joystick("Ly") / (1.635* -1))
            en["RB"].set_speed(gamepad.get_joystick("Ly") / (1.7 * -1))
"""
AUTO
"""
class Auto():
    pass
"""
MANUAL
"""
class Manual():
    pass
"""
MAIN
"""
while True:
    time.sleep(0.001)
    if power_manage_module.is_auto_mode():
        select()
        while not not power_manage_module.is_auto_mode():
            pass
    else:
        controller.mode1() 