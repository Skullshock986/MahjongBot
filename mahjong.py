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
         #hand needs to be reformated: i represent tiles of the same array by a array length 9 where the entries are then numer of tiles
        #so [0,1,2,1,0,..] means 2334
        #for honours we will probably have to have an array for them as well and make a restriction that no sequence
        
        def pairs(suit_arr):
            possible_pairs=[]

            for i in range(9):
                if suit_arr[i]>1:
                    out = [0]*9
                    out[i] = 2
                    possible_pairs.append(out)
            return possible_pairs

        def triplets(suit_arr):
            possible_triplets=[]

            for i in range(9):
                if suit_arr[i]>2:
                    out = [0]*9
                    out[i] = 3
                    possible_triplets.append(out)
            return possible_triplets

        def complete_sequences(suit_arr):
            possible_sequences=[]
            for i in range(2,9):
                if suit_arr[i]>0 and suit_arr[i-1]>0 and suit_arr[i-2]>0:
                    out = [0]*9
                    out[i]=1
                    out[i-1]=1
                    out[i-2]=1
                    possible_sequences.append(out)
            return possible_sequences

        def incomplete_sequences(suit_arr):
            possible_insequences=[]
            if suit_arr[0]>0 and suit_arr[1]>0:
                out = [0]*9
                out[0]=1
                out[1]=1
                possible_insequences.append(out)
            for i in range(2,9):
                if suit_arr[i]>0 and suit_arr[i-1]>0:
                    out = [0]*9
                    out[i]=1
                    out[i-1]=1
                    possible_insequences.append(out)
                if suit_arr[i]>0 and suit_arr[i-2]>0:
                    out = [0]*9
                    out[i]=1
                    out[i-2]=1
                    possible_insequences.append(out)
            return possible_insequences
        
        def resulting_hand(arr1,arr2):
            out=[0]*9
            for i in range(9):
                out[i] = arr1[i] - arr2[i]
            return out
        
        def shanten_nogroups(hand):
            set_insequences = incomplete_sequences(hand)
            current_shan=0
            set_pairs = pairs(hand)

            for i in set_insequences:
                current = shanten_nogroups(resulting_hand(hand, i))+1
                if current > current_shan:
                    current_shan = current

            for i in set_pairs:
                current = shanten_nogroups(resulting_hand(hand, i))+1

                if current>current_shan:
                    current_shan = current
            return current_shan
        
        def shanten(hand):
            current_shanten=0
            set_pairs = pairs(hand)
            set_seq = complete_sequences(hand)
            set_triplets = triplets(hand)

            if len(set_seq) == 0  and len(set_triplets) == 0:
                current_shanten += shanten_nogroups(hand)

            for j in set_seq:
                current = shanten(resulting_hand(hand, j))+2
                if current>current_shanten:
                    current_shanten = current

            for j in set_triplets:
                current = shanten(resulting_hand(hand, j))+2
                if current>current_shanten:
                    current_shanten = current
            return current_shanten
        def shanten_honours(hand):
            current_shanten=0
            for i in range(hand):
                if i > 2:
                    current_shanten += 2
                if i == 2:
                    current_shanten += 1
            return 
        return 8 -(shanten(hand[0]) + shanten(hand[1]) + shanten(hand[2]) + shanten_honours(hand[3]))
    

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