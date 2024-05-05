import sys
import numpy as np
import math
import random
import gym
import gym_game
import pickle
import time
import math

def actioner(state, epsilon, d, q_table):
    up, reward, terminated, truncated, _ = env.step(0)
    down, reward, terminated, truncated, _ = env.step(1)
    left, reward, terminated, truncated, _ = env.step(2)
    right, reward, terminated, truncated, _ = env.step(3)
    rerun = []
    if up == state:
        q_table[(tuplify(state), 0)] = 0
    else:
        rerun.append(0)
    if down == state:
        q_table[(tuplify(state), 1)] = 0
    else:
        rerun.append(1)
    if left == state:
        q_table[(tuplify(state), 2)] = 0
    else:
        rerun.append(2)
    if right == state:
        q_table[(tuplify(state), 3)] = 0
    else:
        rerun.append(3)
    t = len(rerun)
    if d<epsilon:
        return random.randint(0, (t-1))
    else:
        best_action = None
        best_q_value = float('-inf')  # Initialize with negative infinity
        # Iterate over possible actions
        for a in range(t):
            q_value = q_table.get((tuplify(state), rerun[a]), 0.0)  # Get Q-value for the current state-action pair
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = rerun[a]
        # Assign the best action
        action = best_action
        return action
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

def simulate(q_table,w):
    for episode in range(MAX_EPISODES):
        # Init environment
        state = env.reset()
        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):
            # In the beginning, do random action to learn
            d = random.uniform(0, 1)
            #Pick action
            action = actioner(state, epsilon, d, q_table)
            next_state, reward, terminated, truncated, _ = env.step(action)
            # Do action and get result
            done = terminated or truncated
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
                max_block = 0
                for row in state:
                    for cell in row:
                        if cell > max_block:
                            max_block = cell
                if max_block == 2048:
                    b = 1
                else:
                    b=0
                w.append([b,max_block])
                #print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

        # exploring rate decay
    return w, q_table

def validation(q_table,w,epsilon,max_try,max_episodes):
    if epsilon ==1:
        for j in range(max_episodes):
            state = env.reset()
            for i in range(max_try):
                action = env.action_space.sample()
                next_state, reward, terminated, truncated, _ = env.step(action)
                if (next_state == state):
                    action = env.action_space.sample()
                    next_state, reward, terminated, truncated, _ = env.step(action)
                state = next_state
                env.render()
                done = terminated or truncated
                if done or i >= max_try - 1:
                    max_block = 0
                    total_sum = 0
                    for row in state:
                        for cell in row:
                            total_sum += cell
                            if cell > max_block:
                                max_block = cell
                    if max_block == 2048:
                        t = 1
                    else:
                        t = 0
                    r = 9*max_block+total_sum
                    w.append([t, max_block,r])
                # print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                    break
    elif epsilon ==0:
        for j in range(max_episodes):
            state = env.reset()
            for i in range(max_try):
                action = actioner(state,epsilon,1,q_table)
                next_state, reward, terminated, truncated, _ = env.step(action)
                state = next_state
                env.render()
                done = terminated or truncated
                if done or i >= max_try - 1:
                    max_block = 0
                    total_sum = 0
                    for row in state:
                        for cell in row:
                            total_sum += cell
                            if cell > max_block:
                                max_block = cell
                    if max_block == 2048:
                        t = 1
                    else:
                        t = 0
                    r = 9 * max_block + total_sum
                    w.append([t, max_block, r])
                    break
                #print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                #save_q_table(q_table, 'q_table.pkl')
    else:
        print("Babushka")
    return w

if __name__ == "__main__":
    env = gym.make("Pygame-v0")
    MAX_EPISODES = 1000
    gamma = 0.6
    num_actions = 4  # Number of actions
    observation_space_length = 16
    MAX_TRY = 10000
    learning_rate = 0.5
    epsilon_decay = 1
    epsilon = 1
    w = []
    q_table = reader("q_table3.txt")
    for i in range(5):
        start = time.time()
        w, q_table = simulate(q_table,w)
        end = time.time()
        print("time" + str(end - start))
        epsilon *= .9623
    ## testing our bots (learner) vs a random bot (randomer) - looking at number of wins, max block, and reward
    learns = []
    writer("q_table3.txt", q_table)
    #randoms = []
    learnsst = time.time()
    learner = validation(q_table,learns,0,1000,50000)
    learnsend = time.time()
    with open("learnertrend.txt", "w") as txt_file:
        for line in w:
            txt_file.write(str(line) + "\n")
    print("times learner:" + str(-learnsst+learnsend))
    with open("learns.txt", "w") as txt_file:
        for line in learner:
            txt_file.write(str(line) + "\n")
    #random bot is already done
    #randomer = validation(q_table,randoms,1,100000,50000)
    #randomend = time.time()
    #print("times randomer:" + str(randomend-randomst))
    #randomst = time.time()
def mean(w,q):
    count = 0
    sum = 0
    for i in range(len(w)):
        count+=1
        sum+=w[i][q]
    average  = sum/count
    return average
def stdev(w,q):
    average = mean(w,q)
    count = 0
    sum = 0
    for i in range(len(w)):
        count+=1
        sum+=(w[i][q]-average)*(w[i][q]-average)
    standarddeviation  = math.sqrt(sum/(count-1))
    return standarddeviation
def x(r):
    w = []
    for i in range(r):
        w.append(i)
    return w


#def valider(w):
#    a = []
#    b = []
#    c = []
#    count = 0
#    for i in range(len(w)):
#        if i == 0:
#            return 1
#        else:
#            count+=1
#    return 0




