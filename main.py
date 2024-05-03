import sys
import numpy as np
import math
import random
import gym
import gym_game
import pickle
import time

def save_q_table(q_table, filename):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)

def load_q_table(filename):
    with open(filename, "rb") as f:
        q_table = pickle.load(f)
    return q_table
def reader(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    q_table = {}
    # iterate through each line and split key-value pairs
    for line in lines:
        key, value = line.strip().split(':')
        q_table[key.strip()] = value.strip()
    return q_table

def writer(filename,q_table):
    with open(filename, 'w') as f:
        for key, value in q_table.items():
            f.write('%s:%s\n' % (key, value))
def tuplify(w):
    a = tuple(w[0])
    b = tuple(w[1])
    c = tuple(w[2])
    d = tuple(w[3])
    f = (a,b,c,d)
    return f

def simulate(q_table):
    global epsilon, epsilon_decay
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
                next_state, reward, terminated, truncated, _ = env.step(action)
                if(next_state == state):
                    action = env.action_space.sample()
                    next_state, reward, terminated, truncated, _ = env.step(action)
            else:
                # Initialize action with a default value
                best_action = None
                best_q_value = float('-inf')  # Initialize with negative infinity

                # Iterate over possible actions
                for a in range(env.action_space.n):
                    q_value = q_table.get((tuplify(state), a), 0.0)  # Get Q-value for the current state-action pair
                    if q_value > best_q_value:
                        best_q_value = q_value
                        best_action = a

                # Assign the best action
                action = best_action

            # Do action and get result
            done = terminated or truncated
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table.get((tuplify(state), action), 0.0)
            # print("newstate: ", next_state)
            #print("q_value: ", q_table.get((tuplify(state), action), 0.0))
            best_q = max(q_table.get((tuplify(next_state), a), 0.0) for a in range(env.action_space.n))

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[(tuplify(state), action)] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                #print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                #save_q_table(q_table, 'q_table.pkl')
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay
    return q_table

if __name__ == "__main__":
    env = gym.make("Pygame-v0")
    MAX_EPISODES = 100000
    MAX_TRY = 100000
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    num_actions = 4  # Number of actions
    observation_space_length = 16
    # q_table = np.zeros((observation_space_length, num_actions))
    # q_table = load_q_table("q_table.pkl")
    q_table = reader('q_table5.txt')
    start = time.time()
    simulate(q_table)
    end = time.time()
    print("time"+str(end-start))
    writer("q_table5.txt",q_table)