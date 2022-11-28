#Mariana Capdevielle Schurmann - c1830536

"""Checks animation currently running"""

from ReadWriteMemory import ReadWriteMemory
import time


def check_death():
    rwm = ReadWriteMemory()
    ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
    ds.open()
    php_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])
    player_hp = ds.read(php_pointer)
    if player_hp < 0.01:
        return True
    else:
        return False


def check_animation():
    rwm = ReadWriteMemory()
    ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
    ds.open()
    current_animation_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x68, 0x48, 0x80])
    current_animation = ds.read(current_animation_pointer)
    #print(type(current_animation))
    check = 0
    dead = False

    while current_animation != 4294967295 and not dead:
        time.sleep(0.03)
        #print(current_animation)
        #print(check)
        #print(current_animation == 9294967295)
        #print()
        current_animation = ds.read(current_animation_pointer)
        dead = check_death()

    ds.close()