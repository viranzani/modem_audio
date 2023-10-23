'''import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio



# Function to generate the tone
def generate_tone(bit_number, duration_seconds):
    base_freq = 1000 + (bit_number / 16) * 1000
    sample_rate = 44100
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    frequency_array = np.linspace(base_freq, base_freq + 1000, len(time))

    for i in range(len(frequency_array)):
        while frequency_array[i] > 2000:
            frequency_array[i] -= 1000

    tone = np.sin(2 * np.pi * frequency_array * time)

    return tone, time, frequency_array

# Function to apply CSS modulation

# Function to play the tone
def play_tone(bit_number, duration_seconds):
    tone, _, _ = generate_tone(bit_number, duration_seconds)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    stream.write(tone.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to plot the waterfall plot
def plot_waterfall(bit_number, duration_seconds):
    tone, time, _ = generate_tone(bit_number, duration_seconds)

    plt.specgram(tone, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Frequency over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

# Function to plot the frequency over time
def plot_frequency_time(bit_number, duration_seconds):
    _, time, frequency_array = generate_tone(bit_number, duration_seconds)

    plt.plot(time, frequency_array)
    plt.title('Frequency over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()


# Function to get the input and generate the tone
def get_input():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    play_tone(bit_number, duration_seconds)

# Function to plot the waterfall plot
def plot():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    plot_waterfall(bit_number, duration_seconds)


# Function to plot the frequency over time
def plot_freq_time():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    plot_frequency_time(bit_number, duration_seconds)

# Create the UI
root = Tk()
root.title("Tone Generator")

label = Label(root, text="Enter 4-bit number:")
label.pack()

entry = Entry(root, width=10)
entry.pack()

label_duration = Label(root, text="Enter duration (in seconds):")
label_duration.pack()

entry_duration = Entry(root, width=10)
entry_duration.pack()

button_tone = Button(root, text="Play Tone", command=get_input)
button_tone.pack()

button_plot = Button(root, text="Plot Waterfall", command=plot)
button_plot.pack()

button_freq_time = Button(root, text="Plot Frequency over Time", command=plot_freq_time)
button_freq_time.pack()



root.mainloop()
'''
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio

default_min_freq = 1000
default_max_freq = 2000
default_duration = 1.0

# Function to generate the tone
def generate_tone(bit_number, duration_seconds):
    min_freq = float(entry_min_freq.get())
    max_freq = float(entry_max_freq.get())
    base_freq = min_freq + (bit_number / 256) * (max_freq-min_freq)  # Updated for 8 bits
    sample_rate = 44100
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    frequency_array = np.linspace(base_freq, base_freq + 1000, len(time))

    for i in range(len(frequency_array)):
        while frequency_array[i] > max_freq:
            frequency_array[i] -= min_freq

    tone = np.sin(2 * np.pi * frequency_array * time)

    return tone, time, frequency_array

def generate_decreasing_tone(duration_seconds):
    min_freq = float(entry_min_freq.get())
    max_freq = float(entry_max_freq.get())
    start_freq = max_freq
    end_freq = min_freq
    sample_rate = 44100
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    frequency_array = np.linspace(start_freq, end_freq, len(time))
    tone = np.sin(2 * np.pi * frequency_array * time)
    return tone, time, frequency_array

