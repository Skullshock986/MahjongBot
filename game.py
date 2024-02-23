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
        self.seats = ["e", "s", "w", "n"]
        self.discardPiles = {"e": [], "s": [], "w": [], "n" : [], "total" : []}
        self.over=False
        self.deadWall = [[self.drawTile() for i in range(7)] for j in range(2)]

        self.chooseDora()
        self.players = [Player(["e_wind", "w_wind", "n_wind", "s_wind", "g_dragon", "r_dragon", "1_char", "9_char", "1_bamb", "5_char", "4_bamb", "6_circ", "8_bamb"], self.chooseSeat())] + [Player(self.drawHand(), self.chooseSeat()) for i in range(3)]

    def chooseDora(self):
        l = len(self.dora)
        self.dora.append(self.deadWall[0][2+l])

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
        seat = self.seats.pop(0)
        return seat

    def main(self):
        turn = 0
        while not self.over:
            turn+=1
            for player in self.players:
                if not self.over:
                    draw = self.drawTile()

                    if not draw:
                        self.over = True
                        break
                    
                    windDict = {
                        "e": "East",
                        "s": "South",
                        "w": "West",
                        "n" : "North"
                    }

                    print(windDict[player.getSeat()] , "Player's turn, Turn: ", turn)
                    discard = player.discard(draw)
                    self.discardPiles[player.getSeat()].append(discard)
                    self.discardPiles["total"].append(discard)

        
        

            