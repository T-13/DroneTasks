import sys
import os
import argparse
from pydub import AudioSegment, exceptions
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack, constants


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Frequency-Time Sound Analysis")
    parser.add_argument("-f", type=str, metavar="file", help="input sound file", required=True)
    parser.add_argument("-t", type=float, default=0.003, metavar="threshold",
                        help="amplitude threshold (default: 0.003)", required=False)
    parser.add_argument("-f1", type=int, default=2000, metavar="frequency 1",
                        help="frequency of 1. beep (default: 2000)", required=False)
    parser.add_argument("-f2", type=int, default=3000, metavar="frequency 2",
                        help="frequency of 2. beep (default: 3000)", required=False)
    args = parser.parse_args()

    file, threshold, freq_one, freq_two = args.f, args.t, args.f1, args.f2

    # Verify sound file exists
    if not os.path.isfile(file):
        print("Error! Given sound file does not exist!")
        return 1

    # Load file
    try:
        sound = AudioSegment.from_file(file)
        sound_samples = sound.get_array_of_samples()
    except exceptions.CouldntDecodeError:
        print("Failed to load sound!")
        return 1
    else:
        print("Loaded file {}\n".format(file))

    # Prepare graph axes
    fig, axes = plt.subplots(5, sharex=True)

    # STFT arguments
    NFFT = 192             # Number of data points used in each block for the FFT (power 2 is most efficient)
    Fs = sound.frame_rate  # Sampling frequency (samples per time unit)
    Overlap = NFFT / 4     # Number of points of overlap between blocks

    # Optimal length for stft to calculate quickly (divide and conquer algorithm)
    good_size = fftpack.helper.next_fast_len(NFFT)

    # spectrum - 2d array:  Columns are the periodograms of successive segments
    # freq     - 1d array:  Frequencies corresponding to the rows in spectrum
    # bins     - 1d array:  Times corresponding to midpoints of segments (the columns in spectrum)
    # _im      - AxesImage: Image created by imshow containing the spectrogram
    spectrum, freqs, bins, _ = axes[0].specgram(
        sound_samples, NFFT=NFFT, Fs=Fs, pad_to=good_size, noverlap=Overlap, cmap=plt.cm.get_cmap('magma'))

    # Calculate time and frequency accuracy
    time_step = bins[0] * 2  # bins contains midpoints
    freq_step = freqs[1]

    # Get the index of frequencies of the 2 beeps in our spectrum
    freq_one_i = int(round(freq_one / freq_step))
    freq_two_i = int(round(freq_two / freq_step))

    # Normalize values
    freq_one_norm = np.array(spectrum[freq_one_i] / max(spectrum[freq_one_i]))
    freq_two_norm = np.array(spectrum[freq_two_i] / max(spectrum[freq_two_i]))

    # Filter normalized values
    freq_one_norm_filt = np.convolve(freq_one_norm, np.ones((30,)) / 30, mode='same')
    freq_two_norm_filt = np.convolve(freq_two_norm, np.ones((30,)) / 30, mode='same')

    # Binarize the filtered output
    freq_one_bin, freq_two_bin = [], []
    for i in range(0, len(bins)):
        b = 1 if freq_one_norm_filt[i] > threshold else 0
        freq_one_bin.append(b)

        b = 1 if freq_two_norm_filt[i] > threshold else 0
        freq_two_bin.append(b)

    # Get timestamps from binarized output
    freq_one_timestamps, freq_two_timestamps = [], []
    freq_one_state, freq_two_state = False, False
    bins_one_i = []
    for i in range(0, len(bins)):
        if (freq_one_bin[i] == 1 and not freq_one_state) or (freq_one_bin[i] == 0 and freq_one_state):
            freq_one_timestamps.append(bins[i])
            bins_one_i.append(i)
            freq_one_state = not freq_one_state

        if (freq_two_bin[i] == 1 and not freq_two_state) or (freq_two_bin[i] == 0 and freq_two_state):
            freq_two_timestamps.append(bins[i])
            freq_two_state = not freq_two_state

    # Calculate offsets from middle
    offsets = []
    offsets_all = np.zeros(bins_one_i[0])
    for i in range(0, len(freq_one_timestamps)):
        time_dif = freq_one_timestamps[i] - freq_two_timestamps[i]
        offsets.append(time_dif * constants.speed_of_sound)
        if i % 2 != 0:
            middle = np.linspace(offsets[i - 1], offsets[i], bins_one_i[i] - len(offsets_all))
            offsets_all = np.append(offsets_all, middle)
    offsets_all = np.append(offsets_all, np.zeros(len(bins) - len(offsets_all)))

    # Normalize to account for errors
    offsets_all = np.array(offsets_all / (2 * max(offsets_all)))

    # Print results
    print("Completed STFT:")
    print("- Time accuracy: {} s".format(time_step))
    print("- Frequency accuracy: {} Hz\n".format(freq_step))

    print("Frequency 1:")
    print("- Approximation: {} Hz".format(freqs[freq_one_i]))
    print("- Start times (s): {}".format(freq_one_timestamps[0::2]))
    print("- End times (s): {}\n".format(freq_one_timestamps[1::2]))

    print("Frequency 2:")
    print("- Approximation: {} Hz".format(freqs[freq_two_i]))
    print("- Start times (s): {}".format(freq_two_timestamps[0::2]))
    print("- End times (s): {}\n".format(freq_two_timestamps[1::2]))

    print("Offset approximations (0 - middle, <0 - left, >0 - right):")
    print("- Smallest error: {} m".format(time_step * constants.speed_of_sound))
    print("- Approximations (m): {}".format(offsets))

    # Draw graphs
    plt.suptitle("Sound Analysis\nSpectrogram - Normalized - Filtered - Binarized - Distance")
    axes[0].set_ylabel("Freq (Hz)")

    axes[1].plot(bins, freq_one_norm)
    axes[1].plot(bins, freq_two_norm)

    axes[2].plot(bins, freq_one_norm_filt)
    axes[2].plot(bins, freq_two_norm_filt)

    axes[3].plot(bins, freq_one_bin)
    axes[3].plot(bins, freq_two_bin)

    axes[4].plot(bins, offsets_all, color="k")
    axes[4].set_ylabel("Dist (m)")

    axes[2].set_ylabel("Amplitude")  # All but first plot share y label
    axes[4].set_xlabel("Time (s)")  # All plots display time on x axis
    fig.subplots_adjust(hspace=0.1)  # Bring subplots close to each other
    [ax.label_outer() for ax in axes]  # Hide x labels and ticks for all but buttom plot
    axes[1].legend(["{} Hz".format(freq_one), "{} Hz".format(freq_two)])  # Create legend on first frequencies graph

    plt.show()


if __name__ == "__main__":
    sys.exit(main())
