import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

# Carregar o arquivo de áudio (substitua 'caminho/para/arquivo.wav' pelo caminho do seu arquivo)
taxa_amostragem, sinal = wav.read('output.wav')

# Calcular a transformada de Hilbert do sinal
sinal_hilbert = signal.hilbert(sinal)
envoltoria = np.abs(sinal_hilbert)  # Envoltória do sinal

anterior = envoltoria[0]

for i in range(0, (len(envoltoria)-1)):
    if (envoltoria[i]-anterior)>0.15:
        print(i/taxa_amostragem)
    anterior = envoltoria[i]

# Calcular a frequência instantânea a partir da fase do sinal analítico
fase = np.unwrap(np.angle(sinal_hilbert))  # Desembrulhar a fase para evitar descontinuidades
frequencia_instantanea = (np.diff(fase) / (2.0 * np.pi) * taxa_amostragem)  # Frequência instantânea em Hz

# Filtrar frequências entre 0 e 42000 Hz
# frequencia_filtrada = np.clip(frequencia_instantanea, 0, 4000)

# Plotar o sinal de áudio e a frequência instantânea
tempo = np.arange(len(sinal)) / taxa_amostragem

# t = len(tempo)/24000-1
# # print(t)
# # 24000 posições a cada 0.5s
# pivo = 0
#
# for j in range(0, int(t)):
#     for i in range(0, 17):
#         pivo += 1500
#         print(i)
#         print(frequencia_filtrada[pivo])

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(tempo, sinal, label='Sinal de Áudio')
plt.plot(tempo, envoltoria, label='Envoltória')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(tempo[:-1], frequencia_instantanea)
plt.xlabel('Tempo (s)')
plt.ylabel('Frequência Instantânea (Hz)')
plt.ylim(0, 4000)  # Limitar o eixo y entre 0 e 2000 Hz
plt.tight_layout()
plt.show()