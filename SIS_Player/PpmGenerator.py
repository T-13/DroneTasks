import pyaudio
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFileDialog, QPushButton
from pydub import AudioSegment
from Receiver import Receiver
from MusicPlot import MusicPlot
import numpy as np


class PpmGenerator(QWidget):

    # Inits basic variables
    def __init__(self, parent):
        super().__init__()

        # Init signal params
        # TODO - Change to correct params for PPM signal
        self.rate = 1000
        self.format = 2
        self.channels = 1

        # Init default variables
        self.receiver = Receiver(self)
        self.signalData = []  # DataSamples of the PPM signal (simple array of ints with max and minimum at +/-(2^15-1)

        # Assign parent app
        self.parent = parent

        self.init_ui()

    # Defines the UI of the widget
    def init_ui(self):
        # Init main UI layout
        self.mainUiGrid = QGridLayout()

        # Status text to alert user if recording or not
        self.statusText = QLabel("Stopped")
        self.mainUiGrid.addWidget(self.statusText, 0, 3, 1, 1)

        # Graph that will draw the signal in the way it would be transmitted over WIFI network
        self.graph = MusicPlot()
        self.update_graph()
        self.mainUiGrid.addWidget(self.graph, 1, 0, 10, 3)
        self.mainUiGrid.addWidget(self.graph.plotnav, 1, 3, 10, 1)

        # Add buttons
        play_button = QPushButton('Play / Pause')
        play_button.clicked.connect(self.play_or_pause)
        self.mainUiGrid.addWidget(play_button, 0, 0, 1, 1)

        # Add buttons
        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.reset)
        self.mainUiGrid.addWidget(reset_button, 11, 0, 1, 1)

        load_button = QPushButton('Load to program')
        load_button.clicked.connect(self.load_signal)
        self.mainUiGrid.addWidget(load_button, 11, 1, 1, 1)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_signal)
        self.mainUiGrid.addWidget(save_button, 11, 2, 1, 1)

        self.setLayout(self.mainUiGrid)

    # Resets state
    def reset(self):
        if self.receiver.recording():
            self.receiver.stop_inputs()

        self.receiver.reset()
        self.signalData = []
        self.statusText.setText("Stopped")
        self.update_graph()

    # Pauses or resumes/starts recording input from controller
    def play_or_pause(self):
        if self.receiver.recording():
            self.statusText.setText("Paused")
            self.receiver.stop_inputs()
            self.update_graph()
        else:
            self.statusText.setText("Recording")
            self.receiver.get_inputs()

    def load_ppm_signal(self):
        self.signalData = self.receiver.get_ppm_data()

    # Load recording date into program to play
    def load_signal(self):
        self.load_ppm_signal()
        # If still recording pause
        if self.receiver.recording():
            self.receiver.stop_inputs()

        self.parent.musicName.setText("Opened: New signal")

        # Load recording into app
        self.parent.loadSamples(self.signalData, self.rate,
                                self.channels, self.format)

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
            if ext != "mp3" and ext != "wav":
                fileName += ".mp3"
                ext = "mp3"

            # Save to file
            AudioSegment(b''.join(self.signalData), sample_width=pyaudio.PyAudio().get_sample_size(self.format),
                         channels=self.channels, frame_rate=self.rate).export(fileName, ext)

    def update_graph(self):
        # Update graph
        self.graph.axes.clear()
        time = np.linspace(0, self.receiver.signal.duration, num=len(self.receiver.signal.data))
        self.graph.plot(time, self.receiver.signal.data, 1)
        self.graph.addLabel("amp (int)", "y")
        self.graph.addLabel("t (ms)", "x")
