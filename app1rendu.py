from numpy.fft import fft
import numpy as np
import math
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd

def decode(fichier):
    def findIndexMaxMieux(TF, duree): #cherche la fréquence maximale entre fmin et fmax
        maximum = 0
        indicemax = 0
        for i in range(1, int(len(TF) / 2)):
            if (i / duree >= fmin and i / duree <= fmax): #si l'indice correspond à une fréquence qui nous intéresse
                if (TF[i] > maximum):
                    maximum = TF[i]
                    indicemax = i
        return indicemax / duree, maximum #on renvoie aussi la valeur du maximum pour savoir si il n'y a que du bruit (donc un espace) ou du signal (donc une lettre)
    def findIndexMaxTout(TF): #cherche la fréquence maximale entre fmin et fmax
        maximum = 0
        indicemax = 0
        for i in range(0, int(len(TF) / 2)):
            if (TF[i] > maximum):
                maximum = TF[i]
                indicemax = i
        return indicemax, maximum #on renvoie aussi la valeur du maximum pour savoir si il n'y a que du bruit (donc un espace) ou du signal (donc une lettre)
    def fourier(signal):
        lenpadding = len(signal)*100 #valeur arbirtraire qui est un bon compromis entre temps de calcul et précision
        TF = np.fft.fft(signal, lenpadding) # on utilise la méthode de zéro-padding pour augmenter la précision
        TF = np.abs(TF) #dans notre méthode, on s'intéresse seulement au module de la fonction
        duree_avec_padding = lenpadding / Fe #durée du signal incluant le zero-padding
        fmax, amplitudeFmax = findIndexMaxMieux(TF, duree_avec_padding) #on cherche la fréquence max et l'amplitude max entre fmin et fmax
        tab = [i / duree_avec_padding for i in range(len(TF))]
        plt.plot(tab, TF)
        plt.xlim(480,540)
        return fmax, amplitudeFmax,TF,duree_avec_padding

    fmin = 501
    fmax = 526
    alphabet = [chr(i) for i in range(65, 65 + 26)] #création d'un alphabet
    lenchar = 2000
    lenentre = 500
    str = "" #chaine de caractère pour le retour
    s, Fe = sf.read(fichier) #ouverture du fichier
    signal = np.array(s)
    sep = 0.75
    if (len(signal) == lenchar):#on utilise une porte si le signal n'est composé que d'un seul caractère
        signal = signal * np.hanning(len(signal))
    amplitudes = [] #amplitudes du pic de la TF, pour savoir si c'est du bruit (donc un espace) ou du signal (donc une lettre)
    for i in range(math.ceil(len(signal)/(lenchar+lenentre))):
        debut = (lenchar+lenentre)*i    #debut du ieme caractere
        fin = debut + lenchar   #fin du ieme caractere
        flettre, amplitudeFlettre, TF, d= fourier(signal[debut:fin]) #calcul de la TF
        amplitudes.append(amplitudeFlettre)
        amplitudeRelative = amplitudes[-1]/amplitudes[0] #calcul de l'amplitude relative avec le premier caractère, qui ne peut pas etre un espace
        if(amplitudeRelative<sep): #si l'amplitude relative est inférieure à 1/2, alors on considere que c'est un espae
            str += " "
        elif (amplitudeRelative>2): # si l'amplitude relative est inférieure à 1/2, alors on considere que c'est un espae
                # print('pb')
                j, max = findIndexMaxTout(TF)
                indice = j
                while (TF[j - 1] - TF[j] < 0):
                    j -= 1
                tab = np.arange(len(TF))
                bruit = [0] * len(tab)
                # print(max)
                for k in range(1, len(tab)):
                    if (indice != tab[k]):
                        # print("indice",indice)
                        # print("j",j)
                        bruit[k] = abs(max * math.sin((math.pi / (indice - j) * (tab[k] - indice))) / (
                                    math.pi / (indice - j) * (tab[k] - indice)))
                    else:
                        bruit[k] = max
                # print(j / d)
                tab = [i / d for i in range(len(TF))]
                # plt.plot(tab, bruit)
                # plt.close()
                plt.plot(tab, TF - bruit)

                for i in range(len(bruit)):
                    if(bruit[i]==0):
                        TF[i]=0
                    else:
                        TF[i]=TF[i]/bruit[i]
                flettre, rien = findIndexMaxMieux(TF, d)
                lettre = alphabet[round(flettre - fmin)]  # lettre de l'alphabet qui correspond à cette fréquence
                str += lettre
        else:
            lettre = alphabet[round(flettre - fmin)] #lettre de l'alphabet qui correspond à cette fréquence
            str += lettre
        if (amplitudeRelative > sep):
            print(alphabet[round(flettre - fmin)])
            print(flettre)
            print(round(amplitudeRelative,2))
        # if i == 2:
        #     plt.show()
        # else:
        #     plt.close()
        print(i)
        # plt.show()
        # plt.savefig("%s " %i+lettre+" %s %s.png" %(round(amplitudeRelative,2),flettre))
        plt.close()
    return str

#code pour décoder tous les messages donnés
#
# FILES = ["symboleA.wav","symboleA2.wav","symboleU.wav","symboleU2.wav","mess_ssespace.wav","mess.wav","mess_difficile.wav"]
# for file in FILES:
#     print(decode(file))
print(decode('mess_difficile.wav'))