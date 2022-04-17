import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import TransEXTify

WINDOW_TITLE = 'TransEXTify'
APP_ICON_URL = './asset/myicon.ico'


def run():
    app = QApplication(sys.argv)
    imageFrame = TransEXTify.TransEXTify()
    imageFrame.setWindowTitle(WINDOW_TITLE)
    imageFrame.setWindowIcon(QIcon(APP_ICON_URL))
    imageFrame.mainwidget.setFocus()
    imageFrame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
