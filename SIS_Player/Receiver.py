from inputs import get_gamepad
from threading import Thread, Event
from time import sleep
from PpmSignal import PpmSignal



class Receiver:

    def __init__(self, parent):
        self.recording_signal = Event()
        self.send_delay = 0.0225
        self.parent = parent

        self.signal = PpmSignal()

        self.create_threads()

        # Axis values
        self.roll = 1.5
        self.pitch = 1.5
        self.yaw = 1.5
        self.throttle = 1.5

    # Starts recording inputs async
    def get_inputs(self):
        self.recording_signal.set()
        self.create_threads()
        self.recording_Thread.start()
        self.sending_Thread.start()

    # Function that will run async and will record controller state
    def recording_function(self):
        while self.recording_signal.is_set():
            events = get_gamepad()
            for event in events:
                if event.code == "ABS_X":
                    self.roll = (event.state / (32767*2)) + 1.5
                elif event.code == "ABS_Y":
                    self.pitch = (event.state / (32767 * 2)) + 1.5
                elif event.code == "ABS_RX":
                    self.yaw = (event.state / (32767 * 2)) + 1.5
                elif event.code == "ABS_RY":
                    self.throttle = (event.state / (32767 * 2)) + 1.5

    # Function that will sen controller state in correct intervals
    def sending_function(self):
        while self.recording_signal.is_set():
            self.signal.axis_to_signal(self.roll, self.pitch, self.yaw, self.throttle)
            sleep(self.send_delay)

    def stop_inputs(self):
        self.recording_signal.clear()

    def recording(self):
        return self.recording_signal.is_set()

    def create_threads(self):
        self.recording_Thread = Thread(target=self.recording_function, args=[])
        self.recording_Thread.daemon = True
        self.sending_Thread = Thread(target=self.sending_function, args=[])
        self.sending_Thread.daemon = True
