from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MusicPlot(FigureCanvas):
    def __init__(self):
        # Init stuff
        self.fig = Figure(tight_layout=True)
        self.axes = self.fig.add_subplot(111)

        # Hide lines
        #self.axes.spines['bottom'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        # Hide labels
        #self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        FigureCanvas.__init__(self, self.fig)
        self.setMinimumHeight(200)
        self.setMaximumHeight(200)

        self.setMinimumWidth(1150)
        self.setMaximumWidth(1150)

        self.resize(200,1150)

        self.background = None
        self.line = None
        self.xmin = 0
        self.xmax = 0

    def plot(self, data_time, data_samples, step):
        # Plot data
        self.axes.margins(x=0)
        self.axes.plot(data_time[0::step], data_samples[0::step])
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
        #self.fig.canvas.mpl_connect('resizeEvent', self.resizeHandler)

    def resizeHandler(self, event):
        self.axes.artists.clear()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
