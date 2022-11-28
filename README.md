# AI for Video Games: How Different Inputs Affect Dark Souls AI Performance in Custom Environment

Dissertation project built to compare observation spaces and state data types (backend numerical data vs image captures) using a custom built environment in Dark Souls: Remastered. Although already handed in, this is an ongoing project. 

The aim of this project is to implement a custom environment and reinforcement learning model to determine the best observation space and state data type for the game Dark Souls: Remastered. The model will attempt to defeat an enemy with either discrete value or image inputs, in a custom OpenAI Gym environment. Each evolution of the model should have minimal changes to accommodate different inputs as to ensure fair comparisons of the data, with live information collected from the game process to be used as the inputs. 


## Installation

Cheat Engine needed to access backend information, as well as the appropriate table (https://fearlessrevolution.com/viewtopic.php?t=8422).

## Dependencies
Tensorflow
OpenAI Gym
ReadWriteMemory
Numpy
OpenCV (Image input)

Game and Cheat Engine must be left open and running while model runs.


## Future work

Currently testing RLib to apply a hybrid observation space of both image and backend input.
Further development on environment needed, current challenge is identifying when animation is done and next move can be performed. Currently using timings which can be innacurate if there's any lag as this version (Steam) of Dark Souls does not allow cheat engine to access all information needed.
