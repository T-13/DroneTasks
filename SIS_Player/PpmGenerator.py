import pyaudio
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFileDialog, QPushButton
from pydub import AudioSegment
from Receiver import Receiver
from PpmSignal import PpmSignal


class PpmGenerator(QWidget):

    # Inits basic variables
    def __init__(self, parent):
        super().__init__()

        # Init signal params
        # TODO - Change to correct params for PPM signal
        self.rate = 100000
        self.format = pyaudio.paInt16
        self.channels = 1

        # Init default variables
        self.receiver = Receiver(self)
        self.signalData = []  # DataSamples of the PPM signal (simple array of ints with max and minimum at +/-(2^15-1)

        self.ppmsignal = PpmSignal()

        # Assign parent app
        self.parent = parent

        self.init_ui()

    # Defines the UI of the widget
    def init_ui(self):
        # Init main UI layout
        self.mainUiGrid = QGridLayout()

        # Status text to alert user if recording or not
        self.statusText = QLabel("Stopped")
        self.mainUiGrid.addWidget(self.statusText, 0, 0, 1, 2)

        # Add buttons
        play_button = QPushButton('Play / Pause')
        play_button.clicked.connect(self.play_or_pause)
        self.mainUiGrid.addWidget(play_button, 1, 1, 1, 1)

        graph_button = QPushButton('Draw Graph')
        graph_button.clicked.connect(self.load_ppm_signal)
        self.mainUiGrid.addWidget(graph_button, 2, 1, 1, 1)

        self.setLayout(self.mainUiGrid)

    # Resets state
    def reset(self):
        if self.receiver.recording():
            self.receiver.stop_inputs()

        self.signalData = []
        self.statusText.setText("Stopped")

    # Pauses or resumes/starts recording input from controller
    def play_or_pause(self):
        if self.receiver.recording():
            self.statusText.setText("Paused")
            self.receiver.stop_inputs()
        else:
            self.statusText.setText("Recording")
            self.receiver.get_inputs()

    def load_ppm_signal(self):
        # TEST
        #from PpmSignal import PpmSignal
        #ppm = PpmSignal()
        #ppm.axis_to_signal(1, 2, 1.5, 1, 2, 1, 1.5, 1.5)

        self.signalData = self.receiver.get_ppm_data()

        print(self.signalData)
        #self.signalData = ppm.get_data()
        self.load_signal()

    # Load recording date into program to play
    def load_signal(self):
        # If still recording pause
        if self.receiver.recording():
            self.receiver.stop_inputs()

        self.parent.musicName.setText("Opened: New signal")

        # Load recording into app
        self.parent.loadWave(
            AudioSegment(
                b''.join(self.signalData),
                sample_width=pyaudio.PyAudio().get_sample_size(self.format),
                channels=self.channels,
                frame_rate=self.rate))
        # Load recording graphs
        self.parent.loadWaveGraphs()

    # Save recording data to a file
    def save_signal(self):
        # If still recording pause
        if self.receiver.recording():
            self.receiver.stop_inputs()

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self.parent, "Save to file", "", ".mp3 (*.mp3);;.wav (*.wav)", options=options)
        if fileName:
            # Get type of file
            ext = fileName.split(".")[-1]

            # If on linux and no extension was specified
            if ext != "mp3" and ext != ".wav":
                fileName += ".mp3"
                ext = "mp3"

            # Save to file
            AudioSegment(b''.join(self.signalData), sample_width=pyaudio.PyAudio().get_sample_size(self.format),
                         channels=self.channels, frame_rate=self.rate).export(fileName, ext)

    # TODO - Add method that can record input from controller when self.recording is True - use special class

    # TODO - Add method that translates controller input to PPM signal - use special class
    # TODO - Input params for the translation of input to signal are axis in order: 1. Speed, F/B, Strafe, Rotate
