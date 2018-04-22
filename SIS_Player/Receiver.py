from inputs import get_gamepad
from threading import Thread



class Receiver:

    def __init__(self, parent):
        self.recording = False
        self.parent = parent

        self.recording_Thread = Thread(target=self.recording_function, args=[])

    def get_inputs(self):
        self.recording = True
        self.recording_Thread.daemon = True
        self.recording_Thread.start()

    def recording_function(self):
        while self.recording:
            events = get_gamepad()
            for event in events:
                print(event.ev_type, event.code, event.state)

    def stop_inputs(self):
        self.recording = False
