import argparse
import pydub
import os
import matplotlib.pyplot as plt
from scipy import fftpack
import numpy as np

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description="Sound analysis")
    parser.add_argument("-f", type=str, metavar="file", help="input sound file", required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.f):
        print("Error! Given sound file does not exist!")

    # Load file
    sound = pydub.AudioSegment.from_file(args.f)
    sound_samples = sound.get_array_of_samples()
    print("Loaded file {}\n".format(args.f))

    # STFT arguments
    NFFT = 192             # The number of data points used in each block for the FFT. A power 2 is most efficient.
    Fs = sound.frame_rate  # The sampling frequency (samples per time unit).
    Overlap = NFFT / 8     # The number of points of overlap between blocks.

    # Optimal length for stft to calculate quickly (divide and conquer algorithm)
    good_size = fftpack.helper.next_fast_len(NFFT)

    # spectrum - 2d array: Columns are the periodograms of successive segments
    # freq - 1d array:  The frequencies corresponding to the rows in spectrum
    # bins - 1d array:  The times corresponding to midpoints of segments (i.e., the columns in spectrum)
    # im   - AxesImage: The image created by imshow containing the spectrogram
    spectrum, freqs, bins, im = plt.specgram(
        sound_samples, NFFT=NFFT, Fs=Fs, pad_to=good_size, noverlap=Overlap, cmap=plt.cm.get_cmap('magma'))

    # Calculate time accuracy
    time_step = bins[0] * 2
    # Calculate freq accuracy
    freq_step = freqs[1]

    # Get the freq of the 2 beeps
    freq_one = int(2000 / freq_step)
    freq_two = int(3000 / freq_step)

    # Set threshold of beep
    threshold = 0.5

    # Normalize values for freq_one and freq_two
    freq_one_norm = np.array(spectrum[freq_one] / max(spectrum[freq_one]), dtype=np.float32)
    freq_two_norm = np.array(spectrum[freq_two] / max(spectrum[freq_two]), dtype=np.float32)

    # Get frequency timestamps
    freq_one_timestamps = []
    freq_two_timestamps = []
    freq_one_state = False
    freq_two_state = False
    for i in range(0, len(bins)):
        if freq_one_norm[i] > threshold and not freq_one_state:
            freq_one_timestamps.append(i)
            freq_one_state = not freq_one_state
        elif freq_one_norm[i] < threshold and freq_one_state:
            freq_one_timestamps.append(i)
            freq_one_state = not freq_one_state

        if freq_two_norm[i] > threshold and not freq_two_state:
            freq_two_timestamps.append(i)
            freq_two_state = not freq_two_state
        elif freq_two_norm[i] < threshold and freq_two_state:
            freq_two_timestamps.append(i)
            freq_two_state = not freq_two_state

    # Print result
    print("Completed STFT\nTime accuracy: {}\nFq accuracy: {}\n".format(time_step, freq_step))

    a = max(freq_one_norm)
    b = max(freq_two_norm)

    # Draw graph
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.show()
