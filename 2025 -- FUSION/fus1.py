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
RANGGING
"""
debug = led_matrix_class("PORT2","INDEX1")
lk = ranging_sensor_class("PORT4", "INDEX1")
bk = ranging_sensor_class("PORT2", "INDEX3")
rk = ranging_sensor_class("PORT2", "INDEX2")
fk = ranging_sensor_class("PORT2", "INDEX1")