
#import cv2
import win32api as wapi  #CHECK TO SEE IF THIS SHIT WORKS WITH PYKEYBOARD OR KEYBOARD
#from win32api import GetSystemMetrics
#from grab_screen import grab_screen

from env import DarkSoulsEnv
from model import Agent
import numpy as np
import time
import matplotlib.pyplot as plt

if __name__ == "__main__":
    game = "Dark Souls Remastered"  # the name of the game being played for log files
    num_actions = 10  #ATTACK number of valid actions
    Max_Epoch = 500  # timesteps to observe before training
    replay_memory = 5000  # number of previous transitions to remember
    batch = 64  # size of minibatch
    #training_data = []

    env = DarkSoulsEnv()
    max_epochs = 500

    time.sleep(5)
    print('STARTING')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = Agent(action_size, state_size, [24, 24])
    scores = {key: None for key in range(max_epochs)}
    yplot = []
    yplot2 = []

    for episode in range(max_epochs):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        done = False
        score = 0

        while not done:
            action = agent.act(state)
            #print(action)
            n_state, reward, done, info = env.step(action)
            score += reward

            next_state = np.reshape(n_state, [1, state_size])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state

            if done:
                agent.update_target_model()
                scores[episode] = [episode, max_epochs, score, agent.epsilon]
                print('Episode:{}/{} Score:{}, e:{:.2}'.format(episode,max_epochs, score, agent.epsilon))
                break
            if len(agent.memory) > batch:
                agent.replay(batch)

            yplot.append(info['Boss Health'])
            yplot2.append(agent.epsilon)

    _yplot = np.array(yplot)
    _yplot2 = np.array(yplot2)
    figure, axis = plt.subplots(1, 2)

    axis[0, 0].plot(_yplot)
    axis[0, 0].set_title("Boss Health throughout epochs")
    axis[0, 0].xlabel("Epochs")
    axis[0, 0].ylabel("Boss Health")

    axis[0, 1].plot(_yplot2)
    axis[0, 1].set_title("Epsilon throughout epochs")
    axis[0, 1].xlabel("Epochs")
    axis[0, 1].ylabel("Epsilon")

    plt.show()




'''
def main(file_name, starting_value):
    training_data = []  #we start with nothing obvs

    print('STARTING!!!')

    while True:

        screen = grab_screen(region = (0, 40, 1920, 1120))  #grab the screen -> use mss
        # resize to something a bit more acceptable for a CNN
        screen = cv2.resize(screen, (480, 270))
        # run a color convert:
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  #-------------------why color convert?!?!!!!!!!!! find out
        keys = key_check()  #checking if any keys are pressed, return is list of any keys pressed
        output = keys_to_output(keys)  #maps from letters to the array representation up top
        training_data.append([screen, output])  #our training data -> what the screen says and what the model does woo

        #   we want to store this trainind data dont be a fucking weeb

        if len(training_data) % 100 == 0:  #if training data full?
            print(len(training_data))  #print length idk
            if len(training_data) == 100:
                np.save(file_name, training_data)  #save np training file
                print('SAVED')
                training_data = []  #start from 0
                starting_value += 1  #episode number me guess
              file_name = 'D:/dis/dis env/DATA/t_data_{0}.npy'.format(starting_value)

        keys = key_check()
        if 'v' in keys:
            if paused:
                paused = False
                print('Unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)'''


#print("Width =", GetSystemMetrics(0))
#print("Height =", GetSystemMetrics(1))
#win32gui.EnumWindows(process_location, None)