import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import pandas as pd
def demodule_wav():
    # Carregar o arquivo de áudio (substitua 'caminho/para/arquivo.wav' pelo caminho do seu arquivo)
    taxa_amostragem, sinal = wav.read("output.wav")

    # Calcular a transformada de Hilbert do sinal
    sinal_hilbert = signal.hilbert(sinal)
    envoltoria = np.abs(sinal_hilbert)  # Envoltória do sinal

    anterior = envoltoria[0]
    valores = []

    for i in range(0, (len(envoltoria)-1)):
        if (envoltoria[i]-anterior)>0.15:
            valores.append("{:.5f}".format(i/taxa_amostragem))
        anterior = envoltoria[i]

    # Eliminar valores próximos
    valores_finais = [valores[0]]
    for valor in valores[1:]:
        if not any(np.isclose(float(valor), float(v), atol=0.00001) for v in valores_finais):
            valores_finais.append(valor)

    # Calcular a frequência instantânea a partir da fase do sinal analítico
    fase = np.unwrap(np.angle(sinal_hilbert))  # Desembrulhar a fase para evitar descontinuidades
    frequencia_instantanea = (np.diff(fase) / (2.0 * np.pi) * taxa_amostragem)  # Frequência instantânea em Hz

    # Plotar o sinal de áudio e a frequência instantânea
    tempo = np.arange(len(sinal)) / taxa_amostragem

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

    print(valores)

    print(valores_finais)

    differences = []
    for i in range(1, len(valores_finais)):
        diff = "{:.5f}".format(float(valores_finais[i]) - float(valores_finais[i - 1]))
        differences.append(diff)

    print(differences)
# Assuming you have the list 'differences' as defined earlier

    middle_values = differences[3:-1]  # Selecting values from index 3 to the second-to-last element
    print(middle_values)
    even_values = [middle_values[i] for i in range(len(middle_values)) if i % 2 == 0]
    print(even_values)

    excel_data = pd.read_excel(
        'nibble_ascii.xlsx')  # Replace 'path_to_your_excel_file.xlsx' with the actual path to your Excel file

    # Extract the values from 'even_values' for comparison
    truncated_values = [float(value[:-2]) for value in even_values]

    corresponding_values = [
        excel_data.loc[excel_data['Tempo'] == value, 'Hertz'].values[0] for value in
        truncated_values]
    # Compare the values to the corresponding column in the Excel table

    print(corresponding_values)
demodule_wav()