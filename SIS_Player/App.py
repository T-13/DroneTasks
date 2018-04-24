import gc
import os

import numpy as np
from MusicPlot import MusicPlot
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import *
from PpmGenerator import PpmGenerator
from pydub import AudioSegment
from Player import MaPlayer
import math


class App(QWidget, QObject):
    playingSignal = pyqtSignal(int)
    endSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = 'SIS_Player'
        self.left = 110
        self.top = 130
        self.width = 1200
        self.defaultHeight = 400
        self.height = self.defaultHeight

        self.channels = 1
        self.frame_rate = 1
        self.frame_width = 1

        # Init logic variables
        self.sound = np.array([])
        self.time = 0

        self.player = MaPlayer()
        self.player.endCallback = self.endCallback
        self.player.playingCallback = self.playingCallback

        self.PpmGenerator = PpmGenerator(self)

        self.playingSignal.connect(self.playingEvent)
        self.endSignal.connect(self.resetTimeIndicatorUI)

        # Init graph variables
        self.graphs = []
        self.numberOfGraphs = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(self.size())  # Make window unresizeable for user

        # Init main UI layouts
        self.mainUiGrud = QGridLayout()
        self.tabWidget = QTabWidget()

        # Init tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabWidget.addTab(self.tab1, "Graph")
        self.tabWidget.addTab(self.tab2, "PPM")

        # Set main layout
        self.setLayout(self.mainUiGrud)

        self.musicName = QLabel(" Opened: - ")
        self.mainUiGrud.addWidget(self.musicName, 0, 0, 1, 3)

        PausePlayButton = QPushButton('Play / Pause')
        PausePlayButton.clicked.connect(self.pausePlay)
        self.mainUiGrud.addWidget(PausePlayButton, 1, 2)

        StopButton = QPushButton('Stop')
        StopButton.clicked.connect(self.stop)
        self.mainUiGrud.addWidget(StopButton, 1, 1)

        LoadButton = QPushButton('Load', self)
        LoadButton.clicked.connect(self.load)
        self.mainUiGrud.addWidget(LoadButton, 1, 0)

        self.slider = QSlider(Qt.Horizontal)  # Makes slider horizontal
        self.slider.updateGeometry()
        self.slider.sliderReleased.connect(self.timeChange)
        self.mainUiGrud.addWidget(self.slider, 2, 0, 1, 3)

        self.mainUiGrud.addWidget(self.tabWidget, 3, 0, 1, 3)

        # Tab1 layout init
        tab1Scroll = QScrollArea()
        tab1Scroll.setWidgetResizable(True)
        gridHolder = QWidget()
        self.graphGrid = QGridLayout(gridHolder)
        tab1Scroll.setWidget(gridHolder)
        box1 = QVBoxLayout()
        box1.addWidget(tab1Scroll)
        box1.setContentsMargins(0, 0, 0, 0)

        self.tab1.setLayout(box1)

        # Tab2 layout init
        tab2Scroll = QScrollArea()
        tab2Scroll.setWidgetResizable(True)
        tab2Scroll.setWidget(self.PpmGenerator)
        box2 = QVBoxLayout()
        box2.addWidget(tab2Scroll)
        box2.setContentsMargins(0, 0, 0, 0)

        self.tab2.setLayout(box2)
        self.show()

    # Loads sound from file
    def load(self):
        # Reset all data and graph variables and size
        self.reset()
        # Open select file dialog with .mp3 and .wav fiter
        options = QFileDialog.Options()
        fileP, _ = QFileDialog.getOpenFileName(self, "Select file", "", ".mp3 (*.mp3);;.wav (*.wav)", options=options)
        # If file is selected
        if fileP:
            # Alert user of file loaded
            head, tail = os.path.split(fileP)
            self.musicName.setText(" Opened: " + tail)

            # Load data
            self.loadWave(AudioSegment.from_file(fileP))

            # Load graphs
            self.loadWaveGraphs()

    # Resets all variables and size
    def reset(self):
        # Try to clear memory...
        # For some reason 100MB leaks
        for graph in self.graphs:
            graph.fig.clf()
            graph.close()

        self.musicName.setText(" Opened: - ")

        self.graphs = []
        self.numberOfGraphs = 0
        self.height = self.defaultHeight
        self.resize(self.width, self.height)

        self.player.closeStream()

        self.sound = np.array([])
        self.time = []

        # Reset slider
        self.slider.setValue(0)

        gc.collect()

    # Stop play of music if loaded
    def stop(self):
        # Stop sound
        self.player.pause()
        self.player.stop()

    # Plays or pauses music
    def pausePlay(self):
        # If we have loaded sound
        if self.sound.any():
            # If inited but not busy => Sound finished playing => Replay
            if not self.player.hasStarted:
                # Start
                self.player.start()

            # If is already playing => Pause
            elif self.player.isPlaying:
                self.player.pause()

            # If paused => Unpause
            else:
                self.player.play()

    # Correctly updates the played sound data to play from where user requested
    def timeChange(self):
        # If we have loaded sound
        if self.sound.any():
            # Cut away all data before the given time
            self.player.skipToTime(self.slider.value())

            # Update visualization of current time on the graph
            self.updateGraphsHorLine(self.slider.value())

    def updateGraphsHorLine(self, value):
        for graph in self.graphs:
            if graph.background is None:
                graph.initBackground()
            graph.drawHLine(self.time[value])

    def playingEvent(self, time):
        self.updateGraphsHorLine(time)

    # Set UI that indicates where the player is at to initial state
    def resetTimeIndicatorUI(self):
        # Set slider to 0
        self.slider.setValue(0)
        # Update visualization of current time on the graph
        self.updateGraphsHorLine(0)

    # Managing events of MaPlayer
    def playingCallback(self, time):
        # Emit signal with correct time
        self.playingSignal.emit(time)

    # Managing events of MaPlayer
    def endCallback(self):
        # Emit signal of song finish
        self.endSignal.emit()

    # Load data
    def loadWave(self, waveData):
        self.sound = np.array(waveData.get_array_of_samples())
        self.frame_rate = waveData.frame_rate
        self.channels = waveData.channels
        self.frame_width = waveData.sample_width
        self.duration = waveData.duration_seconds
        # Init mixer with params depending on sound
        self.player.loadData(self.sound, waveData.frame_rate,
                             waveData.channels, waveData.sample_width)

        # Get array of "measurment times"
        self.time = np.linspace(0, self.duration, num=len(self.sound))

        # Update slider values to correctly sync with music time
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.time) - 1)
        self.slider.setSingleStep(1)

    # Load data
    def loadSamples(self, samples, frame_rate, channels, width):
        self.sound = np.array(samples)
        self.frame_rate = frame_rate
        self.channels = channels
        self.frame_width = width
        self.duration = len(samples) / self.frame_rate
        # Init mixer with params depending on sound
        self.player.loadData(self.sound, frame_rate,
                             channels, width)

        # Get array of "measurment times"
        self.time = np.linspace(0, self.duration, num=len(self.sound))

        # Update slider values to correctly sync with music time
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.time) - 1)
        self.slider.setSingleStep(1)

    # Loads the graphs for tab1 from sound data
    def loadWaveGraphs(self):
        # Remove old graphs if exist
        for graph in self.graphs:
            graph.fig.clf()
            graph.close()

        self.graphs = []
        self.numberOfGraphs = 0
        self.height = self.defaultHeight
        self.resize(self.width, self.height)

        gc.collect()

        # Get np.array of sound data
        samplesArray = self.sound

        # Update height correctly acording to number of graphs/channels
        self.height = 200 * self.channels + 200
        self.resize(self.width, self.height)

        # Split chanels [samp1L, samp1R, samp2L, samp2R]
        for i in range(0, self.channels):
            self.addChanel(self.time[i::self.channels], samplesArray[i::self.channels])

    # Adds a graph of the passed chanel to UI
    def addChanel(self, data_time, data_samples):
        # Reduce data for memory and time saving We want
        step = math.ceil(self.frame_rate / 4000)
        temp = math.ceil(len(data_time) / step)
        # If big file, reduce points to 55000
        if temp > 55000:
            step = math.ceil(len(data_time) / 55000)

        # Create graph
        newgraph = MusicPlot()
        # Plot data
        newgraph.plot(data_time, data_samples, step)
        # Put graph onto UI
        self.graphs.append(newgraph)
        self.graphGrid.addWidget(newgraph, self.numberOfGraphs, 0, 1, 3)
        self.graphGrid.addWidget(newgraph.plotnav, 0, 3)
        self.numberOfGraphs += 1
