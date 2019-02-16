from player import Player


class Game:
    def __init__(self, gameId, rated):
        self.gameId = gameId
        self.rated = rated
        self.players = []
        self.current_player = None

    @property
    def turn(self):
        return max([p.turn for p in self.players])

    def addPlayer(self, name):
        self.players.append(Player(name))

    def getPlayerByName(self, pname):
        for p in self.players:
            if p.name.startswith(pname):
                return p
        else:
            raise Exception("No player with this name: {}".format(pname))


