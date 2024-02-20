import json
from typing import List

total_tiles = {}
with open('tiles.json', 'r') as file:
    start_tiles = json.load(file) #Creates a dictionary containing an entire set of tiles


class Player:
    def __init__(self, hand: list) -> None:
        self._hand = hand #Would be ideal to ensure the list is sorted, either we can implement it into the constructor at this stage or we can check it at the input stage idk which is better
    
    def discard(self, drawnTile: str): #Eventually will be filled with a method to select a discard, then return new hand and the discard tile
        self._hand.append(str) #append 14th tile to hand
        discardPossibilities = []
        for i in range(len(self._hand)): 

            tempHand = self._hand[:i] + self._hand[i+1:]

            tempScore = self.format_hand(tempHand)
            discardPossibilities = (self._hand[i] , tempScore)  
        
        discardPossibilities.sort(key=lambda x: (x[1]["shanten"], x[1]["tileEff"]))


    def format_hand(self, hand:List[str]) : #The intent is to separate the raw hand into sublists with integer values for each suit and an integer count of the honour tiles
        

        handDict = {
            "char": [],   # Hopefully this will be useful for calculating shanten and similar operations
            "circ": [],
            "bamb": [],
            "e_wind": 0,
            "s_wind": 0,
            "w_wind": 0,
            "n_wind": 0,
            "r_drag": 0,
            "g_drag": 0,
            "w_drag": 0,
        }

        for i in hand:
            for item in handDict:
                if item in i:
                    if item in ["char", "circ", "bamb"]:
                        handDict[item].append(int(i[0]))
                    else:
                        handDict[item] +=1

        
        handScore = {
            "hand" : handDict,
            "shanten" : self.calcShanten(handDict),
            "tileEff" : self.calcTileEff(handDict)
        }

        return handScore

    def calcShanten(self, handDict):
        return 1

    def calcTileEff(self, handDict):
        return 30

    

seq = {
    "1,2,3"

}

trip = {
    "1,1,1"
}

player = Player(["2_char", "3_char",	"3_char",	"2_circ",	"3_circ",	"6_circ",	"6_circ",	"6_bamb",	"7_bamb",	"7_bamb",	"w_drag",	"w_drag",	"w_drag"])
player.discard("1_char")