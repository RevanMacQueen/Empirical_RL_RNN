import gym
import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from envs.random_maze import RandomMaze

#env = gym.make('LunarLander-v2')
env = RandomMaze(5, 3, 8479, 'one_hot')
env.seed(0)

ob_dim = int(np.prod(env.observation_space.shape))

print('State shape: ', ob_dim)
print('Number of actions: ', env.action_space.n)

from dqn_agent import Agent

agent = Agent(state_size=ob_dim, action_size=env.action_space.n, seed=0)

# watch an untrained agent
# state = env.reset()
# for j in range(1000):
#     action = agent.act(state)
#     env.render()
#     state, reward, done, _ = env.step(action)
#     if done:
#         break 
        
# env.close()

# load the weights from file
# agent.qnetwork_local.load_state_dict(torch.load('checkpoint.pth'))

# for i in range(5):
#     state = env.reset()
#     for j in range(200):
#         action = agent.act(state)
#         env.render()
#         state, reward, done, _ = env.step(action)
#         if done:
#             break 
            
# env.close()

def dqn(n_episodes=1000, max_t=10000, eps_start=1.0, eps_end=0.01, eps_decay=0.995):
    """Deep Q-Learning.
    
    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    scores = []                        # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start                    # initialize epsilon
    for i_episode in range(1, n_episodes+1):
        state = env.reset()
        score = 0
        ep_len = 0
        for t in range(max_t):
            action = agent.act(state, eps)
            next_state, reward, done, _ = env.step(action)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            ep_len += 1
            #score += reward
            if done:
                score = ep_len
                break 
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score
        eps = max(eps_end, eps_decay*eps) # decrease epsilon
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), end="")
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
        # if np.mean(scores_window)>=200.0:
        #     print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode-100, np.mean(scores_window)))
        #     torch.save(agent.qnetwork_local.state_dict(), 'checkpoint.pth')
        #     break
    return scores

scores = dqn()

# plot the scores
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.arange(len(scores)), scores)
plt.ylabel('Score')
plt.xlabel('Episode #')
plt.show()