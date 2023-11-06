import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio
from scipy.io import wavfile
from css_demod import demodule_wav
from tkinter import filedialog
default_min_freq = 1000
default_max_freq = 2000
default_duration = 1.0
sample_rate = 48000
chirp_freq_step = (1000/16)

# Function to generate the tone
def generate_tone(bit_number, duration_seconds):
    min_freq = float(entry_min_freq.get())
    max_freq = float(entry_max_freq.get())
    base_freq = min_freq + (bit_number / 16) * (max_freq-min_freq)  # Updated for 4 bits
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    frequency_array = np.linspace(base_freq, base_freq + (max_freq-min_freq), len(time))

    for i in range(len(frequency_array)):
        while frequency_array[i] > max_freq:
            frequency_array[i] -= min_freq

    tone = np.sin(2 * np.pi * frequency_array * time)

    return tone, time, frequency_array


def generate_increasing_tone(duration_seconds):
    min_freq = float(entry_min_freq.get())
    max_freq = float(entry_max_freq.get())
    start_freq = min_freq
    end_freq = max_freq
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds/2))
    frequency_array = np.linspace(start_freq, end_freq, len(time))
    tone = np.sin(2 * np.pi * frequency_array * time)
    return tone, time, frequency_array

def generate_decreasing_tone(duration_seconds):
    min_freq = float(entry_min_freq.get())
    max_freq = float(entry_max_freq.get())
    start_freq = max_freq
    end_freq = min_freq
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds/2))
    frequency_array = np.linspace(start_freq, end_freq, len(time))
    tone = np.sin(2 * np.pi * frequency_array * time)
    return tone, time, frequency_array


