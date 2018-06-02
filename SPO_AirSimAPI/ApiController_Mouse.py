from AirSimClient import *
import inputs
from threading import Thread, Event
from time import sleep
import signal
import sys

# Change if mouse has different absolute return values
mouse_absolute_maximum = 2000


class Receiver:
    def __init__(self):
        self.recording_signal = Event()

        self.recording_Thread = Thread(target=self.recording_function, args=[])
        self.recording_Thread.daemon = True

        self.default_roll = 0
        self.default_pitch = 0
        self.default_yaw = 0
        self.default_throttle = 0

        # Axis values
        self.roll = self.default_roll
        self.pitch = self.default_pitch
        self.yaw = self.default_yaw
        self.throttle = self.default_throttle

    # Checks if Receiver is recording input
    def recording(self):
        return self.recording_signal.is_set()

    # Creates the thread needed for the receiver to record data
    def create_threads(self):
        self.recording_Thread = Thread(target=self.recording_function, args=[])
        self.recording_Thread.daemon = True

    # Starts recording inputs async
    def get_inputs(self):
        self.recording_signal.set()
        self.create_threads()
        self.recording_Thread.start()

    # Stops recording
    def stop_inputs(self):
        self.recording_signal.clear()
        self.recording_Thread.join()

    def reset(self):
        # Stop if running
        if self.recording():
            self.stop_inputs()
        # Set inputs to default values
        self.roll = self.default_roll
        self.pitch = self.default_pitch
        self.yaw = self.default_yaw
        self.throttle = self.default_throttle

    # Runs async and records input
    def recording_function(self):
        try:
            while self.recording_signal.is_set():
                events = inputs.get_mouse()
                for event in events:
                    if event.code == "ABS_X":
                        self.roll = (event.state / mouse_absolute_maximum) * 3
                    elif event.code == "ABS_Y":
                        self.pitch = (event.state / mouse_absolute_maximum) * 3
                    elif event.code == "BTN_LEFT" and event.state == 1:
                        self.yaw += 1
                    elif event.code == "BTN_RIGHT" and event.state == 1:
                        self.yaw -= 1
                    elif event.code == "REL_WHEEL":
                        self.throttle += event.state
                        if self.throttle < 0:
                            self.throttle = 0
            return 0
        except:
            return 1


rec = Receiver()


def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    if rec.recording():
        rec.stop_inputs()
    print("Exiting program")
    sys.exit(0)


# MAIN
if __name__ == '__main__':
    # connect to the AirSim simulator
    client = MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Assign interrupt call
    signal.signal(signal.SIGINT, signal_handler)

    print("-----------------------\nCONTROLS:\nMouse Y => Pitch\nMouse X => Roll\nLMB => -Yaw\nRMB => +Yaw"
          "\nMouse wheel => Throttle\n^C => Exit gracefully\n-----------------------\n")

    client.reset()
    client.enableApiControl(True)
    client.wait_key("Press any key to start")

    # Stat receiving inputs
    rec.get_inputs()
    print("-----------------------\nStarting")
    try:
        while True:
            print("Clients Pitch, Roll, Yaw: ")
            print(client.getPitchRollYaw())
            print("Pitch, Roll, Yaw, Throttle from input: ")
            print([rec.pitch, rec.roll, rec.yaw, rec.throttle])

            client.moveByAngleThrottle(rec.pitch - client.getPitchRollYaw()[0], rec.roll - client.getPitchRollYaw()[1],
                                       rec.throttle, client.getPitchRollYaw()[2] + rec.yaw, 0.225)
            sleep(0.225)

    except SystemExit:
        os._exit(0)
    except Exception as e:
        print("Something went horribly wrong")  # some other exception got
        print(str(e))
        os._exit(1)
