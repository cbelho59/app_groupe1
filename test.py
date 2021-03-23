#!/usr/bin/env python
# coding: utf-8

# # A la recherche de la fréquence perdue
# ##### Groupe I~G : Youssef AHAMMOU, LEE Joe Ing, Bastien SABLE, Saad NIDIFI
#
# ### Problème
# Dans le cadre d'un système de communication de secours en milieu difficile (sous-marin, enterré), votre équipe d'ingénieurs a été engagée pour tester une technique basée sur l'envoi de signaux sinusoïdaux à différentes fréquences. L'information sera portée par la valeur de cette fréquence : les 26 lettres de l'alphabet seront codées par une fréquence comprise entre 501 et 526 Hz, une par Hz et ne seront pas superposées. Ces signaux sont corrompus par différents perturbateurs additifs (bruits, autres composantes), dont la puissance peut être significative, et liés au canal de transmission.
#
# ### Solution
# Nous avons conçu une fonction python `decode(s,Fe)` permettant d'analyser un message comprenant un nombre quelconque de symboles codés et qui renvoie la chaîne de caractères trouvée en majuscules. Nous avons testé cette fonction sur des différents signaux dans la fonction `decrypt_mess(wav_file)`.

#

# In[1]:


# get_ipython().run_line_magic('matplotlib', 'inline')

from scipy.io import wavfile as wf
import matplotlib.pyplot as plt
import scipy.signal as sgn
import numpy as np
import math


# La fonction decode contient 2 fonctions intérieures : `fft_np(signal)` et `decrypt_string(signal) `

# In[2]:


def decode(s, fe):
    amplitude_lettres = []  # stocke l'ampitude de chaque lettre afin de les comparer savoir si c'est une lettre ou un espace
    decoded_string = []  # stocke la lettre décodé dans un tableau
    nb_echantillon = 2000  # longueur d'un symbole(échantillons)
    step = 500  # longeur entre symboles
    N = s.shape[0]  # taille de signal
    print(N)
    nb_symbol = int(N / nb_echantillon)  # nombre de symboles
    hann_bool = False
    freq_min = 501
    freq_max = 526

    if (N == 2000):
        hann_bool = True  # si la longeur du symbole est 2000, nous allons appliquer une fenêtre de Hann

    """--------------------------------------------------------------------------------------"""
    """--------fft_np : Fonction qui calcule la Fast Fourier Transform avec précision--------"""
    """--------------------------------------------------------------------------------------"""

    def fft_np(signal):
        precision = 2
        N_fft = int(len(signal) * 10 ** precision)  # on utilise la méthode de zéro-padding pour augmenter la précision
        print(len(signal))
        print(N_fft)
        print(signal)
        fft_signal = np.fft.fft(signal, N_fft)  # on calcule la fast fourier transform du signal
        # plt.plot(fft_signal)
        # plt.show()
        return N_fft, fft_signal  # N_fft : taille de signal transformé ; fft_signal : signal transformé

    """--------------------------------------------------------------------------------------"""
    """---------------------------------Fin de fonction fft_np-------------------------------"""
    """--------------------------------------------------------------------------------------"""

    """--------------------------------------------------------------------------------------"""
    """--------decrypt_string : Fonction qui décode un caractère de 2000 échantillons--------"""
    """--------------------------------------------------------------------------------------"""

    def decrypt_string(signal):
        x = signal
        # print(len(x))
        # print(nb_echantillon)
        print(x)
        if (hann_bool):
            x = x * np.hanning(nb_echantillon)  # on applique une fenêtre de hanning de même taille que notre signal
        else:
            x = signal  # il s'est avéré que le fenêtrage nous donne un faux résultat pour décoder le message contenant plus d'un symbole

        N_fft, fft_signal = fft_np(x)  # on calcule la fft de notre signal
        print(fft_signal)
        borne_max = round(
            freq_max * N_fft / fe)  # on définit la borne maximale qui correspond à la fréquence max (*N_fft/fe pour avoir le bon ordre de grandeur suite au zéro-padding)
        borne_min = round(
            freq_min * N_fft / fe)  # on définit la borne minimale qui correspond à la fréquence min (*N_fft/fe pour avoir le bon ordre de grandeur suite au zéro-padding)
        pic = np.argmax(abs(fft_signal)[borne_min:borne_max])  # indice de la valeur du pic
        freq_lettre = int(borne_min + pic)  # fréquence du pic

        amplitude_lettres.append(10)  # on stocke l'amplitude à la fréquence de lettre
        difference = abs(amplitude_lettres[0] - amplitude_lettres[len(
            amplitude_lettres) - 1])  # on compare l'amplitude de chaque symbole avec celle de le premier symbole pour déduire si c'est un espace ou un symbole

        if (difference > 550000):
            return " "  # si l'écart est trop élévé, c'est un espace

        freq_lettre = round(
            freq_lettre * fe / N_fft)  # on retrouve la fréquence avec l'ordre de grandeur du départ (501-526)
        lettre = chr(int(freq_lettre - freq_min + 65))  # on traduit le caractère en utilisant le code ASCII (A = 65)
        return lettre

    """--------------------------------------------------------------------------------------"""
    """-----------------------------Fin de fonction decrypt_string---------------------------"""
    """--------------------------------------------------------------------------------------"""

    for symbol in range(nb_symbol):
        start = int(symbol * (
                    nb_echantillon + step))  # (nb_echantillon)2000 par symbole, (step)500 entre symboles, 2000 zéros pour « espace »
        end = int(start + nb_echantillon)  # on prend l'intevalle de 2000 (0-2000 ; 2500-4500 ; 5000-7000 ...)

        if len(s[start:end]) != nb_echantillon:
            break  # on doit être sur que la taille du signal que l'on coupe est bien la taille d'un symbole

        decoded_symbol = decrypt_string(s[start:end])
        decoded_string.append(decoded_symbol)  # on stocke les lettres dans un tableau

    res = (" ".join(decoded_string))  # on concatène le tableau en une chaîne de caractère
    print(res)

    return res


# ## Tester cette méthode sur des signaux synthétiques

# In[3]:


def decrypt_mess(wav_file):
    fe, s = wf.read(wav_file)
    print(s)
    decode(s, fe)
decrypt_mess('mess_difficile.wav')