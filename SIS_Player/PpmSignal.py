import math
import numpy as np


class PpmSignal:
    def __init__(self):
        self.rate = 50
        self.pulse_duration = 22.5
        self.duration = 2

        self.data = np.ones(100).tolist()  # Start 2ms

    # Generates signal represented by the 8 inputs (normalized between 1 and 2)
    # In drone control, axes represent: roll, pitch, yaw, throttle, aux1, aux2, aux3, aux4
    def axis_to_signal(self, ax1=1.5, ax2=1.5, ax3=1.5, ax4=1.5, ax5=1.5, ax6=1.5, ax7=1.5, ax8=1.5):
        signal = np.array([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8])

        # Insert "no data" sections correctly
        data_array = []
        for a in signal:
            data_array += np.zeros(int(a * self.rate)).tolist()
            data_array += np.ones(int(0.3 * self.rate)).tolist()

        self.append_to_data(data_array)

    # Appends generated signal to data with correct modulation
    # Signal contains 8 numbers representing length of each PPM section
    def append_to_data(self, signal):
        originalNumberOfElements = self.pulse_duration * self.rate
        number = originalNumberOfElements - len(signal)
        self.data += signal + np.ones(int(number)).tolist()
        self.duration += self.pulse_duration

    def get_data(self):
        return np.multiply(self.data, math.pow(2, 15) - 1)
