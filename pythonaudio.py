import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


def generate_tone():
    # Get the values from the entry fields
    total_duration = float(total_duration_entry.get())
    tone_duration = float(tone_duration_entry.get())
    frequency_start = float(frequency_start_entry.get())
    frequency_end = float(frequency_end_entry.get())

    # Calculate the number of tone repetitions
    num_repetitions = int(total_duration / tone_duration)

    # Generate the time axis for each repetition
    t_repetition = np.linspace(0, tone_duration, int(tone_duration * sampling_rate), endpoint=False)

    # Generate the frequency axis for each repetition
    frequency_repetition = np.linspace(frequency_start, frequency_end, len(t_repetition))

    # Generate the audio signal for each repetition
    signal_repetition = np.sin(2 * np.pi * frequency_repetition * t_repetition)

    # Normalize the signal for each repetition
    signal_repetition /= np.max(np.abs(signal_repetition))

    # Concatenate the repetitions to create the full audio signal
    signal = np.tile(signal_repetition, num_repetitions)

    return signal


def play_audio():
    signal = generate_tone()

    # Play the audio signal
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sampling_rate,
                    output=True)

    stream.write(signal.astype(np.float32).tostring())

    stream.stop_stream()
    stream.close()

    p.terminate()


def plot_graph():
    signal = generate_tone()

    # Compute the spectrogram
    spec, freqs, t, im = plt.specgram(signal, NFFT=1024, Fs=sampling_rate, noverlap=512, cmap='jet')

    # Set the axis labels
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    # Calculate the adjusted y-axis limits
    frequency_start = float(frequency_start_entry.get())
    frequency_end = float(frequency_end_entry.get())
    y_min = max(frequency_start - 1000, freqs[0])
    y_max = min(frequency_end + 1000, freqs[-1])
    plt.ylim(y_min, y_max)

    # Set the colorbar
    plt.colorbar()

    # Display the plot
    plt.show()

# Parameters
sampling_rate = 44100  # Number of samples per second

# Create the main window
window = tk.Tk()
window.title("Tone Generator")

# Create the entry fields
total_duration_label = tk.Label(window, text="Total Duration (seconds):")
total_duration_label.pack()
total_duration_entry = tk.Entry(window)
total_duration_entry.pack()

tone_duration_label = tk.Label(window, text="Tone Duration (seconds):")
tone_duration_label.pack()
tone_duration_entry = tk.Entry(window)
tone_duration_entry.pack()

frequency_start_label = tk.Label(window, text="Frequency Start (Hz):")
frequency_start_label.pack()
frequency_start_entry = tk.Entry(window)
frequency_start_entry.pack()

frequency_end_label = tk.Label(window, text="Frequency End (Hz):")
frequency_end_label.pack()
frequency_end_entry = tk.Entry(window)
frequency_end_entry.pack()


# Create the buttons
play_button = tk.Button(window, text="Play Audio", command=play_audio)
play_button.pack()

plot_button = tk.Button(window, text="Plot Graph", command=plot_graph)
plot_button.pack()


# Run the main window loop
window.mainloop()
