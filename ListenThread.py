from PyQt5.QtCore import QThread, pyqtSignal

class LocateBaseSupplyCardsThread(QThread):
    signal = pyqtSignal("QString")

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent

    def run(self):
        return



class ListenThread(QThread):
    listen_signal = pyqtSignal("QString")

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent

    def run(self):
        return
        # self.browser = self.parent.browser
        # while self.parent.listening:
        #     self.parent.scraper.getPile
        #     # self.browser.implicitly_wait(2)
        #     # loglines = self.browser.find_elements_by_class_name("game-log")
        #     # if loglines:
            #     for line in loglines:
            #         print(line.text)
            #         self.listen_signal.emit(line.text)

    # def check_victory_cards(self):
    #     if self.browser:
    #         self.browser.