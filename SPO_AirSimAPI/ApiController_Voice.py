from AirSimClient import *
import sys
import signal
import speech_recognition as sr


def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    print("Exiting program")
    sys.exit(0)


if __name__ == '__main__':
    # connect to the AirSim simulator
    client = MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Assign interrupt call
    signal.signal(signal.SIGINT, signal_handler)

    print("Sound devices:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(str(index) + ": " + name)

    mic_index = int(input("-----------------------\nInsert microphone index: "))

    print("-----------------------\nCONTROLS:\nForward\nBack\nUpward\nDownward\nLeft\nRight\nLand\nTakeoff\nHover\n"
          "^C => Exit gracefully\n-----------------------")
    print("Only 1 command can be computed at once\n-----------------------")

    client.reset()
    client.enableApiControl(True)
    client.wait_key("Press any key to start")
    print("Taking off...")
    client.takeoff(max_wait_seconds=4)

    # Init recognizer
    m = sr.Microphone(device_index=mic_index)
    print("Using microphone: " + sr.Microphone.list_microphone_names()[mic_index])
    r = sr.Recognizer()

    print("-----------------------\nStarting")
    try:
        while True:
            # Start listening
            with m as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Recording - Speak now!")
                sound = r.listen(source, timeout=2, phrase_time_limit=2)

            print("Processing...")
            try:
                result = r.recognize_sphinx(sound)
            except:
                result = "Nothing was recognised"

            print("Recognized speech: " + result)

            # Check what to do
            if "forward" in result:
                client.moveByAngleThrottle(-0.5, 0, 2, 0, 4)

            elif "back" in result:
                client.moveByAngleThrottle(0.5, 0, 2, 0, 4)

            elif "downward" in result:
                client.hover()
                client.moveByAngleThrottle(0, 0, 0.3, 0, 4)

            elif "upward" in result:
                client.hover()
                client.moveByAngleThrottle(0, 0, 7, 0, 4)

            elif "left" in result:
                client.moveByAngleThrottle(0, -0.5, 2, 0, 4)

            elif "right" in result:
                client.moveByAngleThrottle(0, 0.5, 2, 0, 4)

            elif "land" in result:
                client.land(max_wait_seconds=4)

            elif "takeoff" in result or ("take" in result and "off" in result):
                client.takeoff(max_wait_seconds=4)

            elif "hover" in result:
                client.hover()

    except SystemExit:
        os._exit(0)
    except Exception as e:
        print("Something went horribly wrong")  # some other exception got
        print(str(e))
        os._exit(1)
