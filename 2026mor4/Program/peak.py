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

# -----------------------------
# MOTOR
# -----------------------------

en = {
    "LF": encoder_motor_class("M1", "INDEX1"),
    "LB": encoder_motor_class("M3", "INDEX1"),
    "RF": encoder_motor_class("M2", "INDEX1"),
    "RB": encoder_motor_class("M4", "INDEX1")
}

sv = {
    "shooter": smartservo_class("M6", "INDEX1"),
    "left": smartservo_class("M2", "INDEX1")
}

mode = "1"

# -----------------------------
# FUNCTIONS
# -----------------------------

def feed(a, b, c):
    power_expand_board.set_power("DC2", a)
    power_expand_board.set_power("DC1", b)
    power_expand_board.set_power("DC3", c)


def stop_feed():
    feed(0, 0, 0)


def lift(power):
    power_expand_board.set_power("DC4", power)


def gripper(power):
    power_expand_board.set_power("DC8", power)


def brushless(power):
    power_expand_board.set_power("BL1", power)
    power_expand_board.set_power("BL2", power)


def servo_move(angle):
    sv["shooter"].move_to(angle, 50)


def red_servo():
    if sv["shooter"].get_value("current") > 1250:
        sv["shooter"].set_power(0)


# -----------------------------
# DRIVE
# -----------------------------

def control_movement():

    x = gamepad.get_joystick("Lx") * 0.7
    y = gamepad.get_joystick("Ly") * 0.7
    r = -gamepad.get_joystick("Rx") * 0.9

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


# -----------------------------
# MODE 1
# -----------------------------

def controller_1():

    # Feed
    if gamepad.is_key_pressed("N1"):
        feed(100, 100, 100)

    elif gamepad.is_key_pressed("N2"):
        feed(100, 100, 100)

    elif gamepad.is_key_pressed("N3"):
        feed(-100, -100, -100)

    else:
        stop_feed()

    # Shooter Servo
    if gamepad.is_key_pressed("Up"):
        servo_move(10)

    # Left Servo
    if gamepad.is_key_pressed("Down"):
        sv["left"].set_power(-100)
    else:
        sv["left"].set_power(0)


# -----------------------------
# MODE 2
# -----------------------------

def controller_2():

    # Lift
    if gamepad.is_key_pressed("Up"):
        lift(100)

    elif gamepad.is_key_pressed("Down"):
        lift(-100)

    else:
        lift(0)

    # Gripper
    if gamepad.is_key_pressed("N1"):
        gripper(100)

    elif gamepad.is_key_pressed("N2"):
        gripper(-100)

    else:
        gripper(0)


# -----------------------------
# CHANGE MODE
# -----------------------------

def change_mode():
    global mode

    if gamepad.is_key_pressed("+"):
        mode = "1"

    elif gamepad.is_key_pressed("≡"):
        mode = "2"


# -----------------------------
# MAIN
# -----------------------------

while True:

    if power_manage_module.is_auto_mode():

        while power_manage_module.is_auto_mode():
            pass

    else:

        change_mode()
        if mode == "1":
            controller_1()
            control_movement()
        else:
            controller_2()
            control_movement()