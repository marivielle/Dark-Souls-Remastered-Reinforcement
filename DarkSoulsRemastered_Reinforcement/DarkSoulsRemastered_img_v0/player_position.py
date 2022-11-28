# Mariana Capdevielle Schurmann - c1830536

"""Resets save file for fresh start and sets up correct location after death"""

from ReadWriteMemory import ReadWriteMemory
from pykeyboard import PyKeyboard, PyKeyboardEvent
import os
import time


def teleport(ds):
    k = PyKeyboard()

    camera_x = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0xE0])
    camera_z = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0xE4])
    camera_y = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0xE8])

    camera_pos_x = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0x100])
    camera_pos_z = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0x104])
    camera_pos_y = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0x108])

    camera_rot_x = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0x140])
    camera_target_rot_x = ds.get_pointer(0x141d151b0, offsets=[0x60, 0x60, 0x150])

    # player
    player_x = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x28, 0x50, 0x20, 0x120])
    player_z = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x28, 0x50, 0x20, 0x124])  # from pvp ai in github
    player_y = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x28, 0x50, 0x20, 0x128])

    php_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])

    player_pos_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x10])

    ds.write(player_x, 1133007089)
    ds.write(player_z, 3248018856)
    ds.write(player_y, 3280357093)

    ds.write(camera_x, 1133046977)
    ds.write(camera_z, 3247074059)
    ds.write(camera_y, 3280260962)
    ds.write(camera_pos_x, 1133056964)
    ds.write(camera_pos_z, 3247023915)
    ds.write(camera_pos_y, 3280236890)
    ds.write(camera_rot_x, 1039478796)
    ds.write(camera_target_rot_x, 1039478805)

    time.sleep(0.2)
    k.press_keys(['w', 'd'])  # should set player facing correct way
    k.press_key('w')
    time.sleep(0.1)
    k.release_key('w')
    ds.write(php_pointer, 1459)


def restore_save_file():
    #have to use /s instead of going directly to directory because DS leaves spaces on their folder names
    cmd = 'replace .\save_file\DRAKS0005.sl2 C:\\Users\\marvi\\OneDrive\\Documents\\NBGI /s'
    os.system(cmd)


def lock_on(ds):
    k = PyKeyboard()
    locked_on = False
    tries = 0

    while not locked_on:

        if tries == 5:
            return locked_on

        k.press_key('w')
        time.sleep(0.5)
        k.release_key('w')
        k.press_key('q')
        time.sleep(0.5)
        k.release_key('q')

        boss_hp_pointer = ds.get_pointer(0x14383001B, offsets=[0x3E8])
        php_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])

        boss_hp = ds.read(boss_hp_pointer)
        player_hp = ds.read(php_pointer)
        print({'Boss HP': boss_hp, 'HP': player_hp})

        #reading boss health
        if boss_hp == 3432:  #we know boss health is 3432
            #print({'Boss HP': boss_hp, 'HP': player_hp})
            locked_on = True
            k.tap_key('q')
            return locked_on

        if player_hp <= 0.1:
            return locked_on

        tries += 1


def boss_data(ds):
    hp = ds.get_pointer(0x14383001B, offsets=[0x3E8])
    types = ds.get_pointer(0x14383001B, offsets=[0xD4])
    player_hp = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])

    bhp = ds.read(hp)
    typess = ds.read(types)
    php = ds.read(player_hp)

    print({'HP': bhp, 'Player HP': php, 'BType': typess, })


def quit_and_reset_game():
    k = PyKeyboard()
    print('here')
    time.sleep(1)
    k.tap_key(k.escape_key)
    time.sleep(0.9)
    k.tap_key(k.left_key)
    time.sleep(1)
    #k.tap_key(k.right_key, n=3, interval=0.8)
    k.tap_key('e')
    time.sleep(1)
    k.tap_key(k.up_key)
    time.sleep(0.8)
    #k.tap_key(k.down_key, n=5, interval=0.8)
    k.tap_key('e')
    time.sleep(0.9)
    k.tap_key(k.left_key)
    time.sleep(0.7)
    k.tap_key('e')
    time.sleep(10)
    restore_save_file()
    time.sleep(3)
    k.tap_key('e')
    time.sleep(2)
    k.tap_key('e')
    time.sleep(1)
    k.tap_key('e')
    time.sleep(2)
    k.tap_key('e')
    time.sleep(1)
    k.tap_key('e')
    time.sleep(1)
    k.tap_key('e')
    time.sleep(5)


"""
    Starting the game
"""
"""
m = PyMouse()
k = PyKeyboard()

subprocess.call(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 570940")  #calls steam and plays game using desktop shortcut id

t.sleep(25)
#t.sleep(4)                                                                  #wait until the unskippable loading screen ends
#print("escape x 3")
#k.tap_key(k.escape_key,n=4,interval=2)                                     #skip brand screens
#t.sleep(3)
#print("e x 2")
k.tap_key('e', n=2, interval=3)                                         #press e twice to load and accept offline mode
t.sleep(2)
#print("Pressing down")
#k.tap_key(k.down_key,n=2,interval=1)                                               #go down to new game option
#print("e")
k.tap_key('e')                                                          #select new game
rwm = ReadWriteMemory()
ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
ds.open()
print("\nProcess info:\n", ds.__dict__)


k = PyKeyboard()
while True:
    keyboard_input = keyboard.read_key()
    #print(keyboard_input)
    if keyboard_input == 'z':
        quit_game()
        k.tap_key('e')
        time.sleep(1)
        k.tap_key('e')
        time.sleep(5)
        quit_game() #THIS WAS TO TEST THAT IT COULD QUIT/RELOAD MULTIPLE TIMES

    elif keyboard_input == 'o':

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\": #all possible characters
    keyList.append(char)

k.press_key('r')
print('pressing')


keys = []
print(keyList)
for key in keyList:
    if wapi.GetAsyncKeyState(ord(key)):  # checking which keys are pressed
        print(key)

        k.release_key('r')"""
