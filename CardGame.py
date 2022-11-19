#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:34:23 2022

@author: peter.figetakis
"""

import pygame
import random

pygame.init()
###Global Vars
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
playerX = 370
playerY = 480
dealerX = 370
dealerY = 480 - 150
###Set Window Size
screen = pygame.display.set_mode((800,600))

def createBoard():
    ###Title
    pygame.display.set_caption("Easy21")
    ###Icon
    icon = pygame.image.load('blackjack.png')
    pygame.display.set_icon(icon)
    ##Background
    bg = pygame.image.load('PokerBoard.png')
    screen.blit(bg,(0,0))
    
    
def createPlayer():
    ##Player Image and Location
    playerimg = pygame.image.load('playing-cards.png')
    screen.blit(playerimg,(playerX,playerY))

def createDealer():
    ##Player Image and Location
    playerimg = pygame.image.load('playing-cards.png')
    screen.blit(playerimg,(dealerX,dealerY))


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
    font = pygame.font.Font('arbutusslab-regular.ttf', 12)
    value = randint()
    cardstring = str(value)
    text = font.render(cardstring, True , color, WHITEBG )
    textRect = text.get_rect()
    textRect.center = (playerX // 2, playerY //2)
    screen.blit(text,(playerX + x,playerY))
    return value, colorstring

def generateDealerCard(x):
    if x <= 1:
        x = x
        color = BLACK
        colorstring = 'B'
    else:
        x = (x * 16)
        color,colorstring = randcolor()
    font = pygame.font.Font('arbutusslab-regular.ttf', 12)
    value = randint()
    cardstring = str(value)
    text = font.render(cardstring, True , color, WHITEBG )
    textRect = text.get_rect()
    textRect.center = (playerX // 2, playerY //2)
    screen.blit(text,(dealerX + x, dealerY))
    return value, colorstring

def checkScore(x,y):
     tempscore = 0
     for v in x: 
         if y[v] == 'B':
             tempscore = tempscore + v
         else:
            tempscore = tempscore - v
     return tempscore
    



running = True
createBoard()
createPlayer()
createDealer()

while running:
    for event in pygame.event.get():
        if playercardCount == 0:
            playerscore, color = generatePlayerCard(playercardCount)
            playerscorelist.append(playerscore)
            playercolor.append(color)
            
            dealerscore, dcolor = generateDealerCard(playercardCount)
            dealerscorelist.append(dealerscore)
            dealercolor.append(dcolor)
            
            playercardCount = playercardCount + 1
        else:
            if event.type == pygame.KEYDOWN:
                playercardCount = playercardCount + 1
                playerscore, color = generatePlayerCard(playercardCount)
                playerscorelist.append(playerscore)
                playercolor.append(color)
                x1 = checkScore(playerscorelist, playercolor)
                print(x1)
                
            
            
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        
            
    pygame.display.update()
            
