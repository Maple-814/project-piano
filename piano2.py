# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:21:21 2020

@author: Louis
"""
import time
import pygame
import numpy as np
import sys 
sys.path.append(r'C:\Users\Louis\Desktop\LuMI\Piano')
from clavier import *
import sounddevice as sd
'''
class Tone:
   
    #tonnumber is the tone of the note
    
    def __init__(self, tonenumber):
        self.tonenumber = tonenumber
    
    def play(self):
        print ('play', self.tonenumber, 'for', time, 'ms')
    
    def fadeout(self):
        print ('stop', self.tonenumber, 'in', time, 'ms')
'''

class KeyBoard(object):
    name_note = ("Do", "Re", "Mi", "Fa", "Sol", "La", "Si")
    filename = 'piano.txt'
    size = (23*3*7, 150*3)
    key_white = (23*3,150*3)
    key_black = (10*3,100*3)
    black_position={0,1,3,4,5}
    black = 0,0,0
    white = 255,255,255
    yellow = 225,225,0
    keynumber = 7*1
    keys=('q','w','e','r','t','y','u')
    pykeys=(pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u)
    
    def newpiano(self,screen):
        screen.fill(self.black)
        
        for i in range(self.keynumber):
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
            pygame.draw.rect(screen, self.black, ((i*self.key_white[0], 0),self.key_white), 1)
            if i%7 in self.black_position:
                pygame.draw.rect(screen, self.black, ((18*3+i*(self.key_white[0]), 0),self.key_black))
                
        pygame.display.update()

    def writekeystates(self):
        pressed_p = np.zeros((self.keynumber,1))
        pressed = pygame.key.get_pressed()
        for i, element in enumerate(self.pykeys):
            if pressed[element]:
                pressed_p[i]=1
            else:
                pressed_p[i]=0
        return (list(pressed_p))
     
    def comparekeystates(self, pressed1, pressed2):
        action=list(np.zeros((self.keynumber,1)))
        for i, element in enumerate(pressed1):
            if pressed2[i] and element:
                action[i]=0
            elif pressed2[i]:
                action[i]=1
            else:
                action[i]=2
        
        return (action)
    
    
    def onecircle(self, screen, t0, N_i):
        
        global tone
        
        key_tones={}
        for i in range(7):
            key_tones[self.keys[i]]=self.name_note[i]
        
        event = pygame.event.wait()
        

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            
          
        if event.type == pygame.KEYDOWN:
            if (key in key_tones.keys()):
                t1 = time.time()
                tone.start_tone(key_tones[key], N_i+int((t1-t0)*fs)+blocksize)
                self.pressedpiano(screen)
            #play                  
               
            elif event.key == pygame.K_ESCAPE:
                print('quit')
                pygame.quit()
                
        elif event.type == pygame.KEYUP and key in key_tones.keys():
            t1 = time.time()
            tone.stop_tone(key_tones[key], N_i+int((t1-t0)*fs)+blocksize)
            self.pressedpiano(screen)
            # Stops 
        
       
        
    def run(self):
        
        
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        self.newpiano(screen)
                
        
        
        ##########################
     
        tone = Tone()
        
        key_tones={}
        for i in range(7):
            key_tones[self.keys[i]]=self.name_note[i]
        '''   
        f = open(self.filename, 'w')
        f.write('#Do Rei Mi Fa So La Si time\n')
        f.close()
        t0 = time.time()
        '''
        t1=0
        t2=0
        keystats=list(np.zeros((self.keynumber,1)))
        while True:
            
            time.sleep(0.1)
            #t1 = time.time()
            event = pygame.event.wait()
    
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key = pygame.key.name(event.key)
    
            if event.type == pygame.KEYDOWN:
                if (key in key_tones.keys()):
                #play for 500ms                  
                    self.pressedpiano(screen)
                    keystats = self.writekeystates()
                elif event.key == pygame.K_ESCAPE:
                    print('quit')
                    pygame.quit()
                    break
    
            elif event.type == pygame.KEYUP and key in key_tones.keys():
                # Stops with 50ms fadeout
                self.pressedpiano(screen)
                keystats = self.writekeystates()
                
            if len(keystats)==(self.keynumber+1):
                keystats[-1]=(time.time()-t0)
            else:
                keystats.append((time.time()-t0))
            '''
            a = open(self.filename, 'a')
            for i, element in enumerate(keystats):
                a.write(str(element)+' ')
            
            a.write('\n')
            a.close()
            '''
           # t2 = time.time()
        
        



kb=KeyBoard()



pygame.init()
screen = pygame.display.set_mode(kb.size)
kb.newpiano(screen)
t0 = time.time()




'''

while True:
   #time.sleep(int(duration * 1000))
   kb.onecircle(screen, t0) 
'''
with sd.Stream(channels=2, callback=callback, blocksize=blocksize):
    
    tone.start_tone("Fa",44100)
    
    while True:
        time.sleep(0.1)
        kb.onecircle(screen, t0, N_i=1000)
        print(tone.list_tone)   
      
    sd.sleep(int(duration * 1000))
        
print(tone.list_tone)       

pygame.quit()

#kb.run()
  
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        