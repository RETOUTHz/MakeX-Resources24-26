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
    "RB": encoder_motor_class("M4", "INDEX1"),  #Right_Back wheel
    "FEED": encoder_motor_class("M3", "INDEX1")
}

sv = {
    "shooter" : smartservo_class("M4","INDEX1")
}

debug = led_matrix_class("PORT5","INDEX1")
bk = ranging_sensor_class("PORT5", "INDEX2")
lk = ranging_sensor_class("PORT5", "INDEX1")
"""
AUTO SECLET
"""
def select():
    if lk.get_distance() > 100:
        block_right()
    else:
        block_left()
"""
SYSTEM
"""

def lift(a:int):
    power_expand_board.set_power("DC1",-a)
    time.sleep(0.1)
    power_expand_board.set_power("DC1",15)

def gripper(a:int):
    power_expand_board.set_power("DC3",a)

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
        sv["shooter"].move_to(angle, 50)

def move_forward(a:int):
        en["RF"].set_speed(0)
        en["RB"].set_speed(-a)
        en["LB"].set_speed(0)
        en["LF"].set_speed(a)

def move_backward(a:int):
        en["RF"].set_speed(0)
        en["RB"].set_speed(a)
        en["LB"].set_speed(0)
        en["LF"].set_speed(-a)

def turn_right(a:int):
        en["RF"].set_speed(a)
        en["RB"].set_speed(a)
        en["LB"].set_speed(-a)
        en["LF"].set_speed(a)

def turn_left(a:int):
        en["RF"].set_speed(-a)
        en["RB"].set_speed(-a)
        en["LB"].set_speed(a)
        en["LF"].set_speed(-a)

def slide_right(a:int):
        en["RF"].set_speed(a)
        en["RB"].set_speed(0)
        en["LB"].set_speed(-a*1.3)
        en["LF"].set_speed(0)

def slide_left(a:int):
        en["RF"].set_speed(-a)
        en["RB"].set_speed(-a*0.4)
        en["LB"].set_speed(a*1.6)
        en["LF"].set_speed(a*0.2)

def stop_moving():
        en["RF"].set_speed(0)
        en["RB"].set_speed(0)
        en["LB"].set_speed(0)
        en["LF"].set_speed(0)

def box(a:int):
    power_expand_board.set_power("DC6",a)

