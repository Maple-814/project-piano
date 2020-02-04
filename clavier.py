import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

fs = 44100
blocksize = 1000
freq = 440
duration = 15
start_idx = 0
N_cross = 100
coeff_exp = 1


class Tone:
	
	def __init__(self):
		self.list_tone = []

		nom_note = ("Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si")
		freq_note = (261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440, 466.164, 493.883)
		notes = {}
		for i in range(len(nom_note)):
			notes[nom_note[i]] = freq_note[i]
		self.notes = notes

	def start_tone(self,note,N):
		self.list_tone.append( [note, N, True])

	def stop_tone(self,note,N):
		for i,tone in enumerate(self.list_tone):
			if tone[0] == note:
				self.list_tone[i][2] = False
				self.list_tone[i][1] = N
			


def generer_son(Tone, N_time, frames, N_cross, fs):
	outdata = np.zeros(frames)

	t = (N_time + np.arange(frames)) / fs

	for tone in Tone.list_tone:

		freq = Tone.notes[tone[0]]
		N_note = tone[1]
		note  = np.sin(2*np.pi*t*freq)	

		if tone[2] == True:
			note*= np.exp(-coeff_exp * (t-N_note/fs))
		outdata+= note
	outdata = outdata.reshape(-1,1)
	return outdata



def callback(indata, outdata, frames, time,  status):
	if status:
		print(status)
	global start_idx
	global tone

	note = generer_son(tone, start_idx, frames, N_cross, fs)

	outdata[:] = note

	start_idx+= frames


tone = Tone()

tone.start_tone("Fa",44100)


with sd.Stream(channels=2, callback=callback, blocksize=blocksize):
	sd.sleep(int(duration * 1000))


print(tone.list_tone)



