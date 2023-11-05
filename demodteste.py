import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import pandas as pd
import pygame
import sys

def demodule_wav():
    taxa_amostragem, sinal = wav.read("output.wav")
    duration=len(sinal)/taxa_amostragem
    print(duration)
    # Calcular a transformada de Hilbert do sinal
    sinal_hilbert = signal.hilbert(sinal)
    envoltoria = np.abs(sinal_hilbert)  # Envoltória do sinal


    # Calcular a frequência instantânea a partir da fase do sinal analítico
    fase = np.unwrap(np.angle(sinal_hilbert))  # Desembrulhar a fase para evitar descontinuidades
    np.set_printoptions(threshold=sys.maxsize)
    print(fase)
    frequencia_instantanea = (np.diff(fase) / (2.0 * np.pi) * taxa_amostragem)  # Frequência instantânea em Hz
    momentos=[]
    # TODO - Fazer a transformada de hilbert ser refeita de x em x tempos
    #print(len(sinal))
    #sinal[201:-1]
    #sinal[x] = sinal[x+200]
    frequencias=[]
    freq_anterior=frequencia_instantanea[0]
    for i in range(0, (len(frequencia_instantanea) - 1)):
        if frequencia_instantanea[i] - freq_anterior < -350:
            momento = i / taxa_amostragem
            print(i)
            print(momento)
            if 1.5 <= momento <= (duration - 1):
                momentos.append("{:.5f}".format(momento))
                frequencias.append("{:.5f}".format(frequencia_instantanea[i]))

        freq_anterior = frequencia_instantanea[i]

    momentos_float = [float(i) for i in momentos]

    # Ordenando a lista de valores float
    momentos_ordenados = sorted(momentos_float)

    # Convertendo os valores de volta para strings com a precisão desejada
    precisao = 5
    momentos_ordenados_str = [f"{valor:.{precisao}f}" for valor in momentos_ordenados]

    print("Lista ordenada:", momentos_ordenados_str)


#demodule_wav()
