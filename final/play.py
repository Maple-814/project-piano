import time
import pygame

from instrument import callback, frames, tone
from piano4 import KeyBoard
import sounddevice as sd



#############
kb=KeyBoard()



pygame.init()
screen = pygame.display.set_mode(kb.size)
pygame.display.set_caption('Piano')
kb.newpiano(screen)

tone.filename = 'test1.txt'

a = open(tone.filename, 'w')            
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
