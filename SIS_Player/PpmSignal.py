
class PpmSignal:
    def __init__(self):
        data = []
        pass

    # Transforms 4 doubles representing axis input of controller to 8 doubles representing length of correct channel
    def axis_to_signal(self, roll, pitch, yaw, throttle):
        pass

    # Generates signal represented by the 8 inputs
    def to_signal(self, c1, c2, c3, c4, c5, c6, c7, c8):
        pass

    # Appends generated signal to data with correct modulation
    def append_to_data(self, signal):
        pass
