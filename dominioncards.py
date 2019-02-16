import os
import json

attributes = ["name", "cost", "pcost", "vp", "actions", "cards", "buys", "coins", "gain_vp"]

def class_dict(kwds):
    return {attr: (kwds[attr] if attr in kwds else 0) for attr in attributes}

def init(self, player, pile):
    self.player = player
    self.pile = pile

def _str(self):
    return self.name

for expansion in os.listdir("cards"):
    for file in os.listdir(os.path.join("cards", expansion)):
        if file.endswith(".json"):
            path = os.path.join("cards", expansion, file)
            with open(path) as f:
                props = json.load(f)
                name = "".join(props["name"].split())
                print(name)
                globals()[name] = type(name,
                                       (),
                                       {"__init__": init,
                                        "__str__": _str,
                                        **class_dict(props)})

if __name__ == "__main__":
    print(Copper.coins)
    aCopper = Copper("p1", "drawpile")
    print("name", aCopper)




