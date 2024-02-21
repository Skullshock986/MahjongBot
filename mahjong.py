import json
import random
from typing import List

total_tiles = {}
with open('tiles.json', 'r') as file:
    start_tiles = json.load(file) #Creates a dictionary containing an entire set of tiles


class Player:
    def __init__(self, hand: list) -> None:
        self._hand = hand #Would be ideal to ensure the list is sorted, either we can implement it into the constructor at this stage or we can check it at the input stage idk which is better
    
    def discard(self, drawnTile: str): #Eventually will be filled with a method to select a discard, then return new hand and the discard tile

        print(self._hand)
        print()

        self._hand.append(drawnTile) #append 14th tile to hand
        discardPossibilities = []
        for i in range(len(self._hand)): 

            tempHand = self._hand[:i] + self._hand[i+1:]

            tempScore = self.format_hand(tempHand)
            discardPossibilities.append((self._hand[i] , tempScore))  
        
        discardPossibilities.sort(key=lambda x: (x[1]["shanten"], -x[1]["tileEff"]))
        
        print(discardPossibilities)
        print()

        self._hand.remove(discardPossibilities[0][0])

        
        print(self._hand)
        print()

    def format_hand(self, hand) : #The intent is to separate the raw hand into sublists with integer values for each suit and an integer count of the honour tiles
        

        handDict = {
            "char": [],   # Hopefully this will be useful for calculating shanten and similar operations
            "bamb": [],
            "circ": [],
            "e_wind": 0,
            "s_wind": 0,
            "w_wind": 0,
            "n_wind": 0,
            "w_drag": 0,
            "g_drag": 0,
            "r_drag": 0,
        }

        handArray = [[0 for x in range(9)], [0 for x in range(9)], [0 for x in range(9)], [0 for x in range(7)]]

        for i in hand:
            for item in handDict:
                if item in i:
                    if item in ["char", "circ", "bamb"]:

                        suitsDict = {
                            "char" : 0,
                            "bamb" : 1,
                            "circ" : 2,
                        }

                        honorsDict = {
                            "e_wind": 0,
                            "s_wind": 1,
                            "w_wind": 2,
                            "n_wind": 3,
                            "w_drag": 4,
                            "g_drag": 5,
                            "r_drag": 6,
                        }
                                
                        handDict[item].append((i.split("_")[0]))
                        handDict[item].sort()

                        print(i, (suitsDict[item]), int(i[0]) - 1) 

                        handArray[suitsDict[item]][int(i[0]) - 1] += 1

                    else:
                        handDict[item] +=1
                        
                        print(i, 3, honorsDict[item])
                        handArray[3][honorsDict[item]] +=1

        
        print(handArray)
        print()

        handScore = {
            "displayHand" : handDict,
            "calcHand" : handArray,
            "shanten" : self.calcShanten(handDict),
            "tileEff" : self.calcTileEff(handDict)
            
        }

        return handScore

    def calcShanten(self, handDict):
        return random.randint(0,5)

    def calcTileEff(self, handDict):
        return random.randint(1,30)

    

seq = {
    "1,2,3"

}

trip = {
    "1,1,1"
}

player = Player(["2_char", "3_char",	"5aka_char",	"2_circ",	"3_circ",	"6_circ",	"6_circ",	"6_bamb",	"7_bamb",	"7_bamb",	"w_drag",	"w_drag",	"w_drag"])
player.discard("1_char")