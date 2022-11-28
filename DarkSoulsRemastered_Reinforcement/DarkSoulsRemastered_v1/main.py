
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
    replay_memory = 5000  # number of previous transitions to remember
    batch = 64  # size of minibatch
    plotting_data = []
    scores_data = []

    time.sleep(10)
    print('STARTING')
    time.sleep(1)

    env = DarkSoulsEnv()
    max_epochs = 500

    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = Agent(action_size, state_size, [24, 24])
    scores = {key: None for key in range(max_epochs)}
    yplot = []
    yplot2 = []

    for episode in range(max_epochs):
        if episode%10 == 0 or episode == 1:
            state = env.reset(True) #resets environment for each episode
        else:
            state = env.reset(False)
        state = np.reshape(state, [1, state_size])
        done = False #haven’t gone through all episodes yet
        score = 0 #overall score
        env.max_run = 300

        while not done: #while we haven’t finished this episode
            action = agent.act(state) #make decision based on state
            print(action)
            n_state, reward, done, info = env.step(action) #do the action

            score += reward  # add reward to score

            next_state = np.reshape(n_state, [1, state_size])  # reshape for agent
            agent.memorize(state, action, reward, next_state, done)  # agent memorises
            state = next_state  # calculate state for next decision

            if done:
                agent.update_target_model()
                scores[episode] = [episode, max_epochs, score, agent.epsilon]
                print('Episode:{}/{} Score:{}, e:{:.2}'.format(episode, max_epochs, score, agent.epsilon))
                print(info['Boss Health'])
                break

        if len(agent.memory) > batch:
            agent.replay(batch)

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


