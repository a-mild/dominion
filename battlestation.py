from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStyle, QMessageBox, QLabel, QGridLayout, QWidget, \
    QHBoxLayout, QFrame, QVBoxLayout, QTableView, QDesktopWidget, QGroupBox, QCheckBox

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ListenThread import ListenThread
from dominionscraper import DominionScraper
from pandastable import PandasTable

# TODO: start webdriver as Qthread
# TODO: add player turn label
# TODO: add 2nd table with metrics
class MainWindow(QMainWindow):
    dominion_url = "https://dominion.games/"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.desktop = QDesktopWidget()
        self.setWindowTitle("Dominion Battle Station")
        self.setWindowIcon(QIcon("media/favicon.ico"))
        self.setGeometry(self.desktop.screenGeometry(1))
        self.showMaximized()


        self.initUI()

        self.listening = False

    def initUI(self):
        self.mainwidget = QWidget(self)
        self.setCentralWidget(self.mainwidget)

        self.leftframe = QFrame(self.mainwidget)
        self.leftframe.setFrameStyle(QFrame.Box)
        self.rightframe = QFrame(self.mainwidget)
        self.mainhbox = QHBoxLayout()
        self.mainhbox.addWidget(self.leftframe)
        self.mainhbox.addWidget(self.rightframe)

        self.p1frame = QFrame(parent=self.leftframe)
        # self.p1frame.setStyle(QFrame.Panel)
        # self.p1frame.setFrameStyle(QFrame.Panel)
        self.p1tableview = QTableView(self.p1frame)

        self.p2frame = QGroupBox("Player 2", parent=self.leftframe)
        # self.p2frame.setFrameStyle(QFrame.Panel)
        # self.p2tableview = QTableView(self.p2frame)

        self.leftframevbox = QVBoxLayout()
        self.leftframevbox.addWidget(self.p1frame)
        self.leftframevbox.addWidget(self.p2frame)

        self.leftframe.setLayout(self.leftframevbox)

        self.mainwidget.setLayout(self.mainhbox)

        self.toolbar = self.addToolBar("Connect")

        start_browser = QAction(QIcon("media/favicon.ico"), "start", self)
        listener_status = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogNoButton)), "listen", self)
        self.autologin = QCheckBox("Auto-Login")

        start_browser.triggered.connect(self.start_webdriver)
        listener_status.triggered.connect(self.start_listener)

        self.toolbar.addAction(start_browser)
        self.toolbar.addWidget(self.autologin)
        self.toolbar.addAction(listener_status)

        self.show()

    def wait_for_presence_of_element(self, name, by, waittime=10):
        try:
            return WebDriverWait(self.webdriver, waittime).until(EC.presence_of_element_located((getattr(By, by), name)))
        except:
            print("Konnte Element nicht finden: ", name)

    def start_webdriver(self):
        self.webdriver = webdriver.Firefox()
        self.scraper = DominionScraper(self.webdriver)
        self.scraper.createtable.connect(self.createTable)
        self.webdriver.get(MainWindow.dominion_url)
        if self.autologin.isChecked():
            print("trying autologin")
            username_input = self.wait_for_presence_of_element("username-input", "ID")
            username_input.clear()
            username_input.send_keys("schlafi")
            passwd_input = self.wait_for_presence_of_element("password", "NAME")
            passwd_input.clear()
            passwd_input.send_keys("ganxta89")
            passwd_input.submit()

    def start_listener(self):
        if self.browser:
            self.listening = True
            # self.ListenThread.start()
        else:
            QMessageBox.critical(self, "Kein Webdriver",
                                 "Starte zuerst den Webdriver bevor du den Listener aktivierst",
                                 QMessageBox.Ok)

    # @pyqtSlot(int)
    # def update_label(self, text):
    #     self.testlabel.setText(str(text))

    @pyqtSlot(name="createTable")
    def createTable(self):
        print("trying to create table")
        self.p1tablemodle = PandasTable(self.scraper.game.getPlayerByName("schlafi").deck.cardcountTable)
        self.p1tableview.setModel(self.p1tablemodle)


if __name__ == "__main__":
    theApp = QApplication([])
    mw = MainWindow()
    mw.show()

    theApp.exec_()