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
    duration=len(envoltoria)/taxa_amostragem
    print(duration)
    anterior = envoltoria[0]
    valores = []

    for i in range(0, (len(envoltoria) - 1)):
        if (envoltoria[i] - anterior) > 0.15:
            time_value = i / taxa_amostragem
            if 1.5 <= time_value <= (duration - 1):
                valores.append("{:.5f}".format(time_value))
        anterior = envoltoria[i]

    print(f'Instantes no tempo com diferenças maiores de 0.15: {valores}')

    # Eliminar valores próximos
    valores_finais = [valores[0]]
    for valor in valores[1:]:
        if not any(np.isclose(float(valor), float(v), atol=0.00009) for v in valores_finais):
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

    print(f'Retirada de duplicatas: {valores_finais}')


    differences = []
    for i in range(1, len(valores_finais)):
        diff = "{:.5f}".format(float(valores_finais[i]) - float(valores_finais[i - 1]))
        differences.append(diff)

    print(f'Subtração entre pares de tempo: {differences}')

    # filtro das diferenças para eliminar valores maior do que 0.5

    #filtered_differences = [diff for diff in differences if float(diff) <= 0.5]
    # seleção de valores que não seriam os sync chirps ou down chirps
    # mas isso já está sendo resolvido na hora de gerar o vetor inicial
    '''
    middle_values = filtered_differences[3:-1]  # Selecting values from index 3 to the second-to-last element
    print(middle_values)
    middle_values = differences[3:-1]  # Selecting values from index 3 to the second-to-last element
    print(middle_values)
    '''

    # Pega apenas os valores que estão em índices pares, a fim de pular os termos complementares
    even_values = [differences[i] for i in range(len(differences)) if i % 2 == 0]

    print(f'Complementares retirados: {even_values}')

    excel_data = pd.read_excel(
        'nibble_ascii.xlsx')  # Replace 'path_to_your_excel_file.xlsx' with the actual path to your Excel file

    # Extract the values from 'even_values' for comparison
    truncated_values = [float(value[:-2]) for value in even_values]

    corresponding_values = [
        excel_data.loc[excel_data['Tempo'] == value, 'Hertz'].values[0] for value in
        truncated_values]

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
            if ascii_result=="space":
                ascii_result = " "
            decoded_text = decoded_text + ascii_result


    print("Texto decodificado:", decoded_text)

demodule_wav()
