#Mariana Capdevielle Schurmann - c1830536

from pymouse import PyMouse
from pykeyboard import PyKeyboard, PyKeyboardEvent
from animation import check_animation
import time

"""Stores and does all moves the AI has access to"""

m = PyMouse()
k = PyKeyboard()


def take_action(action):
    if action == 'forward':
        forward()
        check_animation()
    #check if animation is over, once it is continue

    elif action == 'right':
        right()
        #time.sleep(0.6)
        check_animation()

    elif action == 'left':
        left()
        #time.sleep(0.6)
        check_animation()

    elif action == 'back':
        back()
        #time.sleep(0.6)
        check_animation()

    elif action == 'attack':
        attack()
        #time.sleep(1.2)
        check_animation()

    elif action == 'back_roll':
        back_roll()
        #time.sleep(1.3)
        check_animation()

    elif action == 'forward_roll':
        forward_roll()
        #time.sleep(1.3)
        check_animation()

    elif action == 'left_roll':
        left_roll()
        #time.sleep(1.3)
        check_animation()

    elif action == 'right_roll':
        right_roll()
        #time.sleep(1.3)
        check_animation()

    elif action == 'use_item':
        use_item()
        #time.sleep(1.3)
        check_animation()

    elif action == 'heavy_attack':
        heavy_attack()
        #time.sleep(1.4)
        check_animation()


def use_item():
    k.press_key('h')
    time.sleep(0.3)
    k.release_key('h')


def right_roll():
    k.press_key('d')
    k.tap_key(k.space_key)
    time.sleep(0.3)
    k.release_key('d')


def forward_roll():
    k.press_key('w')
    k.tap_key(k.space_key)
    k.release_key('w')


def left_roll():
    k.press_key('a')
    k.tap_key(k.space_key)
    k.release_key('a')


def back_roll():
    k.press_key('d')
    k.tap_key(k.space_key)
    k.release_key('d')


def forward():
    k.press_key('w')
    time.sleep(0.5)
    k.release_key('w')


def right():
    k.press_key('d')
    time.sleep(0.5)
    k.release_key('d')


def left():
    k.press_key('a')
    time.sleep(0.5)
    k.release_key('a')


def back():
    k.press_key('s')
    time.sleep(0.5)
    k.release_key('s')


def lock():
    k.tap_key('q')  #will probably not need any longer -> setting it up in the env_setup


def attack():
    k.press_key('i')
    time.sleep(0.3)
    k.release_key('i')


def heavy_attack():
    k.press_key(k.shift_key)
    k.press_key('i')
    time.sleep(0.2)
    k.release_key('i')
    k.release_key(k.shift_key)
