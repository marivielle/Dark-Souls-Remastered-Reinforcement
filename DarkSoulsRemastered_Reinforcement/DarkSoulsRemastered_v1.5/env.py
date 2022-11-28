#Mariana Capdevielle Schurmann - c1830536

'''Custom environment for Dark Souls: Remastered. Current version only allows for play against Sif'''

from gym import Env
from gym.spaces import Discrete, Box, Dict
from ReadWriteMemory import ReadWriteMemory
from moveset import take_action
from player_position import teleport, quit_and_reset_game, lock_on
import numpy as np
from pykeyboard import PyKeyboard, PyKeyboardEvent
import time


class DarkSoulsEnv(Env):
    def __init__(self):
        #actions we can take
        self.action_space = Discrete(10)
        self.observation_space = Box(low=np.array([0, 0, 0, 0, 0]), high=np.array([3432, 1486, 9999999999, 9999999999, 9999]))

        self.actions = {0: 'forward', 1: 'right', 2: 'left', 3: 'back', 4: 'use_item', 5: 'attack', 6: 'heavy_attack',
                        7: 'back_roll', 8: 'forward_roll', 9: 'left_roll', 10: 'right_roll'}

        self.max_run = 300
        self.ready = False
        done = False
        self.state, self.info = self.set_current_state()
        self.previous = {'Boss Health': 0, 'Player Health': 0, 'Location Difference': 0}

    def set_current_state(self):
        rwm = ReadWriteMemory()
        ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
        ds.open()
        php_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x3E8])
        bhp_pointer = ds.get_pointer(0x14383001B, offsets=[0x3E8])
        ploc_pointer = ds.get_pointer(0x141d151b0, offsets=[0x68, 0x18, 0x10])
        bloc_pointer = ds.get_pointer(0x14383001B, offsets=[0x18, 0x28, 0x50, 0x20, 0x30, 0x30])

        boss_hp = ds.read(bhp_pointer)
        player_hp = ds.read(php_pointer)
        player_loc = ds.read(ploc_pointer)
        boss_loc = ds.read(bloc_pointer)

        loc_dif = abs(ds.read(ploc_pointer) - ds.read(bloc_pointer))

        info = {'Boss Health': boss_hp, 'Player Health': player_hp,
                         'Player Location': player_loc, 'Boss Location': boss_loc,
                         'Location Difference': loc_dif}

        current_state = np.array([boss_hp, player_hp, player_loc,
                                 boss_loc, loc_dif])

        ds.close()

        return current_state, info

    def step(self, action):
        """
        Our step will be as follows:
            1. Check our and bosses health
            2. Apply our action
            -> Actions have times in consideration for animation
            3. Check our and our bosses health again
            4. Give rewards:
            -> If we lose health = -
            -> If we die = -

            -> if health neither goes up or down = 0

            -> if boss losses health = +

            !~If there was further access to animation, we would implement rewards based on if player
            dodged an attack~!

        :param action:
        :return state, reward, done, info:
        """
        reward = 0
        done = False

        #checking if previous animation os over

        take_action(self.actions[action])

        # read health after action
        self.state, self.info = self.set_current_state()

        #if self.previous['Player Health'] < self.info['Player Health']:
            #time.sleep(2)  # cannot make decisions while player animation for getting up is running

        #if not 0 <= self.info['Boss Health'] <= 3432:
        #    k = PyKeyboard()
        #    k.press_key('q')
        #    time.sleep(0.3)
        #    k.release_key('q')

        if self.info['Player Health'] <= 0.1 or self.info['Boss Health'] <= 0.1:
            done = True
            self.ready = False

        if self.info['Location Difference'] < self.previous['Location Difference']:
            reward += 0.09  #encourage decisions that lead to player being closer to the boss

        if self.previous['Player Health'] > self.info['Player Health']:
            #time.sleep(1.5) #cannot make decisions while player animation for getting up is running
            if self.info['Boss Health'] < self.previous['Boss Health']:
                reward -= 0.2
            else:
                reward -= 0.4

        if self.info['Boss Health'] < self.previous['Boss Health']:
            reward += 0.7  #prioritise boss losing health over us losing health

        if self.info['Player Health'] <= 0:
            reward -= 1

        if self.info['Boss Health'] <= 0:
            reward += 1

        self.max_run -= 1
        if self.max_run <= 0 and not done:
            done = True

        self.previous['Boss Health'] = self.info['Boss Health']
        self.previous['Player Health'] = self.info['Player Health']
        self.previous['Location Difference'] = self.info['Location Difference']

        return self.state, reward, done, self.info

    def reset(self, quit=False):
        """
        Resets setup:
            1. quit game back to start
            2. replace local save file with our save file
            3. continue game
            4. give a few seconds to load, then teleport
            5. lock onto enemy

            Assumes game is already running, and player is at bonfire.
            Also used to reset save file between episodes

            :param:
            :return:
        """

        if quit:
            locked_on = False
            while not locked_on:
                time.sleep(12)
                quit_and_reset_game()

                rwm = ReadWriteMemory()
                ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
                ds.open()

                teleport(ds)

                time.sleep(1)
                locked_on = lock_on(ds)
                ds.close()
                #print('passed')
                #if not locked_on:
                    #time.sleep(10)  #giving time for the player to respawn

        else:
            locked_on = False
            while not locked_on:
                time.sleep(10)
                rwm = ReadWriteMemory()
                ds = rwm.get_process_by_name("DarkSoulsRemastered.exe")
                ds.open()
                teleport(ds)
                time.sleep(1)
                locked_on = lock_on(ds)
                ds.close()
                #if not locked_on:
                #    time.sleep(10)  # giving time for the player to respawn

        self.state, info = self.set_current_state()
        self.previous['Boss Health'] = self.info['Boss Health']
        self.previous['Player Health'] = self.info['Player Health']
        self.previous['Location Difference'] = self.info['Location Difference']
        self.ready = True

        return self.state

    def render(self):
        """
        No rendering needed
        :return:
        """
        pass

    def close(self):
        """
        Will be used to close the game
        :return:
        """
        pass