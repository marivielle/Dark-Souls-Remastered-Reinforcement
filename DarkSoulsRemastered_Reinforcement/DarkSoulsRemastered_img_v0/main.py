
#import cv2
#from grab_screen import grab_screen
from env import DarkSoulsEnv
from model import Agent
from store import store
import numpy as np
import time
import matplotlib.pyplot as plt


if __name__ == "__main__":
    game = "Dark Souls Remastered"  # the name of the game being played for log files
    num_actions = 10  #ATTACK number of valid actions
    replay_memory = 7000  # number of previous transitions to remember - WHY 5000
    batch = 70  # size of minibatch - WHY 64
    image_stack = 5

    plotting_data = [] #SETUP TO SAVE TRAINING DATA UWU
    scores_data = []
    yplot = []
    yplot2 = []

    time.sleep(1)
    print('STARTING')
    time.sleep(5)

    env = DarkSoulsEnv()
    max_epochs = 500

    state_size = env.observation_space.shape
    action_size = env.action_space.n
    agent = Agent(action_size, state_size, [40, 40]) #why 24??
    scores = {key: None for key in range(max_epochs)}

    for episode in range(max_epochs):
        if episode%5 == 0:
            state = env.reset(True) #resets environment for each episode — NEED TO SETUP USING ITEMS
        else:
            state = env.reset(False)
        #state = np.reshape(state, [ 1, state_size]) #needed to run - find out why for writeup
        done = False #haven’t gone through all episodes yet
        score = 0 #overall score uwu - DONT ADD IF WE LOSE SIF LOCK ON, ALSO ADD TO TXT FILE FOR TRAINING
        env.max_run = 400

        while not done: #while we haven’t finished this episode
            action = agent.act(state) #make decision based on state
            n_state, reward, done, info = env.step(action) #do the action - enable use of items

            score += reward  # add reward to score, maybe store separately in training file?? check reference

            #next_state = np.reshape(n_state, [1, state_size])  # reshape for agent - find out why
            agent.memorize(state, action, reward, n_state, done)  # agent memorises
            state = n_state  # calculate state for next decision

            if done:
                agent.update_target_model()
                scores[episode] = [episode, max_epochs, score, agent.epsilon]
                print('Episode:{}/{} Score:{}, e:{:.2}, Boss Health: {}/3432'.format(episode, max_epochs, score, agent.epsilon, info['Boss Health']))
                #print(info['Boss Health'])
                break

        if len(agent.memory) > batch:
            print()
            print("Learning...")
            agent.replay(batch) #learn uwu - find more description pls for writeup
            print("Done")
            print()

        yplot.append(info['Boss Health'])
        yplot2.append(agent.epsilon)
        plotting_data.append([info['Boss Health'], agent.epsilon])
        scores_data.append([info['Boss Health'], score])

    store("Boss_Epsilon.csv", plotting_data)
    store("Boss_Scores.csv", scores_data)
    agent.save('darksouls_run_0.h5')

    _yplot = np.array(yplot)
    _yplot2 = np.array(yplot2)
    figure, axis = plt.subplots(2)

    axis[0].plot(_yplot)
    axis[0].set_title("Boss Health throughout epochs")
    axis[0].set_xlabel("Epochs")
    axis[0].set_ylabel("Boss Health")

    axis[1].plot(_yplot2)
    axis[1].set_title("Epsilon throughout epochs")
    axis[1].set_xlabel("Epochs")
    axis[1].set_ylabel("Epsilon")

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