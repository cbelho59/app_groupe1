from numpy.fft import fft
import numpy as np
import cmath
import math
from matplotlib.pyplot import *
import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

s, Fe = sf.read(r'mess_ssespace.wav')  # s : data Fe : frequence d'echantillonage
print(Fe)
# sd.play(s,Fe)

step = 1/Fe
signal = np.array(s)
# print(signal)
# print(s)
# t = np.arange(start,stop,step)


# plt.figure()
# plt.plot(s)
# plt.show()
alphabet = [chr(i) for i in range(65,65+26)]
# print(alphabet)
def fourier(signal):
    N = len(signal)
    FOURIER = [0]*N
    for p in range(N):
        fourierp = 0
        for n in range(N):
            fourierp += (signal[n]*cmath.exp(-2*1j*math.pi*n*p/N))
        # print(fourierp)
        fourierp = N * math.sqrt(fourierp.real**2+fourierp.imag**2)
        # print(fourierp)
        FOURIER[p] = fourierp
    return FOURIER

def findIndexMax(TF):
    max =  TF[0]
    indicemax = 0
    for i in range(1,int(len(TF)/2)):
        if(TF[i]>max):
            max = TF[i]
            indicemax = i
    return indicemax

def findIndexMaxMieux(TF,duree):
    max = TF[0]
    indicemax = 0
    for i in range(1, int(len(TF) / 2)):
        if(i/duree>=500 and i/duree<527):
            if (TF[i] > max):
                max = TF[i]
                indicemax = i
    return indicemax/duree

def fourierTot(signal):
    a = fourier(signal)
    Fe = 8000
    lenLettre = 2000
    duree = lenLettre/Fe
    fmax = findIndexMaxMieux(a,duree)
    tab = [i/duree for i in range(len(a))]
    plt.plot(tab, a)
    plt.show()
    return fmax

def decode(signal):
    str = ""
    # print(len(signal)/2500)
    for i in range(int(len(signal)/2500)+1):
        sig = signal[2500*i:2500*i+2000]
        # div = 4
        # si = [sig[i*div] for i in range(int(len(sig)/div))]
        # print(len(si))
        flettre = fourierTot(sig)
        print(flettre)
        lettre = alphabet[int(flettre-500)]
        str += lettre
        print(lettre)
    return str

print(decode(signal))
# flettre = fourierTot(signal)
# flettre = 500
# print(flettre)
# print(alphabet[int(flettre-500)])
# plt.show()
# print(alphabet[])
# a = fourier(s)
# print(a)
#
# plt.plot(tab,a)
# plt.show()
