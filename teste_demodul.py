import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# audio file to be read from
data, samplerate = sf.read('output.wav')
print(data)
print(len(data))
print(samplerate)
fileSize = int(len(data)) / samplerate
#
audio = []
#
for i in range(int(fileSize * 2 - 1)):
    print(i)
    x = sf.read('output.wav', start=i * 28000, stop=((28000 * (i + 1)) - 1))
    #print(x[0][0])
    audio.append(x[0])  # Use append to add elements to the list
    #audio.append(x[0][0])  # Use append to add elements to the list

# Convert the audio list to a numpy array
#audio = np.array(audio)

# Calcular a FFT do sinal
espectro = np.fft.fft(audio[1])
print(espectro)

# Calcular as frequências correspondentes ao espectro
frequencias = np.fft.fftfreq(len(espectro), 1 / samplerate)
len(frequencias)
print("len frequencias")
print(len(frequencias))
# Plotar o espectro de frequências
plt.figure(figsize=(10, 4))
plt.plot(frequencias[frequencias > 0], np.abs(espectro)[frequencias > 0])
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.title('Espectro de Frequências do Sinal de Áudio')
plt.grid(True)
plt.show()
