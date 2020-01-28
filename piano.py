# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:12:25 2020

@author: LIU Yuhao
"""

import pygame
import sys

#  definition
size = (800,600)
key_white = (23*3,150*3)
key_black = (10*3,100*3)
black_position={0,1,3,4,5}
black = 0,0,0
white = 255,255,255
keynumber = 7*1


#
class Tone:
    def __init__(self, tonenumber):
        self.tonenumber = tonenumber
    
    def play(self, time):
        print ('play', self.tonenumber, 'for', time, 'ms')
    
    def fadeout(self, time):
        print ('stop in', time, 'ms')
        
    
################
    
def run():
    ##############
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(black)
    for i in range(keynumber):
        pygame.draw.rect(screen, white, ((i*key_white[0], 0),key_white))
        
        pygame.draw.rect(screen, black, ((i*key_white[0], 0),key_white), 1)
    for i in range(keynumber):
        if i%7 in black_position:
            pygame.draw.rect(screen, black, ((17*3+i*(key_white[0]), 0),key_black))
            
    pygame.display.update()
    
    
    ##########################
    keys=('q','w','e','r','t','y','u','i')
    
    tones={}
    for i in range(7):
        tones[i]=Tone(i+1)
        
    tones[0].fadeout(10)
    key_tones={}
    for i in range(7):
        key_tones[keys[i]]=tones[i]
    #key_tones=dict(keys, tones)
    
    key_tones['w'].play(300)
    
    #######################
    
    while True:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_tones.keys()):
            #play for 500ms
                key_tones[key].play(500)

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

        elif event.type == pygame.KEYUP and key in key_tones.keys():
            # Stops with 50ms fadeout
            key_tones[key].fadeout(50)
    
    
    ########################
run()
pygame.quit()
