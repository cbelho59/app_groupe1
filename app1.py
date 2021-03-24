from numpy.fft import fft
import numpy as np
import math
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf

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

    def findIndexMaxTout(TF): #cherche la fréquence maximale sur l'ensemble de la TF
        maximum = 0
        indicemax = 0
        for i in range(0, int(len(TF) / 2)):
            if (TF[i] > maximum):
                maximum = TF[i]
                indicemax = i
        return indicemax, maximum #on renvoie aussi la valeur du maximum pour savoir si il n'y a que du bruit (donc un espace) ou du signal (donc une lettre)

    def fourier(signal): #calule la TF du signal
        lenpadding = len(signal)*100 #valeur arbirtraire qui est un bon compromis entre temps de calcul et précision
        TF = np.fft.fft(signal, lenpadding) # on utilise la méthode de zéro-padding pour augmenter la précision
        TF = np.abs(TF) #dans notre méthode, on s'intéresse seulement au module de la fonction

        duree_avec_padding = lenpadding / Fe #durée du signal incluant le zero-padding
        fmax, amplitudeFmax = findIndexMaxMieux(TF, duree_avec_padding) #on cherche la fréquence max et l'amplitude max entre fmin et fmax
        return fmax, amplitudeFmax,TF,duree_avec_padding

    fmin = 501
    fmax = 526
    alphabet = [chr(i) for i in range(65, 65 + 26)]
    lenchar = 2000
    lenentre = 500
    str = "" #chaine de caractère pour le retour
    s, Fe = sf.read(fichier) #ouverture du fichier
    signal = np.array(s)

    if (len(signal) == lenchar):#on utilise une porte si le signal n'est composé que d'un seul caractère
        signal = signal * np.hanning(len(signal))

    amplitudes = [] #amplitudes du pic de la TF, pour savoir si c'est du bruit (donc un espace) ou du signal (donc une lettre)

    for i in range(math.ceil(len(signal)/(lenchar+lenentre))):
        debut = (lenchar+lenentre)*i    #debut du ieme caractere
        fin = debut + lenchar   #fin du ieme caractere
        flettre, amplitudeFlettre, TF, d = fourier(signal[debut:fin]) #calcul de la TF
        amplitudeRelativeEspace = 0.75
        amplitudes.append(amplitudeFlettre)
        amplitudeRelative = amplitudes[-1]/amplitudes[0] #calcul de l'amplitude relative avec le premier caractère, qui ne peut pas etre un espace
        if(amplitudeRelative<amplitudeRelativeEspace): #si l'amplitude relative est inférieure à amplitudeRelativeEspae, alors on considere que c'est un espae
            str += " "
        elif (amplitudeRelative>2):
            #si l'amplitude relative est très importante, c'est qu'il y a un énorme pic qui cache la vrai fréquence envoyée
                j, max = findIndexMaxTout(TF)
                if(j/d<513): #si la fréquence du bruit est inférieure à la fréquence moyenne d'une lettre
                    #On va diviser la partie droite du pic de bruit par la partie gauche pour essayer de le retirer
                    for k in range(int(100*d)):
                        if(TF[j-k]>3):
                            TF[k+j] = TF[k+j]/TF[j-k]
                        else:
                            TF[k+j] = 0
                    for k in range(int(100*d)):
                        TF[j-k] = 0

                else: #si la fréquence du bruit est supérieure à la fréquence moyenne d'une lettre
                    # On va diviser la partie gauche du pic de bruit par la partie droite pour essayer de le retirer
                    for k in range(int(100*d)):
                        if(TF[j+k]>3):
                            TF[j-k] = TF[j-k]/TF[j+k]
                        else:
                            TF[j-k] = 0
                    for k in range(int(100*d)):
                        TF[j+k] = 0

                flettre, max = findIndexMaxMieux(TF, d) #On recalcule la fréquence max avec le bruit retiré

                if (max < 3):  # si la fréquence maximale est inférieure à 3, c'est probablement un espace
                    str += " "
                else: #si ce n'est pas un espace
                    lettre = alphabet[round(flettre - fmin)]  # lettre de l'alphabet qui correspond à cette fréquence
                    str += lettre
                tab = [i/d for i in range(len(TF))]
                plt.plot(tab, TF)
                plt.xlim(490, 530)
        else: #si c'est une lettre normale envoyée, sans bruit particulier
            lettre = alphabet[round(flettre - fmin)] #lettre de l'alphabet qui correspond à cette fréquence
            str += lettre
        if(i>25):
            print(alphabet[round(flettre-fmin)])
            print(flettre)
            plt.show()
        plt.close()
        del(TF) #la mémoire peut être un pb, donc on efface cette variable
    return str


FILES = ["symboleA.wav","symboleA2.wav","symboleU.wav","symboleU2.wav","mess_ssespace.wav","mess.wav","mess_difficile.wav"]
for file in FILES:
    print(decode(file))
# print(decode('mess_difficile.wav'))