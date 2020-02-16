import time
import pygame

from instrument import callback, frames, tone, fs
#from instrument import *
from piano4 import KeyBoard
import sounddevice as sd


#############
kb=KeyBoard()



pygame.init()
pygame.display.set_caption('Piano')
screen = pygame.display.set_mode(kb.size)
kb.newpiano(screen)

tone.filename= "test1.txt"
a = open(tone.filename, "r")
lines = a.readlines()
t0 = time.time()
t = 0

with sd.Stream(channels=2, callback=callback, blocksize=frames):
    for line in lines[1:]:
        #print(tone.start_idx)
        note, pressed, N_time = line.split()
        N_time = int(N_time)
        while t < N_time/fs:
            t = time.time()-t0
            time.sleep(1e-1)
        if pressed == "1":
            tone.start_tone_read(note,N_time)
        if pressed == "0":
            tone.stop_tone_read(note,N_time)
        kb.pressedpiano2(screen,tone)
        pygame.display.init()
        pygame.init()
    sd.sleep(2000)
    pygame.quit()
##############
"""


    
    kb.esc = 0
    while kb.esc==0:
        
        kb.onecircle(screen, t0)
        #print(tone.list_tone)   
    pygame.quit()
"""
