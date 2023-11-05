import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import pandas as pd
import pygame

def demodule_wav():
    # Carregar o arquivo de áudio (substitua 'caminho/para/arquivo.wav' pelo caminho do seu arquivo)
    pygame.init()
    taxa_amostragem, sinal = wav.read("output.wav")

    # Calcular a transformada de Hilbert do sinal
    sinal_hilbert = signal.hilbert(sinal)
    #TODO - Trocar envoltória por frequencia instantanea
    envoltoria = np.abs(sinal_hilbert)  # Envoltória do sinal
    duration=len(envoltoria)/taxa_amostragem
    print(duration)
    anterior = envoltoria[0]

    segment_size = 24000  # Tamanho do segmento

    # Inicializar o array que irá armazenar os resultados da transformada de Hilbert para cada segmento
    sinal_hilbert_array = np.zeros_like(sinal, dtype=np.complex128)

    # Calcular a transformada de Hilbert para cada segmento
    for i in range(0, len(sinal), segment_size):
        segmento = sinal[i:i + segment_size]
        sinal_hilbert_segmento = signal.hilbert(segmento)
        sinal_hilbert_array[i:i + segment_size] = sinal_hilbert_segmento

    valores = []
    incremento = 0.5
    start_time = 1.5
    end_time = duration - 0.99

    #Forçando valores de 0.5 em 0.5
    for i in np.arange(start_time, end_time, incremento):
        valores.append("{:.5f}".format(i))

    momentos = []
    for i in np.arange(start_time, end_time, incremento):
        momentos.append("{:.5f}".format(i))

    print(momentos)
    #for i in range(0, (len(envoltoria) - 1)):
    #    if (envoltoria[i] - anterior) > 0.15:
    #        time_value = i / taxa_amostragem
    #        if 1.5 <= time_value <= (duration - 1):
    #            valores.append("{:.5f}".format(time_value))
    #    anterior = envoltoria[i]

    print(f'Instantes no tempo com diferenças maiores de 0.15: {valores}')

    # Eliminar valores próximos
    #valores_finais = [valores[0]]
    #for valor in valores[1:]:
    #    if not any(np.isclose(float(valor), float(v), atol=0.00009) for v in valores_finais):
    #        valores_finais.append(valor)

    # Calcular a frequência instantânea a partir da fase do sinal analítico
    fase = np.unwrap(np.angle(sinal_hilbert_array))  # Desembrulhar a fase para evitar descontinuidades
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
    #plt.xlim(15, 22.5)  # Limitar o eixo y entre 0 e 2000 Hz

    plt.tight_layout()
    plt.show()
    # TODO - Fazer a transformada de hilbert ser refeita de x em x tempos
    print(len(sinal))
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

    print(len(momentos_ordenados_str))


   # Eliminar valores próximos
    momentos_final = [momentos_ordenados_str[0]]
    for valor in momentos_ordenados_str[1:]:
        if not any(np.isclose(float(valor), float(v), atol=0.00500) for v in momentos_final):
            momentos_final.append(valor)

    print(momentos_final)


    differences = []
    for i in range(1, len(momentos_final)):
        diff = "{:.5f}".format(float(momentos_final[i]) - float(momentos_final[i - 1]))
        differences.append(diff)

    print(f'Subtração entre pares de tempo: {differences}')

    elementos_uteis = []
    contador = 0
    for i in range(len(differences)):
        current_diff = float(differences[i])
        if np.isclose(current_diff, 0.500, atol=0.001):  # Checking if the element is close to 0.500
            elementos_uteis.append(current_diff)
            contador += 1
            if contador % 2 != 0:  # Make sure the counter is even
                contador += 1
        else:
            if contador % 2 ==0:
                # Checking the sum of the current element and the next element
                sum_current_next = current_diff + float(differences[i + 1]) if i + 1 < len(differences) else current_diff
                if np.isclose(sum_current_next, 0.500, atol=0.001):  # Checking if the sum is close to 0.500
                    elementos_uteis.append(current_diff)
                    contador += 1
            else:
                contador+=1


    print(elementos_uteis)

    elementos_uteis_str = [f"{valor:.{precisao}f}" for valor in elementos_uteis]
    print(elementos_uteis_str)
    excel_data = pd.read_excel(
        'nibble_ascii.xlsx')  # Replace 'path_to_your_excel_file.xlsx' with the actual path to your Excel file


    truncated_values = [float(value[:-2]) for value in elementos_uteis_str]
    print(truncated_values)

    tolerance = 0.005  # Defina a tolerância de proximidade desejada

    corresponding_values = [
        excel_data.loc[np.isclose(excel_data['Tempo'], value, atol=tolerance), 'Hertz'].values[0]
        for value in truncated_values
    ]

    # Compare the values to the corresponding column in the Excel table
    print(corresponding_values)

    # Agrupar os valores correspondentes em pares
    pairs = [(corresponding_values[i], corresponding_values[i + 1]) for i in range(0, len(corresponding_values), 2)]
    print("Pares de valores correspondentes:")
    for pair in pairs:
        print(pair)

    # Agrupar os valores correspondentes em pares
    pairs = [(corresponding_values[i], corresponding_values[i + 1]) for i in range(0, len(corresponding_values), 2)]
    decoded_text = ""
    print("Pares de valores correspondentes:")
    for pair in pairs:
        nibble_1 = pair[0]
        nibble_2 = pair[1]
        relevant_row = excel_data[(excel_data['nibble 1 (Hz)'] == nibble_1) & (excel_data['nibble 2 (Hz)'] == nibble_2)]
        if not relevant_row.empty:
            ascii_result = relevant_row['ascii'].values[0]
            print(ascii_result)
            print(type(ascii_result))
            if ascii_result == "space":
                ascii_result = " "
            decoded_text = decoded_text + str(ascii_result)

    print("Texto decodificado:", decoded_text)


demodule_wav()
