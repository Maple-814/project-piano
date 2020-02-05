import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time

fs = 44100
frames = 1000

N_cross = 500

coeff_exp1 = 1
coeff_exp2 = 5

T_up = 5
T_down = 1
N_up = int(T_up*fs)
N_down = int(T_down*fs)

volume = 0.5
start_idx = 0

now = lambda x : int((time.time() - t0)*fs)

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
				self.list_tone[i][1] = (self.list_tone[i][1], N)
			


def generer_son(Tone, N_time, frames, N_cross, fs):
	outdata = np.zeros(frames)

	t = (N_time + np.arange(frames)) / fs
	A_cross = np.arange(N_cross)/N_cross

	for i,tone in enumerate(Tone.list_tone):

		freq = Tone.notes[tone[0]]
		note  = volume*np.sin(2*np.pi*t*freq)	




		if tone[2] == True:
			N_note = tone[1]
			note*= np.exp(-coeff_exp1 * (t-N_note/fs))

			if N_time-N_note > N_up:
				del Tone.list_tone[i]

			elif N_time < N_note-frames:
				note = np.zeros(frames)

			elif N_time < N_note:
				note[0:N_note-N_time] = 0
				taille = len(note[N_note-N_time : N_note+N_cross-N_time])
				note[N_note-N_time : N_note+N_cross-N_time]*= A_cross[0:taille]

			elif N_time < N_note+N_cross:
				note[0:N_note+N_cross-N_time]*= A_cross[N_time-N_note : N_cross]





		if tone[2] == False:
			N_note_up = tone[1][0]
			N_note_down = tone[1][1]
			note*= np.exp(-coeff_exp1 * (t-N_note_up/fs))

			if N_time < N_note_down:
				note[N_note_down-N_time:frames]*= np.exp(-coeff_exp2 * (t-N_note_down/fs))[N_note_down-N_time:frames]

			else:
				note*= np.exp(-coeff_exp2 * (t-N_note_down/fs))	


			if  N_time-N_note_down > N_down:
				del Tone.list_tone[i]

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
	
	for notes in tone.list_tone:
		print(notes[0])
	print("\n")

	
	start_idx+= frames


tone = Tone()



t0 = time.time()

with sd.Stream(channels=2, callback=callback, blocksize=frames):
	while True:
		time.sleep(1)
		tone.start_tone("Do",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Do",now(t0))
		tone.start_tone("Re",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Re",now(t0))
		tone.start_tone("Mi",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Mi",now(t0))
		tone.start_tone("Fa",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Fa",now(t0))
		tone.start_tone("Sol",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Sol",now(t0))
		tone.start_tone("La",now(t0))
		time.sleep(0.5)
		tone.stop_tone("La",now(t0))
		tone.start_tone("Si",now(t0))
		time.sleep(0.5)
		tone.stop_tone("Si",now(t0))
	


	time.sleep(10)




