from deck import Deck

class Player:
    # TODO: add actions left and reset after finished turn
    def __init__(self, name):
        self.name = name
        self.deck = Deck(self)
        self.turn = 0

    def handleAction(self, action, what):
        if action == "starts":
            self.deck.gainCardsToPile(what, "drawpile")
        elif action == "shuffles":
            print(self.name, "shuffles ...")
        elif action == "draws":
            self.deck.drawCards(what)
        elif action == "plays":
            self.deck.playCards(what)
