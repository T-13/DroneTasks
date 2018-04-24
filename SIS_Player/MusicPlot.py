from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt


class MusicPlot(FigureCanvas):
    def __init__(self):
        # Init stuff
        self.fig = Figure(tight_layout=True)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.plotnav = NavigationToolbar(self.fig.canvas, self)
        self.plotnav.setStyleSheet("QToolBar { border: 0px }")
        self.plotnav.setOrientation(Qt.Vertical)
        self.plotnav.setMaximumWidth(35)

        self.background = None
        self.line = None
        self.xmin = 0
        self.xmax = 0

    def plot(self, data_time, data_samples, step):
        # Plot data
        self.axes.margins(x=0)
        self.axes.plot(data_time[0::step], data_samples[0::step], "-")
        self.fig.canvas.draw()

        self.xmin, self.xmax = self.axes.get_xlim()

    def drawHLine(self, X):
        if self.background:
            if self.xmax < X:
                X = self.xmax
            self.line.set_xdata([X])
            self.fig.canvas.restore_region(self.background)
            self.axes.draw_artist(self.line)
            self.fig.canvas.blit(self.fig.bbox)

    def initBackground(self):
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        if not self.line:
            self.line = self.axes.axvline(0, color='r')
