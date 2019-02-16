import re

from PyQt5.QtCore import QTimer, QObject, pyqtSignal

import dominioncards as cards
from game import Game
from locateGameElements import LocateGameElements


class DominionScraper(LocateGameElements, QObject):
    basesupplycards_found = pyqtSignal(int)
    kingdomcards_found = pyqtSignal(int)

    turn_pattern = re.compile(r"Turn\s+(?P<turn>\d+)\s+\-\s+(?P<pname>\w+)")
    action_pattern = re.compile(r"(?P<pname>\w+)\s+(?P<action>\w+|buys\s+and\s+gains)\s+(?P<what>.*)(?=\.)")

    def __init__(self, webdriver):
        QObject.__init__(self)
        self.webdriver = webdriver
        LocateGameElements.__init__(self)

        self.gamelog_cursor = 0
        self.save_what = None

        self.parseGamelog_timer = QTimer()
        # self.parsePlayernames_timer.timeout.connect(self.parsePlayernames)
        self.parseGamelog_timer.timeout.connect(self.parseGamelog)
        self.parseGamelog_timer.start(200)

    @property
    def gamelogLines(self):
        return self.gamelog_elem.find_elements_by_class_name("actual-log")

    def getGameloglineText(self, i):
        return self.gamelogLines[i-1].text

    def parseGamelog(self):
        if not self.setupGame_timer.isActive():
            while len(self.gamelogLines) > self.gamelog_cursor:
                self.gamelog_cursor += 1
                print("parsing line ", self.gamelog_cursor)
                self.parseGamelogline(self.gamelog_cursor)

    def parseGamelogline(self, i):
        logline = self.getGameloglineText(i)
        m = DominionScraper.turn_pattern.search(logline)
        if m:
            p = self.game.getPlayerByName(m.group("pname"))
            self.game.current_player = p
            p.turn = m.group("turn")
            return True
        else:
            m = DominionScraper.action_pattern.search(logline)
            if m:
                p = self.game.getPlayerByName(m.group("pname"))
                action = m.group("action")
                what_str = m.group("what")
                if not what_str == self.save_what:
                    what = self.parseWhat(what_str)
                    p.handleAction(action, what)
                self.save_what = what_str
                return True
            else:
                print("Konnte zeile {} nicht parsen".format(self.gamelog_cursor + 1))
                return False

    def parseWhat(self, _str):
        pattern = re.compile(r"\+.(?P<money>\d+)|(?P<cardcount>\d+|a|an)\s+(?P<cardname>[\w'-]+)")
        m_iter = pattern.finditer(_str)
        cards = {}
        if m_iter:
            for m in m_iter:
                cardname = m.group("cardname").rstrip("s")
                if m.group("cardcount") in ["a", "an"]:
                    cardcount = 1
                else:
                    cardcount = int(m.group("cardcount"))
                cards[cardname] = cardcount
        return cards

    def getCardcount(self, cardname):
        return self.supplyCardcountElems[cardname].text



    # def parseStartcards(self):
    #     pattern = re.compile(r"(?P<pname>\w+)(\s+starts\s+with\s+)(?P<cardstring>.*)(?=\.)")
    #     m_iter = pattern.finditer(self.gamelog_elem.text)
    #     if m_iter:
    #         self.parseStartcards_timer.stop()
    #         for m in m_iter:
    #             pname = m.group("pname")
    #             # print("{player} has {cardcount} {cardname}".format(player=m.group("pname"),
    #             #                                                    cardcount=m.group("cardcount"),
    #             #                                                    cardname=m.group("cardname")))
    #             startcards = self.parseCardstring(m.group("cardstring"))
    #             self.game.getPlayerByName(pname).deck.gainCardsToPile(startcards, "drawpile")
    #         else:
    #             print("alle spieler haben alle karten gekriegt")
    #             for player in self.game.players:
    #                 player.deck.getCardcountTable()
    #             self.createtable.emit()
    #             self.parseFirstDraw_timer.start(500)
    #         # self.gamelog_cursor = self.getGamelogLength() - 1
    #     else:
    #         print("konnte startkarten nicht finden")


    #
    # def getGamelogLine(self, linenr):
    #     return self.webdriver.find_elements_by_class_name("actual-log")[linenr-1]
    #
    # def parseGamelog(self):
    #     return

    def getPileCount(self, cardname):
        name = cardname + "count_elem"
        try:
            return int(getattr(self, name).text)
        except AttributeError:
            print("Falscher Kartenname oder die Karte ist nicht im Spiel")