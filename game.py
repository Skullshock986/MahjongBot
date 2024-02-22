import json
import random

from player import Player


with open('tiles.json', 'r') as file:
    start_tiles = json.load(file) #Creates a dictionary containing an entire set of tiles

class Game:
    def __init__(self, prevWind = "e") -> None:
        self.tilePool = start_tiles
        self.dora = []
        self.prevWind = prevWind
        self.seats = ["n", "e", "s", "w"]
        self.discardPiles = {"n": [], "e": [], "s": [], "w": [] }
        self.over=False

        self.chooseDora()
        self.players = [Player(self.drawHand(), self.chooseSeat()) for i in range(4)]

    def chooseDora(self):
        self.dora.append(self.drawTile())


    def drawHand(self):
        self.tempHandArray = []
        for i in range(13):
            self.tempHandArray.append(self.drawTile())

        return self.tempHandArray
    
    def drawTile(self):
        keys, weights = zip(*self.tilePool.items())

        if any(weights):
            self.tempRandomElement = random.choices(keys, weights=weights)[0]
            self.tilePool[self.tempRandomElement] -= 1
            return self.tempRandomElement
        
        else:
            return None

    def chooseSeat(self):
        seat = random.choice(self.seats)
        self.seats.remove(seat)

        return seat

    def main(self):
        while not self.over:
            for player in self.players:
                if not self.over:
                    draw = self.drawTile()

                    if not draw:
                        self.over = True
                        break
            
                    print(player.getSeat() , "'s turn")
                    discard = player.discard(draw)
                    self.discardPiles[player.getSeat()].append(discard)

        
        

            