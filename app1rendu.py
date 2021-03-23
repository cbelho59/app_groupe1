from numpy.fft import fft
import numpy as np
import cmath
import math
from matplotlib.pyplot import *
import soundfile as sf
from scipy.io import wavfile as wf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

def decode(fichier):
    def findIndexMaxMieux(TF, duree):
        maximum = 0
        indicemax = 0
        for i in range(1, int(len(TF) / 2)):
            if (i / duree >= fmin and i / duree <= fmax):
                if (TF[i] > maximum):
                    maximum = TF[i]
                    indicemax = i
        return indicemax / duree, maximum

    def fourier(signal):
        precision = 2
        lenpadding = int(
            len(signal) * 10 ** precision)  # on utilise la méthode de zéro-padding pour augmenter la précision
        TF = np.fft.fft(signal, lenpadding)

        TF = np.abs(TF)
        duree_avec_padding = lenpadding / Fe
        fmax, amplitudeFmax = findIndexMaxMieux(TF, duree_avec_padding)
        tab = [i / duree_avec_padding for i in range(len(TF))]

        return fmax, amplitudeFmax

    fmin = 501
    fmax = 526
    alphabet = [chr(i) for i in range(65, 65 + 26)]
    lenchar = 2000
    lenentre = 500
    str = ""
    s, Fe = sf.read(fichier)  # s : data Fe : frequence d'echantillonage
    signal = np.array(s)

    if (len(signal) == lenchar):
        signal = signal * np.hanning(len(signal))
    amplitudes = []
    for i in range(math.ceil(len(signal)/(lenchar+lenentre))):
        debut = (lenchar+lenentre)*i
        fin = debut + lenchar
        flettre, amplitudeFlettre = fourier(signal[debut:fin])

        amplitudes.append(amplitudeFlettre)
        amplitudeRelative = amplitudes[-1]/amplitudes[0]
        if(amplitudeRelative<0.5):
            str += " "
        else:
            lettre = alphabet[round(flettre - fmin)]
            str += lettre
    return str

FILES = ["symboleA.wav","symboleA2.wav","symboleU.wav","symboleU2.wav","mess_ssespace.wav","mess.wav","mess_difficile.wav"]
for file in FILES:
    print(decode(file))