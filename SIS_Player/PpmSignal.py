import numpy as np
from sklearn.preprocessing import minmax_scale


class PpmSignal:
    def __init__(self):
        self.data = []
        self.rate = 50

    # Generates signal represented by the 8 inputs (normalized between -1 and 1)
    # In drone control, axes represent: roll, pitch, yaw, throttle, aux1, aux2, aux3, aux4
    def axis_to_signal(self, ax1=0, ax2=0, ax3=0, ax4=0, ax5=0, ax6=0, ax7=0, ax8=0):
        signal = np.array([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8])
        signal = minmax_scale(signal, feature_range=(1, 2))

        # TODO Insert no data sections correctly

        time = 0
        for a in signal:
            time += a

        time += 0.3 * 8

        time_array = np.linspace(0, time, num=int(time*self.rate))

        data_array = []

        for a in signal:
            data_array += np.zeros(int(a * self.rate)).tolist()
            data_array += np.ones(int(0.3 * self.rate)).tolist()

        print(data_array)
        print(time_array)
        print(len(time_array))
        print(len(data_array))
        print(signal)
        return signal

    # Appends generated signal to data with correct modulation
    # Signal contains 8 numbers representing length of each PPM section
    def append_to_data(self, signal):
        pass
