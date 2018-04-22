import numpy as np


class PpmSignal:
    def __init__(self):
        self.data = []

    # Generates signal represented by the 8 inputs (normalized between -1 and 1)
    # In drone control, axes represent: roll, pitch, yaw, throttle, aux1, aux2, aux3, aux4
    def axis_to_signal(self, ax1=0, ax2=0, ax3=0, ax4=0, ax5=0, ax6=0, ax7=0, ax8=0):
        signal = np.array([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8])

        # TODO Insert no data sections correctly

        return signal

    # Appends generated signal to data with correct modulation
    # Signal contains 8 numbers representing length of each PPM section
    def append_to_data(self, signal):
        duration = 22.5
        frequency = 50
        originalNumberOfElements = duration * frequency
        numberOfElements = len(signal)
        number = originalNumberOfElements - numberOfElements
        signal += [1] * number
        return signal
