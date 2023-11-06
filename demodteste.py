import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

taxa_amostragem, sinal = wavfile.read("output.wav")
tam = len(sinal)

tempo = np.arange(len(sinal)) / taxa_amostragem

picos = []

for i in range(tam-1):
    par = []
    par = [sinal[i],sinal[i+1]]
    fft_pares = np.fft.fft(par)
    freq_fund = np.abs(fft_pares)*taxa_amostragem/len(fft_pares)
    picos.append(freq_fund)

print(len(tempo))
print(len(picos))
print(picos)
plt.figure(figsize=(12, 6))
plt.plot(tempo[:-1], picos)
plt.ylim(0,10000)
plt.xlabel('Tempo (s)')
plt.ylabel('Picos da FFT')

plt.show()