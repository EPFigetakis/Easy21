#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:58:06 2022

@author: peter.figetakis
"""

import pygame 
import random 
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np 
from copy import deepcopy


pygame.init()


RED = (255,0,0)
BLACK = (0,0,0)
WHITEBG = (255,255,255)
playerscore = 0
color = 0
dealerscore = 0
dcolor = 0
dealerscorelist = []
dealercolor = []
playerscorelist = []
playercolor = []
playercardCount = 0
dcardcount = 1
playerX = 370
playerY = 480
dealerX = 370
dealerY = 480 - 150
endsim = 0


#####GAME######
def randint(min=1,max=10):
    a = random.randint(min, max)
    return a


def randcolor(min=0,max=2):
    a = random.randint(min,max)
    if a == 0 or a == 1 :
        color = BLACK
        colorstring = 'B'
    else:
        color = RED
        colorstring = 'R'
    return color,colorstring

def generatePlayerCard(x):
    c = len(x)
    if c <= 1:
        color = BLACK
        colorstring = 'B'
    else:
        color,colorstring = randcolor()
    value = randint()
    return value, colorstring

def generateDealerCard(x):
    c = len(x)
    if c <= 1:
        color = BLACK
        colorstring = 'B'
    else:
        color,colorstring = randcolor()
    value = randint()
    return value, colorstring

def dealerplay():
    x1 =  checkScore(dealerscorelist, dealercolor)
    play = True
    while play:
        x1 =  checkScore(dealerscorelist, dealercolor)
        if x1 >= 17:
            play = False
        else:
            dealerscore, dcolor = generateDealerCard(dealerscorelist)
            dealerscorelist.append(dealerscore)
            dealercolor.append(dcolor)
            
            
def checkScore(x,y):
     tempscore = 0 
     z = len(x) 
     for p in range(0,z):
         if y[p] == "B":
             tempscore = tempscore + int(x[p])
         else:
             tempscore = tempscore - int(x[p])
     return tempscore
 
    
def bustout(x):
    
    if x > 21 or x <= 0:
        return True 
    

            


def renderscreen():
    global screen
    screen = pygame.display.set_mode((800,600))
    ###Title
    pygame.display.set_caption("Easy21")
    ###Icon
    icon = pygame.image.load('blackjack.png')
    pygame.display.set_icon(icon)
    ##Background
    bg = pygame.image.load('PokerBoard.png')
    screen.blit(bg,(0,0))
    ##Player Cards
    playerimg = pygame.image.load('playing-cards.png')
    screen.blit(playerimg,(playerX,playerY))
    ###Dealer Cards
    screen.blit(playerimg, (dealerX,dealerY))
    pygame.display.update()

def rendercards():
    global font
    font = pygame.font.Font('arbutusslab-regular.ttf', 12)
    x = len(playerscorelist)
    for y in range(0,x):
        if playercolor[y] == 'B':
            tempcolor = BLACK
        else:
            tempcolor = RED
        text = font.render(str(playerscorelist[y]), True, tempcolor,WHITEBG)
        textRect = text.get_rect()
        textRect.center = (playerX // 2, playerY //2)
        p = playercardCount * 16
        screen.blit(text,(playerX + p, playerY))
        pygame.display.update()
        
    z = len(dealerscorelist)
    for i in range(0,z):
        if dealercolor[i] == 'B':
            tempcolor2 = BLACK
        else: 
            tempcolor2 = RED
        text2 = font.render(str(dealerscorelist[i]), True, tempcolor2, WHITEBG)
        textRect2 = text2.get_rect()
        textRect2.center = (playerX // 2, playerY //2)
        b = dcardcount * 16
        screen.blit(text2,(dealerX + b, dealerY))
        pygame.display.update()

def addscoreplayer(x):
    playerscore, color = generatePlayerCard(x)
    playerscorelist.append(playerscore)
    playercolor.append(color)

def addscoredealer(x):
    
    dealerscore, dcolor = generateDealerCard(x)
    dealerscorelist.append(dealerscore)
    dealercolor.append(dcolor)
    
    
    

class Easy21(Env):
    def __init__(self):
        addscoredealer(dealerscorelist)
        dscore = checkScore(dealerscorelist, dealercolor)
        addscoreplayer(playerscorelist)
        pscore = checkScore(playerscorelist, playercolor)
        
        self.state = {"DealerScore" : dscore, "PlayerScore" :pscore}
        self.actions = ("hit","stick")
        init_state = self.state.copy()
        self.history = [init_state]
        
    def step(self,state, action):
        self.history.append({'player':action})
        
        if action == 'hit':
            addscoreplayer(playerscorelist)
            pscore = checkScore(playerscorelist, playercolor)
            self.state['PlayerScore'] = pscore
            new_state = self.state.copy()
            
            if bustout(self.state['PlayerScore']):
                reward = -1
                state = "terminal"
                self.history.append(state)
                return state, reward
        else:
            new_state = self.state.copy()
            self.history.append(new_state)
            state, reward = self.dealerplay()
            return state,reward
        
    def dealerplay(self):
        while self.state['DealerScore'] < 17:
            addscoredealer(dealerscorelist)
            ndscore = checkScore(dealerscorelist, dealercolor)
            self.state['DealerScore'] = ndscore
            
            new_state = self.state.copy()
            self.history.append(({'dealer':'hit'}))
            self.history.append(new_state)
            
            if bustout(ndscore):
                reward = 1
                state = 'terminal'
                self.history.append(state)
                print(state,reward)
                return state, reward
            
        self.history.append({"dealer:stick"})
        pscore = self.state['PlayerScore']
        dscore = self.state['DealerScore']
        
        state = 'terminal'
        if dscore< pscore: # player wins
            reward = 1
            print(state,reward)
            return state, reward                    
        if dscore == pscore: # draw
            reward = 0
            print(state,reward)
            return state, reward                 
        if dscore > pscore: # player loses
            reward = -1
            print(state,reward)
            return state, reward



class MC_Control():
    def __init__(self, exp, episode):
        self.actions = ("hit", "stick") 
        self.exp = exp           # constant parameter (influence the exploration/exploitation behavior when starting to learn)
        self.episode = episode    # number of episodes (games) to sample in order to make the agent learn
        
        self.Q = self.init_to_zeros()   # init Q function to zeros
        self.N = self.init_to_zeros()   # init N to zeros
        self.policy = "random"          # arbitrarily init the MC learning with a random policy
    def learn_q_value_function(self):
        """
        Update the Q function until optimal value function is reached.
        
        Returns
        ----------
        Q : {state: (action)}, Q value for every state-action pair
        """
        for i in range(self.episode):
            episode = self.play_episode() # run an episode using current policy
            self.policy = "e_greedy"      # policy switch from random to epsilon greedy
            for step in episode: 
                state, action, reward = step
                self.increment_counter(state, action) # increment state-action counter 
                self.update_Q(state, action, reward)  # update the Q value
                
        return self.Q 
    def init_to_zeros(self):
        """
        Init the Q function and the incremental counter N at 0 for every state-action pairs.
        
        Returns
        ----------
        lookup_table : {state: (action)}, a dictionnary of states as keys and actions as value
        """
        dealer_scores = np.arange(1, 11)
        player_scores = np.arange(1, 22)
        states = [(dealer_score, player_score) for player_score in player_scores for dealer_score in dealer_scores]       
        lookup_table = {}
        
        for state in states:
            lookup_table[state] = {"hit": 0, "stick": 0}  
            
        return lookup_table
    
    def play_episode(self):
        """
        Run a complete (from the initial state to the terminal state) Easy21 game sequence given a policy. 
        
        Returns
        ----------
        episode : [(state, action, reward)], a list of (statec, action, reward)
        """
        env = Easy21()           # init a game sequence
        state = env.state.copy() # init state
        episode = []                     # list of the steps of the game sequence
        while state != "terminal":      
            # pick an action regarding the current state and policy
            if self.policy == "random":
                action = self.random_policy()
            if self.policy == "e_greedy":
                action = self.e_greedy_policy(state)
                
            next_state, reward = deepcopy(env.step(state, action))
            
            step = (state, action, reward)
            
            state = next_state
            episode.append(step)   
            
        return episode
    def update_Q(self, state, action, reward):
        """
        Update Q value towards the error term. 
        
        Parameters
        ----------
        state : state, the current score
        action : string, the current score
        reward : int, the current score
        """
        lookup_state = (state["DealerScore"], state["PlayerScore"])
        
        # The learning rate, decaying regarding the number of times an action-state pair 
        # has been explored. It scale the amount of modification we want to bring to 
        # the Q value function.
        alpha_t = 1 / self.get_state_action_counter(state, action)
        
        # We adjust the Q value towards the reality (observed) minus what we estimated.
        # This term is usually descrived as the error term.
        self.Q[lookup_state][action] += alpha_t * (reward - self.Q[lookup_state][action]) 
        
        return None
    def increment_counter(self, state, action):
        """
        Increment N counter for every action-state pair encountered in an episode.
        
        Parameters
        ----------
        state : state, the current score
        action : string, the current score
        """
        lookup_state = (state["DealerScore"], state["PlayerScore"])
        self.N[lookup_state][action] += 1        
        return None
    
    def random_policy(self):
        """
        Return an action follwing a random policy (state free).
        
        Returns
        ----------
        action : string, random action
        """
        action = random.choice(self.actions)
        
        return action
    def e_greedy_policy(self, state):
        """
        Return an action given an epsilon greedy policy (state based).  
        
        Parameters
        ----------
        state : state, state where we pick the action
        
        Returns
        ----------
        action : string, action from epsilon greedy policy
        """
        e = self.exp/(self.exp + self.get_state_counter(state))
        if e > random.uniform(0, 1): 
            action = random.choice(self.actions)
        else:  
            action = self.get_action_w_max_value(state)
            
        return action
    
    def get_action_w_max_value(self, state):
        """
        Return the action with the max Q value at a given state.
        
        Parameters
        ----------
        state : state, state 
        
        Returns
        ----------
        action : string, action from epsilon greedy policy
        """
        lookup_state = (state["dealer_score"], state["player_score"])
        list_values = list(self.Q[lookup_state].values())
        if list_values[0] == list_values[1]:
            return self.random_policy()
        else:
            action = max(self.Q[lookup_state], key=self.Q[lookup_state].get) 
            return action
    def get_state_counter(self, state):
        """
        Return the counter for a given state.
        
        Parameters
        ----------
        state : state, state 
        
        Returns
        ----------
        counter : int, the number of times a state as been explored
        """
        lookup_state = (state["DealerScore"], state["PlayerScore"])
        counter = np.sum(list(self.N[lookup_state].values()))  
        
        return counter
    def get_state_action_counter(self, state, action):
        """
        Return the counter for a given action-state pair.
        
        Parameters
        ----------
        state : state 
        action : string
        
        Returns
        ----------
        counter : int, the number of times an action-state pair as been explored
        """
        lookup_state = (state["DealerScore"], state["PlayerScore"])
        counter = self.N[lookup_state][action]
        
        return counter
    
 

mc = MC_Control(exp=100, episode=100)
mc.learn_q_value_function()
                
'''
env = Easy21()
state1 = env.state
state2 = env.step(state1,'hit')
state3 = env.step(state=state2, action="stick")
print(env.history)
'''
'''
addscoreplayer(playerscorelist)
addscoreplayer(playerscorelist)
x = checkScore(playerscorelist, playercolor)
'''  
            
            
            
        
        
        
        
            
            
        
            
        
        
    
