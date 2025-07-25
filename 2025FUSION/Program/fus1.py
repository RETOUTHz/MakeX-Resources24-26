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
    #Right()
    #Left()
    block_right()
"""
SYSTEM
"""

def lift(a:int):
    power_expand_board.set_power("DC1",-a)
    time.sleep(0.1)
    power_expand_board.set_power("DC1",15)

def gripper(a:int,b:int):
    power_expand_board.set_power("DC3",a)
    time.sleep(0.1)
    power_expand_board.set_power("DC3",b)

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

def move_around(a:int):
        en["RF"].set_speed(a)
        en["RB"].set_speed(a)
        en["LB"].set_speed(-a)
        en["LF"].set_speed(a)

def slide_left(a:int):
        en["RF"].set_speed(a)
        en["RB"].set_speed(0)
        en["LB"].set_speed(-a*1.3)
        en["LF"].set_speed(0)

def slide_right(a:int):
        en["RF"].set_speed(-a)
        en["RB"].set_speed(0)
        en["LB"].set_speed(a*1.6)
        en["LF"].set_speed(0)

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
        rf = ((gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.8) #+ math.fabs((gamepad.get_joystick("Ly") * 0.1))
        lb = (((gamepad.get_joystick("Lx") * 0.8 ) - gamepad.get_joystick("Rx")) * 0.8) #- math.fabs((gamepad.get_joystick("Ly") * 0.1))
        lf = (gamepad.get_joystick("Ly") + -gamepad.get_joystick("Rx")) * 0.85 #- math.fabs((gamepad.get_joystick("Lx") * 0.05))
        rb = (gamepad.get_joystick("Ly") - -gamepad.get_joystick("Rx")) * 0.85 #+ math.fabs((gamepad.get_joystick("Lx") * 0.05))
        # if math.fabs(gamepad.get_joystick("Rx")) > 10:
        #     power_expand_board.set_power("DC6", -gamepad.get_joystick("Rx") * 100)
        # else:
        #     power_expand_board.set_power("DC7", 0)
        en["RF"].set_power(-rf)
        en["RB"].set_power(-rb)
        en["LB"].set_power(lb)
        en["LF"].set_power(lf)
    
    def control_movement_right():
        rf = (gamepad.get_joystick("Ly") - gamepad.get_joystick("Rx")) * 0.8
        lb = (gamepad.get_joystick("Ly") + gamepad.get_joystick("Rx")) * 0.8
        lf = (-gamepad.get_joystick("Lx") + gamepad.get_joystick("Rx")) * 0.85
        rb = (-gamepad.get_joystick("Lx") - gamepad.get_joystick("Rx")) * 0.85
        # if math.fabs(gamepad.get_joystick("Rx")) > 10:
        #     power_expand_board.set_power("DC7", -gamepad.get_joystick("Rx") * 100)
        # else:
        #     power_expand_board.set_power("DC7", 0)
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
            box(100)

        elif gamepad.is_key_pressed("L1"):
            stop_all()

        elif gamepad.is_key_pressed("L2"):
            shooter_angle(62)
            shooting(90)

        elif gamepad.is_key_pressed("L_Thumb"):
            servo_move(5)

        elif gamepad.is_key_pressed("L_Thumb"):
            servo_move(-5)

        elif gamepad.is_key_pressed("N2"):
            shoot(90,90,90)
            box(-100)

        elif gamepad.is_key_pressed("N3"):
            shoot(-90,-90,-90)
        
        elif gamepad.is_key_pressed("R1"):
            shooting(85)

        elif gamepad.is_key_pressed("R2"):
            shooting(0)

        elif gamepad.is_key_pressed("Up"):
            shooter_angle(25)

        elif gamepad.is_key_pressed("Down"):
            shooter_angle(85)
        
        elif gamepad.is_key_pressed("Right"):
            shooter_angle(80)

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
            lift(50)

        elif gamepad.is_key_pressed("N4"):
            gripper(-100,-100)

        elif gamepad.is_key_pressed("N1"):
            gripper(100,100)

        elif gamepad.is_key_pressed("Left"):
            gripper(100,100)

        elif gamepad.is_key_pressed("Right"):
            gripper(-100,-100)

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
        
        elif gamepad.is_key_pressed("R2"):
            box(-100)

    def change_mode():
        if gamepad.is_key_pressed("+"):
            controller.mode = "1"
        elif gamepad.is_key_pressed("≡"):
            controller.mode = "2"
"""
AUTO
"""
def Right():
    power_expand_board.set_power("DC1",100)
    time.sleep(1.05)
    power_expand_board.set_power("DC1",10) #lift up phase 1
    slide_right(200)
    time.sleep(1)
    stop_moving() #set 0 phase 1
    while lk.get_distance() <= 130:
        debug.show(lk.get_distance(), wait=False)
        slide_left(200)
    stop_moving()
    move_around(100)
    time.sleep(0.5)
    stop_moving()
    move_backward(75)
    time.sleep(2.5)
    stop_moving() # set 0 phase 1
    move_forward(75)
    time.sleep(0.2)
    stop_moving() # set 0 phase 1
    while lk.get_distance() <= 175:
        debug.show(lk.get_distance(), wait=False)
        slide_left(100)
    stop_moving()
    time.sleep(1)
    power_expand_board.set_power("DC3",-100)
    slide_right(200)
    time.sleep(1)
    stop_moving()
    power_expand_board.set_power("DC3",100)
    time.sleep(1)
    power_expand_board.set_power("DC3",0) # gripper phsae 1
    move_around(100)
    time.sleep(0.2)
    stop_moving()
    move_backward(100)
    time.sleep(1)
    stop_moving() 
    move_forward(75)
    time.sleep(1.4)
    stop_moving() #set 0 phase 2
    while lk.get_distance() <= 175:
        debug.show(lk.get_distance(), wait=False)
        slide_left(75)
    stop_moving()
    time.sleep(1)
    power_expand_board.set_power("DC3",-100)
    slide_right(200)
    time.sleep(1)
    stop_moving()
    power_expand_board.set_power("DC3",100)
    time.sleep(1)
    power_expand_board.set_power("DC3",0) # gripper phase 2

def Left():
    power_expand_board.set_power("DC1",100)
    time.sleep(1.1)
    power_expand_board.set_power("DC1",10) #lift up phase 1
    move_backward(100)
    time.sleep(0.5)
    stop_moving()
    slide_right(200)
    time.sleep(1)
    stop_moving() #set 0 phase 1
    while lk.get_distance() <= 135:
        debug.show(lk.get_distance(), wait=False)
        slide_left(200)
    stop_moving()
    move_forward(75)
    time.sleep(2)
    stop_moving() # set 0 phase 1
    while lk.get_distance() <= 175:
        debug.show(lk.get_distance(), wait=False)
        slide_left(100)
    stop_moving()
    time.sleep(1)
    power_expand_board.set_power("DC3",-100)
    slide_right(200)
    time.sleep(1)
    stop_moving()
    power_expand_board.set_power("DC3",100)
    time.sleep(1)
    power_expand_board.set_power("DC3",0) # gripper phsae 1
    move_backward(100)
    time.sleep(1)
    stop_moving() #set 0 phase 2
    move_forward(75)
    time.sleep(1.5)
    stop_moving() 
    while lk.get_distance() <= 175:
        debug.show(lk.get_distance(), wait=False)
        slide_left(100)
    stop_moving()
    time.sleep(1)
    power_expand_board.set_power("DC3",-100)
    slide_right(200)
    time.sleep(1)
    stop_moving()
    power_expand_board.set_power("DC3",100)
    time.sleep(1)
    power_expand_board.set_power("DC3",0) # gripper phase 2

def block_right():
    box(100)
    slide_right(100)
    time.sleep(0.2)
    stop_moving()
    while bk.get_distance() <= 173:
        debug.show(lk.get_distance(), wait=False)
        move_forward(300)
    stop_moving()
    slide_right(150)
    time.sleep(2)
    stop_moving() 
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
        controller.change_mode()
        if controller.mode == "1":
            debug.show(sv["shooter"].get_value("angle"),wait = False)
            controller.mode1()
            red_servo()
            
        else:
            debug.show_image("ffffffffffffffffffffffffffffffff")
            controller.mode2()
            red_servo()