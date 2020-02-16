import numpy as np
import time

fs = 44100
frames = 500

N_cross = 500


T_up = 5
T_down = 1
N_up = int(T_up*fs)
N_down = int(T_down*fs)

volume = 0.1


class Tone:
    t_cross = 10e-3
    tau1 = 1
    tau2 = .2
    t_up = 5*tau1
    t_down = 5*tau2

    filename = "piano.txt"

    def __init__(self):
        self.list_tone = []

        nom_note = ("Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si", "Do+", "Re+", "Mi+")
        freq_note = (261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440, 466.164, 493.883, 523.251, 587.330, 659.255)
        notes = {}
        for i in range(len(nom_note)):
            notes[nom_note[i]] = freq_note[i]
        self.notes = notes
        self.start_idx = 0

    def start_tone(self, note, i_event):
        self.list_tone.append( (note, (self.start_idx, None) , True) )

        a = open(self.filename, 'a')            
        a.write(note+' '+str(1)+' '+str(self.start_idx))
        a.write('\n')
        a.close()
    
    
                
    def stop_tone(self, note_event, i_event):
        for i,tone in enumerate(self.list_tone):
            note, (tone_start_i, tone_stop_i) , pressed = tone
            if pressed and note==note_event:
                self.list_tone[i] = (note, (tone_start_i, self.start_idx) , False)
                a = open(self.filename, 'a')            
                a.write(note+' '+str(0)+' '+str(self.start_idx))            
                a.write('\n')
                a.close()
            
    
    def start_tone_read(self, note, i_event):
        self.list_tone.append( (note, (self.start_idx, None) , True) )

    def stop_tone_read(self, note_event, i_event):
        for i,tone in enumerate(self.list_tone):
            note, (tone_start_i, tone_stop_i) , pressed = tone
            if pressed and note==note_event:
                self.list_tone[i] = (note, (tone_start_i, self.start_idx) , False)
    
    def generer_next_son(self, frames, fs):
        outdata = np.zeros(frames)
    
        t = (self.start_idx + np.arange(frames)) / fs
    
        for i,tone in enumerate(self.list_tone):
            note, (tone_start_i, tone_stop_i) , pressed = tone
            
            freq = self.notes[note]
            relative_t = (t-tone_start_i/fs)
            a_cross = np.ones(frames)
            a_cross[relative_t<self.t_cross] = relative_t[relative_t<self.t_cross]/self.t_cross
            note  = volume*np.sin(2*np.pi*relative_t*freq)*np.exp( -relative_t/self.tau1 )*a_cross    
            if pressed == True:    
                if relative_t[-1] > self.t_up:
                    del self.list_tone[i]    
            
            if pressed == False:
                attenuation = np.ones(frames)
                relative_t_since_stop = (t-tone_stop_i/fs)
                attenuation[relative_t_since_stop>0] = np.exp(-relative_t_since_stop[relative_t_since_stop>0]/self.tau2)
                note *= attenuation
                if  relative_t_since_stop[-1] > self.t_down:
                    del self.list_tone[i]
    
            outdata+= note
    
        outdata = outdata.reshape(-1,1)
        self.start_idx += frames
        return outdata





def callback(indata, outdata, frames, the_time,  status):
    if status:
        print(status)
    #print(status, time, frames)
    #t0 = time.time()
    note = tone.generer_next_son(frames, fs)
    outdata[:] = note
    #print((time.time() - t0)*fs, frames)

tone = Tone()
    





