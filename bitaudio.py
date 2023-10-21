'''import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio

# Function to generate the Chirp Spread Spectrum (CSS) signal
def generate_css(bit_number, duration_seconds):
    base_freq = 1000 + (bit_number / 16) * 1000
    sample_rate = 44100
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    chirp_rate = 1000  # Chirp rate in Hz per second

    css_signal = np.sin(2 * np.pi * (base_freq * time + 0.5 * chirp_rate * time ** 2))

    return css_signal, time

# Function to play the CSS signal
def play_css(bit_number, duration_seconds):
    css_signal, _ = generate_css(bit_number, duration_seconds)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    stream.write(css_signal.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to plot the CSS signal
def plot_waterfall_css(bit_number, duration_seconds):
    css_signal, _ = generate_css(bit_number, duration_seconds)

    plt.specgram(css_signal, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Chirp Spread Spectrum Signal')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()


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
def play_tone(bit_number, duration_seconds, css_modulation=False):
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
def plot_waterfall(bit_number, duration_seconds, css_modulation=False):
    tone, time, _ = generate_tone(bit_number, duration_seconds)

    plt.specgram(tone, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Frequency over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

# Function to plot the frequency over time
def plot_frequency_time(bit_number, duration_seconds, css_modulation=False):
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

def modulate_css():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    play_css(bit_number, duration_seconds)
    plot_waterfall_css(bit_number, duration_seconds)

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

# Create the new button for CSS modulation
button_css = Button(root, text="Modulate to CSS", command=modulate_css)
button_css.pack()

root.mainloop()
'''

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio

# Function to generate the Chirp Spread Spectrum (CSS) signal
def generate_css(bit_number, duration_seconds):
    base_freq = 1000 + (bit_number / 16) * 1000
    sample_rate = 44100
    time = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    chirp_rate = 1000  # Chirp rate in Hz per second

    css_signal = np.sin(2 * np.pi * (base_freq * time + 0.5 * chirp_rate * time ** 2))

    return css_signal, time

# Function to play the CSS signal
def play_css(bit_number, duration_seconds):
    css_signal, _ = generate_css(bit_number, duration_seconds)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    stream.write(css_signal.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to plot the CSS signal
def plot_waterfall_css(bit_number, duration_seconds):
    css_signal, _ = generate_css(bit_number, duration_seconds)

    plt.specgram(css_signal, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Chirp Spread Spectrum Signal')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()


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
def play_tone(bit_number, duration_seconds, css_modulation=False):
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
def plot_waterfall(bit_number, duration_seconds, css_modulation=False):
    tone, time, _ = generate_tone(bit_number, duration_seconds)

    plt.specgram(tone, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Frequency over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

# Function to plot the frequency over time
def plot_frequency_time(bit_number, duration_seconds, css_modulation=False):
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

def modulate_css():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    play_css(bit_number, duration_seconds)
    plot_waterfall_css(bit_number, duration_seconds)

# Function to get the input sequence and generate the concatenated CSS modulated signal
def get_sequence():
    sequence = entry_sequence.get()
    if len(sequence) == 12:
        concatenated_signal = np.array([])
        for i in range(0, len(sequence), 4):
            bit_number = int(sequence[i:i+4], 2)
            css_signal, _ = generate_css(bit_number, 1)
            if i == 0:
                concatenated_signal = css_signal
            else:
                concatenated_signal = np.concatenate((concatenated_signal, css_signal), axis=None)
        play_concatenated_signal(concatenated_signal)
        plot_waterfall_concatenated(concatenated_signal)
    else:
        print("Please enter a valid sequence of 3 four-bit numbers.")

# Function to play the concatenated CSS modulated signal
def play_concatenated_signal(concatenated_signal):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)
    stream.write(concatenated_signal.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def plot_waterfall_concatenated(concatenated_signal):
    plt.specgram(concatenated_signal, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Concatenated CSS Modulated Signal')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

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

# Create the new button for CSS modulation
button_css = Button(root, text="Modulate to CSS", command=modulate_css)
button_css.pack()

# Add a label and entry for the sequence of 4-bit numbers
label_sequence = Label(root, text="Enter 3 four-bit numbers sequence:")
label_sequence.pack()

entry_sequence = Entry(root, width=20)
entry_sequence.pack()

# Add a button to modulate the sequence to CSS, concatenate, play, and plot the concatenated signal
button_modulate_sequence = Button(root, text="Modulate Sequence to CSS", command=get_sequence)
button_modulate_sequence.pack()

root.mainloop()
