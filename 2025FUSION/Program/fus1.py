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
    "LF": encoder_motor_class("M6", "INDEX1"), #Left_Front wheel
    "LB": encoder_motor_class("M2", "INDEX1"), #Left_Back wheel
    "RF": encoder_motor_class("M1", "INDEX1"), #Right_Front wheel 
    "RB": encoder_motor_class("M5", "INDEX1"),  #Right_Back wheel
    "FEED": encoder_motor_class("M3", "INDEX1")
}

sv = {
    "shooter" : smartservo_class("M4","INDEX1")
}

debug = led_matrix_class("PORT5","INDEX1")
"""
SYSTEM
"""

def lift(a:int):
    power_expand_board.set_power("DC3",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",-10)

def gripper(a:int):
    power_expand_board.set_power("DC8",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC8",0)

def feed(a:int,b:int):
    power_expand_board.set_power("DC8",a)
    power_expand_board.set_power("DC2",-b)

def stop_all():
    power_expand_board.set_power("DC1",0)
    power_expand_board.set_power("DC2",0)
    power_expand_board.set_power("DC3",0)
    power_expand_board.set_power("DC4",0)
    power_expand_board.set_power("DC5",0)
    power_expand_board.set_power("DC6",0)
    power_expand_board.set_power("DC7",0)
    power_expand_board.set_power("DC8",0)
    en["FEED"].set_power(0)

def shoot(a:int,b:int,c:int):
    power_expand_board.set_power("DC8",a)
    power_expand_board.set_power("DC2",-b)
    en["FEED"].set_power(c)
    time.sleep(0.1)
    power_expand_board.set_power("DC8",0)
    power_expand_board.set_power("DC2",0)

def shooting(a:int):
    power_expand_board.set_power("BL1",a)
    power_expand_board.set_power("BL2",a)

def shooter_angle(a:int):
    sv["shooter"].move_to(a,50)

def red_servo():
    if sv["shooter"].get_value("current") > 1250:
        sv["shooter"].set_power(0)

def servo_move(angle):
    if sv["shooter"].get_value("angle") < 105:
        sv["shooter"].move(angle, 50)
    else:
        sv["shooter"].move_to(95, 50)

def laser(a:int):
    power_expand_board.set_power("DC7",a)


"""
CONTROLLER
"""
class movement:
    def control_movement_font():            
        rf = ((gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.7) #+ math.fabs((gamepad.get_joystick("Ly") * 0.1))
        lb = (((gamepad.get_joystick("Lx") * 0.8 ) - gamepad.get_joystick("Rx")) * 0.7) #- math.fabs((gamepad.get_joystick("Ly") * 0.1))
        lf = (gamepad.get_joystick("Ly") + -gamepad.get_joystick("Rx")) * 0.7 #- math.fabs((gamepad.get_joystick("Lx") * 0.05))
        rb = (gamepad.get_joystick("Ly") - -gamepad.get_joystick("Rx")) * 0.7 #+ math.fabs((gamepad.get_joystick("Lx") * 0.05))
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
        global open_feed
        movement.control_movement_font()
        if gamepad.is_key_pressed("N1"):
            feed(100,100)

        elif gamepad.is_key_pressed("L1"):
            stop_all()

        elif gamepad.is_key_pressed("L2"):
            shooter_angle(57)

        elif gamepad.is_key_pressed("L_Thumb"):
            shoot(0,0,-50)

        elif gamepad.is_key_pressed("N2"):
            shoot(70,70,70)

        elif gamepad.is_key_pressed("N3"):
            shoot(-50,-50,-50)
        
        elif gamepad.is_key_pressed("R1"):
            shooting(80)

        elif gamepad.is_key_pressed("R2"):
            shooting(0)

        elif gamepad.is_key_pressed("Up"):
            shooter_angle(25)

        elif gamepad.is_key_pressed("Down"):
            shooter_angle(86)
        
        elif gamepad.is_key_pressed("Right"):
            servo_move(-3)

        elif gamepad.is_key_pressed("Left"):
            servo_move(3)
        
        elif gamepad.is_key_pressed("N4"):
            shooting(60)

        elif gamepad.is_key_pressed("L2"):
            laser(50)

        else:
            en["FEED"].set_power(0)

    def mode2():
        movement.control_movement_right()
        if gamepad.is_key_pressed("Up"):
            lift(-100)

        elif gamepad.is_key_pressed("Down"):
            lift(100)

        elif gamepad.is_key_pressed("N4"):
            gripper(100)

        elif gamepad.is_key_pressed("N1"):
            gripper(-100)

        elif gamepad.is_key_pressed("N2"):
            power_expand_board.set_power("DC7",-100)
            power_expand_board.set_power("DC8",50)
            time.sleep(0.1)
            power_expand_board.set_power("DC7",-10)
            power_expand_board.set_power("DC8",50)

        elif gamepad.is_key_pressed("N3"):
            power_expand_board.set_power("DC7",100)
            power_expand_board.set_power("DC8",100)
            time.sleep(0.1)
            power_expand_board.set_power("DC7",-10)
            power_expand_board.set_power("DC8",100)

        elif gamepad.is_key_pressed("L1"):
            stop_all()

    def change_mode():
        if gamepad.is_key_pressed("+"):
            controller.mode = "1"
        elif gamepad.is_key_pressed("≡"):
            controller.mode = "2"

"""
MAIN
"""
while True:
    debug.show(sv["shooter"].get_value("angle"),wait = False)
    if power_manage_module.is_auto_mode():
        while not not power_manage_module.is_auto_mode():
            pass
    else:
        controller.change_mode()
        if controller.mode == "1":
            controller.mode1()
            red_servo()
        else:
            controller.mode2()
            red_servo()