"""
CONTROLLER
"""
class movement:
    def control_movement_font():            
        rf = ((gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")*0.9) * 0.8)
        lb = (((gamepad.get_joystick("Lx") * 0.8 ) - gamepad.get_joystick("Rx")*0.9) * 0.8)
        lf = ((gamepad.get_joystick("Ly") + -gamepad.get_joystick("Rx")*0.9) * 0.85 )
        rb = ((gamepad.get_joystick("Ly") - -gamepad.get_joystick("Rx")*0.9) * 0.85 )
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)
    
    def control_movement_right():
        rf = (gamepad.get_joystick("Ly") - gamepad.get_joystick("Rx")) * 0.8
        lb = (gamepad.get_joystick("Ly") + gamepad.get_joystick("Rx")) * 0.8
        lf = (-gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.85
        rb = (-gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx")) * 0.85
        en["RF"].set_power(rf)
        en["RB"].set_power(rb)
        en["LB"].set_power(-lb)
        en["LF"].set_power(-lf)

class blinking:
    blink = False
    def control_blink():
        if novapi.timer() > 0.75:
            blinking.blink = not blinking.blink
            novapi.reset_timer()

    def do_blinking():
        if blinking.blink:
            debug.show_image("00003c7e7e3c000000003c7e7e3c0000")
        else:
            debug.show_image("00103030303010000010303030301000")

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
            box(100)

        elif gamepad.is_key_pressed("L1"):
            stop_all()

        elif gamepad.is_key_pressed("L2"):
            shooter_angle(73)
            shooting(85)

        elif gamepad.is_key_pressed("L_Thumb"):
            shooter_angle(70)

        elif gamepad.is_key_pressed("R_Thumb"):
            shooter_angle(70)

        elif gamepad.is_key_pressed("N2"):
            shoot(90,90,90)
            box(-100)

        elif gamepad.is_key_pressed("N3"):
            shoot(-90,-90,-90)
        
        elif gamepad.is_key_pressed("R1"):
            shooting(80)

        elif gamepad.is_key_pressed("R2"):
            shooting(0)

        elif gamepad.is_key_pressed("Up"):
            shooter_angle(30)

        elif gamepad.is_key_pressed("Down"):
            shooter_angle(83)
        
        elif gamepad.is_key_pressed("Right"):
            shooter_angle(81)

        elif gamepad.is_key_pressed("Left"):
            shooter_angle(93)
        
        elif gamepad.is_key_pressed("N4"):
            shooting(45)

        else:
            en["FEED"].set_power(0)

    def mode2():
        movement.control_movement_right()
        if gamepad.is_key_pressed("Up"):
            lift(-100)

        elif gamepad.is_key_pressed("Down"):
            lift(100)

        elif gamepad.is_key_pressed("N4"):
            gripper(-100)

        elif gamepad.is_key_pressed("N1"):
            gripper(100)

        elif gamepad.is_key_pressed("Left"):
            gripper(100)

        elif gamepad.is_key_pressed("Right"):
            gripper(-100)

        elif gamepad.is_key_pressed("L1"):
            stop_all()
        
        elif gamepad.is_key_pressed("R2"):
            power_expand_board.set_power("DC3",0)

        elif gamepad.is_key_pressed("N2"):
            lift(-100)

        elif gamepad.is_key_pressed("N3"):
            lift(50)

        elif gamepad.is_key_pressed("L2"):
            box(100)
        
        elif gamepad.is_key_pressed("R1"):
            shooting(0)

    def change_mode():
        if gamepad.is_key_pressed("+"):
            controller.mode = "1"
        elif gamepad.is_key_pressed("≡"):
            controller.mode = "2"
"""
AUTO
"""
def block_right():
    turn_left(40)
    time.sleep(0.1)
    stop_moving()
    while bk.get_distance() <= 170:
        box(100)
        debug.show(bk.get_distance(), wait=False)
        move_forward(500)
    stop_moving()
    time.sleep(0.5)
    slide_left(150)
    time.sleep(2)
    stop_moving()
    turn_left(-100)
    time.sleep(0.5)
    stop_moving()
    turn_right(100)
    time.sleep(0.5)
    stop_moving()
    time.sleep(5)
    stop_all() 

def block_left():
    turn_right(40)
    time.sleep(0.1)
    stop_moving()
    while bk.get_distance() <= 156:
        box(100)
        debug.show(bk.get_distance(), wait=False)
        move_forward(500)
    stop_moving()
    slide_right(100)
    time.sleep(0.7)
    box(100)
    time.sleep(0.5)
    stop_moving()
    turn_right(50)
    time.sleep(0.2)
    stop_moving()
    move_forward(60)
    time.sleep(0.2)
    stop_moving()
    slide_left(100)
    time.sleep(1)
    stop_moving()
    turn_left(100)
    time.sleep(1)
    stop_moving()
    move_forward(255)
    time.sleep(1)
    stop_moving()
    time.sleep(5)
    stop_all()
"""
MAIN
"""
while True:
    #debug.show_image("ff828c8c80ff008383ff00ffc90101ff")
    if power_manage_module.is_auto_mode():
        select()
        while not not power_manage_module.is_auto_mode():
            pass
    else:
        blinking.control_blink()
        controller.change_mode()
        if controller.mode == "1":
            debug.show(sv["shooter"].get_value("angle"),wait = False)
            controller.mode1()
            red_servo()
            
        else:
            blinking.do_blinking()
            controller.mode2()

            red_servo()
