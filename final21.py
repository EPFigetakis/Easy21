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


env = Easy21()
state1 = env.state
state2 = env.step(state1,'hit')
state3 = env.step(state=state2, action="stick")
print(env.history)

'''
addscoreplayer(playerscorelist)
addscoreplayer(playerscorelist)
x = checkScore(playerscorelist, playercolor)
'''  
            
            
            
        
        
        
        
            
            
        
            
        
        
    
