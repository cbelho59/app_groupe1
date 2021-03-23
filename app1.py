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

#il faut à chaque 
# s, Fe = sf.read(r'mess_ssespace.wav')  # s : data Fe : frequence d'echantillonage
Fe,s = wf.read(r'mess_ssespace.wav')  # s : data Fe : frequence d'echantillonage

step = 1/Fe
signal = np.array(s)
print(signal)
fmin = 501
fmax = 526

alphabet = [chr(i) for i in range(65,65+26)]

# def fourier(signal):
#     N = len(signal)
#     FOURIER = [0]*N
#     for p in range(N):
#         fourierp = 0
#         for n in range(N):
#             fourierp += (signal[n]*cmath.exp(-2*1j*math.pi*n*p/N))
#         # print(fourierp)
#         fourierp = N * math.sqrt(fourierp.real**2+fourierp.imag**2)
#         # print(fourierp)
#         FOURIER[p] = fourierp
#     return FOURIER

# def findIndexMax(TF):
#     max = TF[0]
#     indicemax = 0
#     for i in range(1,int(len(TF)/2)):
#         if(TF[i]>max):
#             max = TF[i]
#             indicemax = i
#     return indicemax

def findIndexMaxMieux(TF,duree):
    max = 0
    indicemax = 0
    for i in range(1, int(len(TF) / 2)):
        if(i/duree>=fmin and i/duree<=fmax):
            if (TF[i] > max):
                max = TF[i]
                indicemax = i
    return indicemax/duree

def fourierTot(signal):
    # a = fourier(signal)
    precision = 2
    N_fft = int(len(signal) * 10 ** precision)  # on utilise la méthode de zéro-padding pour augmenter la précision
    print(N_fft)
    print(signal)
    a = np.fft.fft(signal,N_fft)
    print(a)
    a = np.abs(a)
    # Fe = 8000

    duree_avec_padding = N_fft/Fe
    fmax = findIndexMaxMieux(a,duree_avec_padding)
    tab = [i/duree_avec_padding for i in range(len(a))]
    # plt.subplot((211))
    # plt.plot(tab,a)
    # # plt.show()
    # plt.grid()
    # plt.xlim(480, 580)
    # plt.subplot((212))
    # plt.plot(tab, b)
    # plt.grid()
    # plt.xlim(480, 580)
    # plt.show()
    print(fmax)
    return fmax

def decode(signal):
    print(signal)
    # print(len(signal))
    str = ""
    # print(len(signal)/2500)
    for i in range(math.floor(len(signal)/2500)):
        debut = 2500*i
        fin = debut + 2000
        # print(debut,fin)
        sig = signal[debut:fin]
        print(len(sig))
        # sig2 = sig*np.hanning(len(sig))
        # print('sig2')
        # print(sig2)
        # print('yo')
        flettre = fourierTot(sig)
        # print('flettre',flettre)
        lettre = alphabet[round(flettre-501)]
        str += lettre
        print(lettre)
    return str

print(decode(signal))