# Function to play the tone
def play_tone(bit_number, duration_seconds):
    tone, _, _ = generate_tone(bit_number, duration_seconds)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    stream.write(tone.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


# Function to plot the waterfall plot
def plot_waterfall(bit_number, duration_seconds):
    tone, time, _ = generate_tone(bit_number, duration_seconds)

    plt.specgram(tone, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Plot Waterfall')
    plt.xlabel('Tempo')
    plt.ylabel('Frequência')
    plt.show()


# Function to plot the frequency over time
def plot_frequency_time(bit_number, duration_seconds):
    _, time, frequency_array = generate_tone(bit_number, duration_seconds)

    plt.scatter(time, frequency_array, s=1, c='b', marker='.')
    plt.title('Frequência x Tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Frequência')
    plt.show()

# Function to plot the continuous frequency over time for text
def plot_frequency_time_text(text, duration_seconds):
    binary_text = ' '.join(format(ord(i), '08b') for i in text)
    binary_list = binary_text.split(' ')
    total_duration = len(binary_list) * duration_seconds

    time = np.linspace(0, total_duration, int(44100 * total_duration))
    frequencies = []

    current_time = 0

    for binary_num in binary_list:
        bit_number = int(binary_num, 2)
        tone_duration = duration_seconds
        _, _, frequency_array = generate_tone(bit_number, tone_duration)
        frequencies.extend(frequency_array)
        current_time += duration_seconds

    plt.scatter(time, frequencies, s=0.5, c='b', marker='.')
    plt.title('Frequência x Tempo (Texto)')
    plt.xlabel('Tempo')
    plt.ylabel('Frequência')
    plt.show()

# Function to get the input and generate the tone
def get_input():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    play_tone(bit_number, duration_seconds)


# Function to convert string to binary and play its corresponding tone
def convert_and_play():
    word = entry_word.get()
    duration_seconds = float(entry_duration.get())

    binary = ' '.join(format(ord(i), '08b') for i in word)
    binary_list = binary.split(' ')

    for binary_num in binary_list:
        bit_number = int(binary_num, 2)
        play_tone(bit_number, duration_seconds)

def convert_and_play_text():
    text = entry_text.get()
    duration_seconds = float(entry_duration.get())

    binary_text = ' '.join(format(ord(i), '08b') for i in text)
    binary_list = binary_text.split(' ')

    for binary_num in binary_list:
        bit_number = int(binary_num, 2)
        play_tone(bit_number, duration_seconds)

    # Add the ending decreasing tone played twice
    end_tone, _, _ = generate_decreasing_tone(duration_seconds)
    end_tone_twice = np.concatenate((end_tone, end_tone))
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)
    stream.write(end_tone_twice.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to generate tones for a sequence of 8-bit values
def generate_sequence():
    sequence = entry_sequence.get().split(',')
    duration_seconds = float(entry_duration.get())
    for seq in sequence:
        bit_number = int(seq, 2)
        play_tone(bit_number, duration_seconds)

# Function to plot the frequency over time
def plot_freq_time():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    plot_frequency_time(bit_number, duration_seconds)

def plot_freq_time_text():
    text = entry_text.get()
    duration_seconds = float(entry_duration.get())
    plot_frequency_time_text(text, duration_seconds)
# Create the UI
root = Tk()
root.title("Modulador CSS")

# Set the window size
root.geometry('600x720')

# Add a background color
root.configure(background='lightgray')

# Add a title label
title_label = Label(root, text="Modulador de Texto Para CSS", font=('Arial', 20, 'bold'), bg='lightgray')
title_label.pack(pady=10)

label_min_freq = Label(root, text="Insira a Frequência Mínima:")
label_min_freq.pack()

entry_min_freq = Entry(root, width=10, font=('arial', 12))
entry_min_freq.pack()

label_max_freq = Label(root, text="Insira a Frequência Máxima:")
label_max_freq.pack()

entry_max_freq = Entry(root, width=10, font=('arial', 12))
entry_max_freq.pack()

label_duration = Label(root, text="Insira a Duração (em segundos):")
label_duration.pack()

entry_duration = Entry(root, width=10, font=('arial', 12))
entry_duration.pack()

label = Label(root, text="Insira um Número de 8 Bits:")
label.pack()

entry = Entry(root, width=30, font=('arial', 12))
entry.pack()

label_sequence = Label(root, text="Insira uma Sequência de Números de 8 Bits Separados por Vírgula:")
label_sequence.pack()

entry_sequence = Entry(root, width=30, font=('arial', 12))
entry_sequence.pack()

label_word = Label(root, text="Insira uma Palavra:")
label_word.pack()

entry_word = Entry(root, width=30, font=('arial', 12))
entry_word.pack()

label_text = Label(root, text="Insira um Texto:")
label_text.pack()

entry_text = Entry(root, width=60, font=('arial', 12))
entry_text.pack()

# Add a title label
separation_label1 = Label(root, text="Tons", font=('Arial', 14, 'bold'), bg='lightgray')
separation_label1.pack(pady=10)

button_tone = Button(root, text="Tom", command=get_input)
button_tone.pack()

button_sequence = Button(root, text="Sequência de Tons", command=generate_sequence)
button_sequence.pack()

button_word = Button(root, text="Tons Palavra", command=convert_and_play)
button_word.pack()

button_text = Button(root, text="Tons Texto", command=convert_and_play_text)
button_text.pack()

# Add a title label
separation_label2 = Label(root, text="Gráficos", font=('Arial', 14, 'bold'), bg='lightgray')
separation_label2.pack(pady=10)

button_plot = Button(root, text="Gráfico Waterfall", command=plot_waterfall)
button_plot.pack()

button_freq_time = Button(root, text="Gráfico Frequência x Tempo", command=plot_freq_time)
button_freq_time.pack()


button_freq_time_text = Button(root, text="Gráfico Frequência x Tempo (Texto)", command=plot_freq_time_text)
button_freq_time_text.pack()

entry_min_freq.insert(0, str(default_min_freq))
entry_max_freq.insert(0, str(default_max_freq))
entry_duration.insert(0, str(default_duration))

# Adjust the appearance of the labels and buttons
label_min_freq.configure(background='lightgray', font=('Arial', 12))
label_max_freq.configure(background='lightgray', font=('Arial', 12))
label_duration.configure(background='lightgray', font=('Arial', 12))
label.configure(background='lightgray', font=('Arial', 12))
label_sequence.configure(background='lightgray', font=('Arial', 12))
label_word.configure(background='lightgray', font=('Arial', 12))
label_text.configure(background='lightgray', font=('Arial', 12))

button_tone.configure(background='lightblue', font=('Arial', 12))
button_sequence.configure(background='lightgreen', font=('Arial', 12))
button_word.configure(background='lightcoral', font=('Arial', 12))
button_plot.configure(background='lightgoldenrodyellow', font=('Arial', 12))
button_freq_time.configure(background='lightpink', font=('Arial', 12))
button_text.configure(background='lightcyan', font=('Arial', 12))
button_freq_time_text.configure(background='lightseagreen', font=('Arial', 12))


root.mainloop()
