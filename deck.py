from functools import wraps
from collections import deque, Counter
import dominioncards as card
import pandas as pd

# TODO: fix problem mit den pilenamen, damit die ansprechbar sind aber im table schön sind. vllt einfach header selbst benennen
class Deck(QObject):
    updateTable = pyqtSignal("updateTable")

    def __init__(self, player):
        self.player = player
        self.drawpile = deque()
        self.hand = []
        self.inplay = []
        self.discardpile = []

        self.cardcountTable = pd.DataFrame(columns=["drawpile", "hand", "inplay", "discardpile", "Total"])
        self.cardcountTable.index.name = "Cardname"

    def __str__(self):
        return self.drawpile.__str__()

    def updateCardcountTable(actionfunc):
        @wraps(actionfunc)
        def wrapper(inst, *args):
            print(args)
            cards =  actionfunc(inst, *args)
            for pile, carddict in inst.card_counts.items():
                for cardname, cardcount in carddict.items():
                    inst.cardcountTable.at[cardname, pile] = cardcount
            inst.cardcountTable["Total"] = 0
            inst.cardcountTable["Total"] = inst.cardcountTable.agg("sum", axis="columns")
            print("updated table")
            print(inst.cardcountTable)
            return cards
        return wrapper

    @property
    def all_piles(self):
        return {"drawpile": self.drawpile,
                "hand": self.hand,
                "inplay": self.inplay,
                "discardpile": self.discardpile}

    @property
    def card_counts(self):
        card_counts = {"drawpile": {}, "hand": {}, "inplay": {}, "discardpile": {}}
        for pile, cards in self.all_piles.items():
            for card in cards:
                cardname = card.__class__.__name__
                if not cardname in card_counts[pile]:
                    card_counts[pile][cardname] = 1
                else:
                    card_counts[pile][cardname] += 1
        return card_counts

    @updateCardcountTable
    def gainCardsToPile(self, cards, pile):
        if not isinstance(cards, dict):
            print("übergebe karten als dict")
        else:
            for (cardname, cardcount) in cards.items():
                for i in range(cardcount):
                    newcard = getattr(card, cardname)(self.player, pile)
                    getattr(self, pile).append(newcard)

    def removeCardsFromPile(self, cards, pile):
        if not isinstance(cards, dict):
            print("übergebe karten als dict")
        elif pile not in ["drawpile", "hand", "inplay", "discardpile"]:
            print("falscher pilename: ", pile)
        else:
            print("removing cards...")
            thepile = getattr(self, pile)
            removed_cards = []
            for (cardname, cardcount) in cards.items():
                for i in range(cardcount):
                    for card in thepile:
                        if card.__class__.__name__ == cardname:
                            removed_cards.append(card)
                            thepile.remove(card)
                            break
                    else:
                        print("Du versuchst {} zu viele {} vom {} zu entfernen".format(cardcount - i,
                                                                                       cardname,
                                                                                       pile))
                        break
            return removed_cards

    @updateCardcountTable
    def drawCards(self, cards):
        removed_cards = self.removeCardsFromPile(cards, "drawpile")
        print("now adding: ", removed_cards)
        if not removed_cards is None:
            self.hand.extend(removed_cards)
        print("{}s Hand: {}.".format(self.player.name, self.hand))

    @updateCardcountTable
    def playCards(self, cards):
        return

    @updateCardcountTable
    def buyCards(self, cards):
        return

    @updateCardcountTable
    def trashCards(self, cards):
        return



if __name__ == "__main__":
    hand = [card.Copper("p1", "drawpile"), card.Copper("p1", "drawpile"), card.Estate("p1", "drawpile")]
    print(hand)
    print(card.Copper("p1", "drawpile").__class__.__name__)
    counter = {}
    for card in hand:
        cardname = card.__class__.__name__
        if not cardname in counter:
            counter[cardname] = 1
        else:
            counter[cardname] += 1
    print(counter)


