import os
from multiprocessing.pool import ThreadPool

from PyQt5.QtCore import pyqtSlot, QFileInfo, pyqtSignal, QBuffer, QByteArray, QIODevice, QSize, Qt
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel
from QCandyUi.CandyWindow import colorful

import ocr_util

from screen_capture import CaptureScreen
from ui_image2text import Ui_image2textWidget

# 全局截屏快捷键
SCREEN_SHOT_SHORTCUT = 'alt'

# 资源路径
WORK_PATH = 'D:/VsCode/TransEXTify'
SCREEN_SHOT_ICON_URL = WORK_PATH+'/asset/scissors.png'
OPEN_FILE_ICON_URL = WORK_PATH+'/asset/file.png'
LOADING_GIF_URL = WORK_PATH+'/asset/loading.gif'

# 设置
MIN_AFTER_SHOT = False


@colorful('blueGreen')
class TransEXTify(QWidget):
    signal_response = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_image2textWidget()
        self.ui.setupUi(self)
        self.ui.textEdit.setAcceptDrops(False)
        self.ui.textEdit.setPlaceholderText('1.将待识别图片拖拽到此处...\n' + '2.截屏识图快捷键: ' + SCREEN_SHOT_SHORTCUT)
        self.setAcceptDrops(True)
        self.init_loading_gif()
        self.signal_response.connect(self.__slot_http_response)
        self.beautify_button(self.ui.pushButtonOpen, OPEN_FILE_ICON_URL)
        self.beautify_button(self.ui.pushButtonCapture, SCREEN_SHOT_ICON_URL)

    def __init_threadPool(self):
        self.pool = ThreadPool(10)

    def beautify_button(self, button, image_url):
        """
        美化按键
        :param button:  QPushButton
        :param image_url: str
        :return: None
        """
        button.setText('')
        button.setIcon(QIcon(image_url))
        icon_width = button.height() >> 1
        button.setIconSize(QSize(icon_width, icon_width))
        button.setFlat(True)

    def init_loading_gif(self):
        """
        初始化loading动画
        :return:
        """
        gif = QMovie(LOADING_GIF_URL)
        gif.start()
        x, y = 275, 110
        self.loadingLabel = QLabel(self)
        self.loadingLabel.setMovie(gif)
        self.loadingLabel.adjustSize()
        self.loadingLabel.setGeometry(x, y, self.loadingLabel.width(), self.loadingLabel.height())
        self.loadingLabel.setVisible(False)


    def run_ocr_async(self, image):
        self.loadingLabel.setVisible(True)
        result = ''
        try:
            result = ocr_util.get_ocr_str(image)
        finally:
            self.signal_response.emit(result)
        


    @pyqtSlot()
    def on_pushButtonOpen_clicked(self):
        self.ui.textEdit.clear()
        file_urls = QFileDialog.getOpenFileNames()[0]
        if len(file_urls) > 0:
            self.ui.textEdit.clear()
        for img_full_path in file_urls:
            if img_full_path is None or img_full_path == '':
                continue
            with open(img_full_path, 'rb') as fp:
                file_bytes = fp.read()
            self.run_ocr_async(file_bytes)

    @pyqtSlot()
    def on_pushButtonCapture_clicked(self):
        self.ui.textEdit.clear()
        self.capture = CaptureScreen()
        self.capture.signal_complete_capture.connect(self.__slot_screen_capture)

    @pyqtSlot(str)
    def __slot_http_response(self, result):
        self.ui.textEdit.append(result)
        self.loadingLabel.setVisible(False)

    @pyqtSlot(QPixmap)
    def __slot_screen_capture(self, image):
        image.save(WORK_PATH+'/data/1.jpg')
        self.run_ocr_async(WORK_PATH+'/data/1.jpg')

    def dragEnterEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if (event.mimeData().hasUrls()):
            urlList = event.mimeData().urls()
            realList = list()
            self.ui.textEdit.clear()
            for url in urlList:
                fileInfo = QFileInfo(url.toLocalFile())
                full_path = fileInfo.filePath()
                if os.path.isfile(full_path):
                    realList.append(full_path)
                if os.path.isdir(full_path):
                    realList.extend(self.__getFiles(full_path))
            for url in realList:
                with open(url, 'rb') as fp:
                    file_bytes = fp.read()
                self.run_ocr_async(file_bytes)
            event.acceptProposedAction()

    def __getFiles(self, dir_path, suffix=None):
        if dir_path == '' or dir_path is None:
            return
        if os.path.isfile(dir_path):
            return
        urls = list()
        for maindir, subdir, filename_list in os.walk(dir_path):
            for file in filename_list:
                full_path = os.path.join(maindir, file)
                ext = os.path.splitext(full_path)[1]
                ok = False
                if suffix is None:
                    ok = True
                elif isinstance(suffix, str):
                    if suffix == ext:
                        ok = True
                elif isinstance(suffix, list) or isinstance(suffix, tuple):
                    if suffix is None or ext in suffix:
                        ok = True
                if ok:
                    urls.append(full_path)
        return urls

    def keyPressEvent(self, e):
        """
        ctrl+alt+shift+F8
        :param e:
        :return:
        """
        if e.modifiers() == Qt.AltModifier:
            if MIN_AFTER_SHOT:
                self.parentWidget().showMinimized()
            self.ui.textEdit.clear()
            self.ui.pushButtonCapture.clicked.emit()