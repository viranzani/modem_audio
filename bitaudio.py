'''
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Parameters
sampling_rate = 44100  # Number of samples per second

# Create the main window
window = tk.Tk()
window.title("Bit to Frequency Converter")

# Create the entry fields
total_duration_label = tk.Label(window, text="Total Duration (seconds):")
total_duration_label.pack()
total_duration_entry = tk.Entry(window)
total_duration_entry.pack()

bit_sequence_label = tk.Label(window, text="Enter 4-bit sequence:")
bit_sequence_label.pack()
bit_sequence_entry = tk.Entry(window)
bit_sequence_entry.pack()

def generate_bit_signal(total_duration):
    bit_sequence = bit_sequence_entry.get()

    # Check if the bit sequence is valid
    if len(bit_sequence) != 4 or not all(bit in ['0', '1'] for bit in bit_sequence):
        messagebox.showerror("Error", "Invalid bit sequence. Please enter a valid 4-bit sequence.")
        return

    initial_frequency = 1000 + int(bit_sequence, 2) * (1000 / 16)
    final_frequency = initial_frequency + 1000

    tone_duration = total_duration / 2
    num_samples = int(sampling_rate * tone_duration)
    t = np.linspace(0, tone_duration, num_samples, endpoint=False)

    # Use a chirp function to create a smoothly varying frequency signal
    frequency_signal = np.sin(2 * np.pi * np.linspace(initial_frequency, final_frequency, num_samples) * t)

    return frequency_signal
def play_bit_audio():
    total_duration = float(total_duration_entry.get())
    signal = generate_bit_signal(total_duration)

    if signal is not None:
        # Play the audio signal
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sampling_rate,
                        output=True)

        stream.write(signal.astype(np.float32).tobytes())

        stream.stop_stream()
        stream.close()

        p.terminate()


def plot_bit_graph():
    total_duration = float(total_duration_entry.get())
    signal = generate_bit_signal(total_duration)

    if signal is not None:
        # Compute the spectrogram
        spec, freqs, t, im = plt.specgram(signal, NFFT=1024, Fs=sampling_rate, noverlap=512, cmap='jet')

        # Set the axis labels
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        # Adjust the y-axis limits
        plt.ylim(0, 3300)  # Adjust these values to focus on the range of frequencies used

        # Set the colorbar
        plt.colorbar()

        # Display the plot
        plt.show()


# Create the buttons
play_button = tk.Button(window, text="Play Bit Audio", command=play_bit_audio)
play_button.pack()

plot_button = tk.Button(window, text="Plot Bit Graph", command=plot_bit_graph)
plot_button.pack()

# Run the main window loop
window.mainloop()
'''
import numpy as np
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

    return tone, time

# Function to play the tone
def play_tone(bit_number, duration_seconds):
    tone, _ = generate_tone(bit_number, duration_seconds)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    stream.write(tone.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to plot the signal
def plot_waterfall(bit_number, duration_seconds):
    tone, time = generate_tone(bit_number, duration_seconds)
    plt.specgram(tone, Fs=44100, NFFT=1024, noverlap=900, cmap='viridis')
    plt.title('Waterfall Plot of Frequency over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

# Create the UI
root = Tk()
root.title("Tone Generator")

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

root.mainloop()
def get_input():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    play_tone(bit_number, duration_seconds)

# Function to plot the waterfall plot
def plot():
    bit_number = int(entry.get(), 2)
    duration_seconds = float(entry_duration.get())
    plot_waterfall(bit_number, duration_seconds)
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

root.mainloop()
