import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


class Clavier:

	def __init__(self, fs, volume, T_segment, T_cross):
		"""
		fs : fréquence de répétition
		volume : amplitude des sinusoïde. doit pas depasser 1
		T_segment/N_sement : durée/taille des array de son
		T_cross : durée/taille de la section reduite
		pour enlever les bruits au début et à la fin		

		frequence : dict avec avec les fréquences associer aux nom des notes
		note : dict avec des bool pour chaque notes
			si True, la note est joué
			si False, la note est pas joué

		"""
		self.fs = fs
		self.volume = volume

		N_segment = int(T_segment*fs)		
		self.T_segment = T_segment
		self.N_segment = N_segment
		self.X_segment = np.linspace(0,T_segment,N_segment)

		N_cross = int(T_cross*fs)
		self.N_cross = N_cross
		self.A_cross = np.linspace(0,1,N_cross)

		note_nom = ["Do","Do#","Re","Re#","Mi","Mi#","Fa","Fa#","Sol","Sol#","La","La#","Si"]
		note_frequence = [261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440.0, 466.164, 493.883]

		frequence = {}
		note = {}
		for i in range(len(note_nom)-1):
			frequence[note_nom[i]] = note_frequence[i]
			note[note_nom[i]] = False
		self.frequence = frequence
		self.note = note


	def start(self, note):
		#joue la note en question
		self.note[note] = True


	def stop(self,note):
		#arrete de jouer la note en question
		self.note[note] = False


	def create_son(self):
		#creer le tableau de son

		Y = np.zeros(self.N_segment)

		for key in self.note.keys():
			if self.note[key] == True:
				Y+= self.volume*np.sin(2*np.pi*self.frequence[key]*self.X_segment)

		Y[0 : self.N_cross]*= self.A_cross
		Y[self.N_segment-self.N_cross : self.N_segment]*= self.A_cross[::-1]
		#Y[self.N_segment-self.N_cross : self.N_segment]= 0

		return Y


fs = 44100
volume = 0.5
T_segment = 1
T_cross = 0.005

clavier = Clavier(fs,volume,T_segment,T_cross)
clavier.start("Re")

note = clavier.create_son()

sd.play(note,fs)
sd.wait()

