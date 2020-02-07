# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:30:28 2020

@author: LIU Yuhao
"""

import time
import pygame

#import sys 
#sys.path.append(r'C:\Users\Louis\Desktop\LuMI\Piano')
from instrument import *
import sounddevice as sd


class KeyBoard(object):
    name_note = ("Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si", "Do+", "Re+", "Mi+")
    filename = 'piano.txt'
    size = (23*3*10, 150*3)
    key_white = (23*3,150*3)
    key_black = (10*3,100*3)
    black_position=(0,1,3,4,5)
    black = 0,0,0
    white = 255,255,255
    yellow = 225,225,0
    darkyellow = 128, 128, 0
    keynumber = 7*1
    keys=('q','2','w','3','e','r','5','t','6','y','7','u', 'i', 'o', 'p')
    pykeys=(pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p)
    pykeysblack=(pygame.K_2, pygame.K_3, pygame.K_5, pygame.K_6, pygame.K_7 )
    esc = 0
    
    
    def newpiano(self,screen):
        screen.fill(self.black)
        
        for i in range(self.keynumber+3):
            pygame.draw.rect(screen, self.white, ((i*self.key_white[0], 0),self.key_white))
            
            pygame.draw.rect(screen, self.black, ((i*self.key_white[0], 0),self.key_white), 1)
        
        for i in range(self.keynumber):
            if i%7 in self.black_position:
                pygame.draw.rect(screen, self.black, ((18*3+i*(self.key_white[0]), 0),self.key_black))
                
        pygame.display.update()
        
    
    def pressedpiano(self,screen):#draw a pressed piano with keys--list of keys pressed
        self.newpiano(screen) 
        pressed = pygame.key.get_pressed()
        
        for i, element in enumerate(self.pykeys):
            if pressed[element]:
                pygame.draw.rect(screen, self.yellow, ((i*self.key_white[0], 0),self.key_white))    
                
        
        for i in range(self.keynumber):            
            if i%7 in self.black_position:
                pygame.draw.rect(screen, self.black, ((18*3+i*(self.key_white[0]), 0),self.key_black))
         
        for i, element in enumerate(self.pykeysblack):
            if pressed[element]:
                x = (18*3+int(self.black_position[i])*(self.key_white[0]), 0)
                pygame.draw.rect(screen, self.darkyellow, (x , self.key_black))
            
        pygame.display.update()
    
        
    
    def onecircle(self, screen, t0):
        N_i = 10
        global tone
        
        key_tones={}
        for i in range(len(self.keys)):
            key_tones[self.keys[i]]=self.name_note[i]
        
        event = pygame.event.wait()
        

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            
          
        if event.type == pygame.KEYDOWN:
            if (key in key_tones.keys()):
                t1 = time.time()
                tone.start_tone(key_tones[key], N_i+int((t1-t0)*fs))
                self.pressedpiano(screen)
                a = open(self.filename, 'a')            
                a.write(str(key_tones[key])+' '+str(1)+' '+str(t1-t0))            
                a.write('\n')
                a.close()
            #play                  
               
            elif event.key == pygame.K_ESCAPE:
                
                self.esc = 1
                #print('quit', self.esc)
        elif event.type == pygame.KEYUP and key in key_tones.keys():
            t1 = time.time()
            tone.stop_tone(key_tones[key], N_i+int((t1-t0)*fs))
            self.pressedpiano(screen)
            a = open(self.filename, 'a')            
            a.write(str(key_tones[key])+' '+str(0)+' '+str(t1-t0))            
            a.write('\n')
            a.close()
            # Stops 
        
       




#############
kb=KeyBoard()



pygame.init()
screen = pygame.display.set_mode(kb.size)
kb.newpiano(screen)

kb.filename = 'test1.txt'

a = open(kb.filename, 'w')            
a.write('#Tones Down_or_up Time(s)')            
a.write('\n')
a.close()
##############

with sd.Stream(channels=2, callback=callback, blocksize=frames):
    t0 = time.time()    
    
    kb.esc = 0
    while kb.esc==0:
        
        kb.onecircle(screen, t0)
        #print(tone.list_tone)   
    pygame.quit()
    
        
