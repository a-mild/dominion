import re

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from game import Game


class LocateGameElements(QObject):
    createtable = pyqtSignal(name="createTable")

    def __init__(self):
        self.supplyCardcountElems = {}

        self.locate_basesupplycards_timer = QTimer()
        self.locate_kingdomcards_timer = QTimer()
        self.setupGame_timer = QTimer()
        # self.locate_gamelog_timer = QTimer()
        # self.locate_playernames_timer = QTimer()
        # self.parseGameId_timer = QTimer()

        self.locate_basesupplycards_timer.timeout.connect(self.locateBaseSupplyCards)
        self.locate_kingdomcards_timer.timeout.connect(self.locateKingdomCards)
        self.setupGame_timer.timeout.connect(self.setupGame)
        # self.locate_gamelog_timer.timeout.connect(self.locateGamelog)
        # self.locate_playernames_timer.timeout.connect(self.locate_playernames)
        # self.parseGameId_timer.timeout.connect(self.parseGameId)

        self.locate_basesupplycards_timer.start(1000)
        self.locate_kingdomcards_timer.start(1000)
        self.setupGame_timer.start(1000)
        # self.locate_gamelog_timer.start(1000)
        # self.locate_playernames_timer.start(1000)

    def locatePlayernames(self):
        try:
            elems = self.webdriver.find_elements_by_class_name("opponent-name")
            if elems is not None:
                return True
            else:
                return False
        except:
            print("Could not find playernames")
            return False

    def readPlayernames(self):
        # TODO: fix this function to read full name
        elems = self.webdriver.find_elements_by_class_name("opponent-name")
        pnames = []
        for elem in elems:
            pnames.append(elem.text.split()[0])
        return pnames

    def locateBaseSupplyCards(self):
        try:
            baseSupplyCardsContainer = self.webdriver.find_element_by_class_name("base-hero-bar")
            if baseSupplyCardsContainer:
                baseSupplyCards = baseSupplyCardsContainer.find_elements_by_class_name("visible-supply")
                for card in baseSupplyCards:
                    cardname = card.find_element_by_class_name("full-card-name-container").text
                    cardcount_elem = card.find_element_by_class_name("new-card-counter-text")
                    self.supplyCardcountElems[cardname] = cardcount_elem
            else:
                print("keine base karten gefunden")
        except:
            print("error beim basekarten lesen")
        else:
            print("Basekarten gefunden!")
            self.locate_basesupplycards_timer.stop()

    def locateKingdomCards(self):
        try:
            kingdomSupplyContainer = self.webdriver.find_element_by_class_name("supply")
            if kingdomSupplyContainer:
                kingdomSupplyCards = kingdomSupplyContainer.find_elements_by_class_name("visible-supply")
                for card in kingdomSupplyCards:
                    cardname = card.find_element_by_class_name("full-card-name-container").text
                    cardcount_elem = card.find_element_by_class_name("new-card-counter-text")
                    self.supplyCardcountElems[cardname] = cardcount_elem
            else:
                print("keine kingdom karten gefunden")
        except:
            print("error beim kingdom karten lesen")
        else:
            print("Kingdom karten gefunden!")
            self.locate_kingdomcards_timer.stop()

    def locateGamelog(self):
        try:
            self.gamelog_elem = self.webdriver.find_element_by_class_name("game-log")
                # self.locate_gamelog_timer.stop()
        except:
            print("Konnte gamelog nicht finden")
            return False
        else:
            print("Gamelog gefunden!")
            return True
            # self.locate_gamelog_timer.stop()
            # self.parseGameId_timer.start(500)

    def parseGameId(self):
        pattern = re.compile(r"Game\s+#(?P<gameId>\d+),\s+(?P<rated>\w+)")
        m = pattern.search(self.gamelog_elem.text)
        if m:
            # self.parseGameId_timer.stop()
            rated = True if m.group("rated") == "rated" else False
            return (m.group("gameId"), rated)
        else:
            print("konnte game id nicht finden")
            return

    def setupGame(self):
        if all([self.locatePlayernames(),self.locateGamelog()]):
            gameId, rated = self.parseGameId()
            self.game = Game(gameId, rated)
            pnames = self.readPlayernames()
            for name in pnames:
                print(name)
                self.game.addPlayer(name)
            self.createtable.emit()
            self.setupGame_timer.stop()
