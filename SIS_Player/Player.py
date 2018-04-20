from threading import Thread, Event
import threading
import numpy as np

import pyaudio


class MaPlayer:
    def __init__(self):
        # instantiate PyAudio
        self.p = pyaudio.PyAudio()

        # Important properties
        self.stream = False
        self.sound = False
        self.mainData = False
        self.isPlaying = False
        self.hasStarted = False
        self.notifyPlay = Event()
        self.notifyStop = Event()
        self.playThread = False

        self.playIndex = 0

        # Init default stream variables
        self.rate = 44100
        self.channels = 2
        self.format = pyaudio.paInt16
        self.chunk = int(self.rate*0.2)

        self.endCallback = None
        self.playingCallback = None

    def __del__(self):
        self.closeStream()

    # Start stream
    def initStream(self, rate = 44100, channels = 2, format = pyaudio.paInt16, closeStream = True):
        if closeStream:
            self.closeStream()

        self.rate = rate
        self.chunk = int(self.rate*0.2)
        self.format = format
        self.channels = channels

        # open stream
        self.stream = self.p.open(format=format,
                                  channels=channels,
                                  rate=rate,
                                  output=True)

    # Close stream
    def closeStream(self):
        # Close stream if opened
        if self.stream != False:
            self.notifyStop.clear()
            self.notifyPlay.clear()

            if self.isPlaying:
                self.notifyStop.wait()

            self.stream.stop_stream()
            self.stream.close()
            self.stream = False

            self.isPlaying = False
            self.hasStarted = False

            self.playIndex = 0

            if self.playThread != False:
                if threading.current_thread() != self.playThread:
                    self.notifyPlay.set()
                    self.playThread.join()
                self.playThread = False

            if threading.current_thread() != self.playThread:
                self.notifyPlay.clear()

    # Load whole audio data
    def loadData(self, segment):
        self.closeStream()
        self.mainData = segment
        self.loadSound(self.mainData.get_array_of_samples(),
                       changeStream=True,
                       rate=self.mainData.frame_rate,
                       channels=self.mainData.channels,
                       format=self.p.get_format_from_width(self.mainData.sample_width))


    # Load new sound
    def loadSound(self, samples, changeStream=False, rate=44100, channels=2, format=pyaudio.paInt16):
        if self.isPlaying:
            self.notifyPlay.clear()

        # Assign sound
        self.sound = np.array(samples)
        self.playIndex = 0

        # If requested re-init stream
        if changeStream:
            self.initStream(rate=rate,
                            channels=channels,
                            format=format)

        if self.isPlaying:
            self.notifyPlay.set()

    def skipToTime(self, time):
        if self.isPlaying:
            self.notifyPlay.clear()

        self.playIndex = time

        if self.isPlaying:
            self.notifyPlay.set()


    # Function that plays the sound
    def playingFunction(self):
        if self.stream != False:
            self.isPlaying = True
            while self.playIndex < self.sound.size and self.stream != False:
                temp = self.sound[self.playIndex:self.playIndex+self.chunk:1]
                self.stream.write(temp.tobytes())

                if self.playingCallback and self.isPlaying:
                    self.playingCallback(self.playIndex)

                self.playIndex += self.chunk

                self.notifyStop.set()
                self.notifyPlay.wait()

        # Music finished => reset to beginning
        if self.playIndex >= self.sound.size:
            self.isPlaying = False
            self.stop()
            if self.endCallback:
                self.endCallback()


    def changeFreq(self, newFreq):
        if newFreq == self.rate:
            return

        self.rate = newFreq
        # open stream
        newStream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  output=True)
        oldStream = None

        if self.stream != False:
            oldStream = self.stream

        self.stream = newStream

        if oldStream is not None:
            oldStream.stop_stream()
            oldStream.close()


    # Pause stream
    def pause(self):
        if self.stream != False:
            self.isPlaying = False
            self.notifyPlay.clear()

    # Continue stream
    def play(self):
        if self.stream != False:
            self.isPlaying = True
            self.notifyPlay.set()

    # Pauses recording and goes to beginning
    def stop(self):
        self.closeStream()
        self.loadSound(self.mainData.get_array_of_samples(),
                       changeStream=True,
                       rate=self.rate,
                       channels=self.channels,
                       format=self.format)
        if self.endCallback:
            self.endCallback()

    # Start stream
    def start(self):
        self.playThread = Thread(target=self.playingFunction, args=[])
        self.playThread.daemon = True
        self.playThread.start()
        self.isPlaying = True
        self.hasStarted = True
        self.notifyPlay.set()


