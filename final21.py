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
import random 


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
    if x <= 1:
        x = x
        color = BLACK
        colorstring = 'B'
    else:
        x = (x * 16)
        color,colorstring = randcolor()
    value = randint()
    return value, colorstring

def generateDealerCard(x):
    if x <= 1:
        x = x
        color = BLACK
        colorstring = 'B'
    else:
        x = (x * 16)
        color,colorstring = randcolor()
    value = randint()
    return value, colorstring

def dealerplay(x):
    x1 =  checkScore(dealerscorelist, dealercolor)
    play = True
    while play:
        x1 =  checkScore(dealerscorelist, dealercolor)
        if x1 >= 17 or x1 <= 0:
            play = False
        else:
            x = x + 1
            dealerscore, dcolor = generateDealerCard(x)
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
 
    
def checkstate(player,dealer):
    
    if player > 21 or player <= 0:
        print("Player busted out with {}".format(player))
        return False 
    
    if dealer > 21 or dealer <= 0:
        print("Dealer busted out with {}".format(dealer))
        return False
    
    if endsim == 1 and (dealer < 21 or dealer > 1) and (player < 21 or dealer > 1):
        if dealer > player :
            print("Dealer wins")
            return False
            
        elif dealer == player:
            print("Draw")
            return False
        else:
            print("Player Wins")
            
    else:
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
        self.sim_length = 0
        global pscore
        pscore = 0
        global dscore
        dscore = 0
        self.action_space = [0,1]
        self.observation_space = np.arange(1,22,1).tolist()
        if self.sim_length == 0:
            addscoreplayer(self.sim_length)
            addscoredealer(self.sim_length)
            self.sim_length += 1
        pscore = checkScore(playerscorelist, playercolor)
        self.state = pscore
        
    def step(self,action):
        if self.action == 0: 
            addscoreplayer(self.sim_length)
        if self.action == 1:
            dealerplay(self.sim_length)
            endsim = 1
        pscore = checkScore(playerscorelist, playercolor)
        dscore = checkScore(dealerscorelist, dealercolor)
        
        if endsim == 1 and (dscore < 21 or dscore > 1) and (pscore < 21 or pscore > 1):
            if dscore > pscore :
                print("Dealer Wins")
                reward =- 1
                self.sim_length = 987654321
            elif dscore == pscore :
                print("Draw")
                reward = 0
                self.sim_length = 987654321
            else:
                reward = 1 
                print('Player Wins')
                self.sim_length = 987654321
        if pscore > 21 or pscore <= 0:
            print("Player busted out with {}".format(pscore))
            self.sim_length = 987654321
        if dscore > 21 or dscore <= 0:
            print("Player busted out with {}".format(dscore))
            self.sim_length = 987654321
        if self.sim_length == 987654321:
            done = True
        else:
            done = False
        self.state = pscore
        self.sim_length += 1
        info = {}
        
        return self.state, reward, done, info
            
            
        
            
        
        
    
