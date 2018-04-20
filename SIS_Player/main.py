import sys

from App import App
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())