# Function to play the tone
def play_tone(bit_number, duration_seconds):
    tone, _, _ = generate_tone(bit_number, duration_seconds)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.write(tone.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


# Function to plot the frequency over time
def plot_frequency_time(bit_number1, bit_number2, duration_seconds):
    tone1, time1, frequency_array1 = generate_tone(bit_number1, duration_seconds / 2)
    tone2, time2, frequency_array2 = generate_tone(bit_number2, duration_seconds / 2)

    plt.scatter(time1, frequency_array1, s=1, c='b', marker='.')
    plt.scatter(time2 + duration_seconds / 2, frequency_array2, s=1, c='r', marker='.')
    plt.title('Frequency x Time for Two Tones')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()
# Function to plot the continuous frequency over time for text
def plot_frequency_time_text(text, duration_seconds):
    binary_text = ' '.join(format(ord(i), '08b') for i in text)
    print(binary_text)
    binary_list = binary_text.split(' ')
    print('\n')
    print(binary_list)
    total_duration = len(binary_list) * duration_seconds

    time = np.linspace(0, total_duration, int(sample_rate * total_duration))
    frequencies = []

    current_time = 0

    for binary_num in binary_list:
        bit_number = int(binary_num, 2)
        first_half = bit_number >> 4
        second_half = bit_number & 0b1111

        tone_duration = duration_seconds / 2

        _, _, frequency_array1 = generate_tone(first_half, tone_duration)
        _, _, frequency_array2 = generate_tone(second_half, tone_duration)

        frequencies.extend(frequency_array1)
        frequencies.extend(frequency_array2)
        current_time += duration_seconds

    plt.scatter(time, frequencies, s=0.5, c='b')
    plt.title('Frequency x Time (Text) for Two Tones')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

# Function to get the input and generate the tone
def get_input():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    first_half = bit_number & 0b1111
    second_half = (bit_number >> 4) & 0b1111
    play_tone(first_half, duration_seconds / 2)
    play_tone(second_half, duration_seconds / 2)


# Function to convert string to binary and play its corresponding tone

def convert_and_play_text(output_filename="output.wav"):
    text = entry_text.get()
    duration_seconds = float(entry_duration.get())
    sync_tone, _, _ = generate_increasing_tone(duration_seconds)
    sync_tone_twice = np.concatenate((sync_tone, sync_tone))
    sync_tone_thrice= np.concatenate((sync_tone_twice, sync_tone))


    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.write(sync_tone_thrice.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()

    for char in text:
        first_half = (ord(char) >> 4) & 0b1111
        second_half = ord(char) & 0b1111
        play_tone(first_half, duration_seconds / 2)
        play_tone(second_half, duration_seconds/2)


    # Add the ending decreasing tone played twice
    end_tone, _, _ = generate_decreasing_tone(duration_seconds)
    end_tone_twice = np.concatenate((end_tone, end_tone))
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.write(end_tone_twice.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()


def gera_wav():
    output_filename = entry_filename.get() + ".wav"
    text = entry_text.get()
    duration_seconds = float(entry_duration.get())
    tones = []
    sync_tone, _, _ = generate_increasing_tone(duration_seconds)
    sync_tone_twice = np.concatenate((sync_tone, sync_tone))
    sync_tone_thrice= np.concatenate((sync_tone_twice, sync_tone))
    tones.append(sync_tone_thrice)

    for char in text:
        first_half = (ord(char) >> 4) & 0b1111
        second_half = ord(char) & 0b1111
        tone1, _, _ = generate_tone(first_half, duration_seconds/2)
        tone2, _, _ = generate_tone(second_half, duration_seconds/2)
        tones.append(tone1)
        tones.append(tone2)

    # Add the ending decreasing tone played twice
    end_tone, _, _ = generate_decreasing_tone(duration_seconds)
    end_tone_twice = np.concatenate((end_tone, end_tone))
    tones.append(end_tone_twice)

    # Concatenate all the tones into a single array
    concatenated_tones = np.concatenate(tones)

    # Convert the list to a numpy array
    tones_np = np.array(concatenated_tones)

    # Save the tones to a .wav file
    wavfile.write(output_filename, 48000, tones_np.astype(np.float32))
# Function to plot the frequency over time
def plot_freq_time():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    first_half = bit_number & 0b1111
    second_half = (bit_number >> 4) & 0b1111

    plot_frequency_time(second_half,first_half, duration_seconds)

def plot_freq_time_text():
    text = entry_text.get()
    duration_seconds = float(entry_duration.get())
    plot_frequency_time_text(text, duration_seconds)


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    demodulated_text = demodule_wav(file_path)  # Assuming demodule_wav now accepts the file path as an argument
    demod_label.config(text= "Texto Decodificado: " + demodulated_text)

# Create the UI
root = Tk()
root.title("Modulador CSS")

# Set the window size
root.geometry('800x1000')

# Add a background color
root.configure()

# Add a title label
title_label = Label(root, text="Modulador de Texto Para CSS", font=('Arial', 20, 'bold'))
title_label.pack(pady=10)

label_min_freq = Label(root, text="Insira as Frequências:")
label_min_freq.pack(pady=2)

freq_frame = Frame(root)
freq_frame.pack()

label_min = Label(freq_frame, text="Min:")
label_min.pack(side='left', padx=5, pady=2)

entry_min_freq = Entry(freq_frame, width=5, font=('arial', 12))
entry_min_freq.pack(side='left', padx=10, pady=2)

label_min = Label(freq_frame, text="Max:")
label_min.pack(side='left', padx=10, pady=2)

entry_max_freq = Entry(freq_frame, width=5, font=('arial', 12))
entry_max_freq.pack(side='left', padx=5, pady=2)


label_duration = Label(root, text="Insira a Duração (em segundos):")
label_duration.pack(pady=4)

entry_duration = Entry(root, width=5, font=('arial', 12))
entry_duration.pack(pady=2)

label = Label(root, text="Insira um Número de 8 Bits:")
label.pack(pady=4)

input_frame = Frame(root)
input_frame.pack(pady=2)

entry = Entry(input_frame, width=30, font=('arial', 12))
entry.pack(side='left')

button_tone = Button(input_frame, text="Play", command=get_input)
button_tone.pack(side='left', padx=5)

label_text = Label(root, text="Insira um Texto:")
label_text.pack(pady=4)

text_frame = Frame(root)
text_frame.pack()

entry_text = Entry(text_frame, width=60, font=('arial', 12))
entry_text.pack(side='left', pady=2)

button_text = Button(text_frame, text="Play", command=convert_and_play_text)
button_text.pack(side='left', padx=5)

label_filename = Label(root, text="Insira o nome do arquivo que deseja gerar: ")
label_filename.pack(pady=4)

entry_filename = Entry(root, width=20, font=('arial', 12))
entry_filename.pack(pady=4)

#separation_label1 = Label(root, text="Tons", font=('Arial', 14, 'bold'), bg='lightgray')
#separation_label1.pack(pady=10)

#button_tone = Button(root, text="Tom", command=get_input)
#button_tone.pack()

#button_text = Button(root, text="Tons Texto", command=convert_and_play_text)
#button_text.pack()


button_generate_wav = Button(root, text="Gerar Arquivo .wav", command = gera_wav)
button_generate_wav.pack(pady=6)

separation_label2 = Label(root, text="Gráficos", font=('Arial', 14, 'bold'))
separation_label2.pack(pady=4)

button_freq_time = Button(root, text="Gráfico Frequência x Tempo", command=plot_freq_time)
button_freq_time.pack()

button_freq_time_text = Button(root, text="Gráfico Frequência x Tempo (Texto)", command=plot_freq_time_text)
button_freq_time_text.pack(pady=4)


separation_label3 = Label(root, text="Demodulação", font=('Arial', 14, 'bold'))
separation_label3.pack(pady=4)


button_select_file = Button(root, text="Demodulação do .wav", command=select_file)
button_select_file.pack()

demod_label= Label(root, text="Texto Decodificado: ", font=('Arial', 16, 'bold'))
demod_label.pack(pady=16)


entry_min_freq.insert(0, str(default_min_freq).center(5))
entry_max_freq.insert(0, str(default_max_freq).center(5))
entry_duration.insert(0, str(default_duration).center(5))

# Adjust the appearance of the labels and buttons
label_min_freq.configure( font=('Arial', 12))
#label_max_freq.configure(background='lightgray', font=('Arial', 12))
label_duration.configure(font=('Arial', 12))
label.configure( font=('Arial', 12))
label_text.configure( font=('Arial', 12))
label_filename.configure( font=('Arial', 12))
button_generate_wav.configure( font=('Arial', 12))
button_tone.configure(background='lightblue', font=('Arial', 12))
button_freq_time.configure(background='lightblue', font=('Arial', 12))
button_text.configure(background='lightblue', font=('Arial', 12))
button_freq_time_text.configure(background='lightblue', font=('Arial', 12))
button_select_file.configure(background='lightgrey', font=('Arial', 12))
button_generate_wav.configure(background='lightgrey', font=('Arial', 12))

root.mainloop()