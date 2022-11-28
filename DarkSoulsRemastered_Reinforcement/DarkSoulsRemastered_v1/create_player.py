#Mariana Capdevielle Schurmann - c1830536

"""Creates and equips build on player character - just loads previously created save file"""

from ReadWriteMemory import ReadWriteMemory


def player_pointers(ds):

    #player pointers????
    player_x = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x28, 0x50, 0x20, 0x120])
    player_y = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x28, 0x50, 0x20, 0x124]) #from pvp ai in github
    player_hp = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])
    player_animation = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x68, 0x48, 0x80])
    player_stamina = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3F8])

    x = ds.read(player_x)
    y = ds.read(player_y)
    hp = ds.read(player_hp)
    animation = ds.read(player_animation)
    stamina = ds.read(player_stamina)

    return ds


rwm = ReadWriteMemory()
ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
ds.open()
print("\nProcess info:\n", ds.__dict__)

'''
what we need:
player stats - to set them up
player weapon
player animations
enemy animations (maybe??? - could just parse move names and see)
player items - healing and mana potions etc
moveset (attack, block, etc)
'''


