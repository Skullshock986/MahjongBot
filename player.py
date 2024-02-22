
import random


class Player:
    def __init__(self, hand: list, seat) -> None:
        self._hand = hand #Would be ideal to ensure the list is sorted, either we can implement it into the constructor at this stage or we can check it at the input stage idk which is better
        self._seat = seat
        self._dealer = True if seat == "e" else False
    
    def getSeat(self):
        return self._seat
    
    def webFormat(self, handArray):
        dict = {0: 'm',
            1: 's',
            2: 'p',
            3: 'z'
        }

        string = ''
        k=0
        for suit in handArray:
            if sum(suit) == 0:
                k+=1
                continue
            for num in range(len(suit)):
                if suit[num] == 0:
                    continue
                else:
                    string += str(num+1)*suit[num]

            string += dict[k]
            k+=1

        return string

    def discard(self, drawnTile: str): #Eventually will be filled with a method to select a discard, then return new hand and the discard tile

        print()
        print("Current Hand")
        print(self.format_hand(self._hand))
        print()

        self._hand.append(drawnTile) #append 14th tile to hand

        print("Draw Tile: ", drawnTile)
        print(self.format_hand(self._hand))
        print()

        discardPossibilities = []
        for i in range(len(self._hand)): 

            tempHand = self._hand[:i] + self._hand[i+1:]

            tempScore = self.format_hand(tempHand)
            discardPossibilities.append((self._hand[i] , tempScore))  
        
        discardPossibilities.sort(key=lambda x: (x[1]["shanten"], -x[1]["tileEff"]))
        
        # Commented out the discard analysis
        # for item in discardPossibilities:
        #     print(item)
        #     print()

        discardTile = discardPossibilities[0][0]

        self._hand.remove(discardTile)
        
        print("Post discard")
        print(self.format_hand(self._hand))
        print()

        return (discardTile)

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
        
        for i in hand:
            for item in handDict:
                if item in i:
                    if item in ["char", "circ", "bamb"]:

                        
                                
                        handDict[item].append((i.split("_")[0]))
                        handDict[item].sort()

                        handArray[suitsDict[item]][int(i[0]) - 1] += 1

                    else:
                        handDict[item] +=1
                        
                        handArray[3][honorsDict[item]] +=1

        handScore = {
            "displayHand" : handDict,
            "webFormat" : self.webFormat(handArray),
            "shanten" : self.calcShanten(handArray),
            "tileEff" : self.calcTileEff(handArray)
        }

        return handScore

    def calcShanten(self, handArray):

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
        
<<<<<<< Updated upstream

        def splits_nogroups(hand):
            set_insequences = incomplete_sequences(hand)
            current_shan=0
            set_pairs = pairs(hand)
            pair_bool = False

            for i in set_pairs:
                pair_bool = True
                current = splits_nogroups(resulting_hand(hand, i))[0]+1
=======
        def splits_nogroups(handArray):
            set_insequences = incomplete_sequences(handArray)
            current_shan=0
            set_pairs = pairs(handArray)

            for i in set_insequences:
                current = splits_nogroups(resulting_hand(handArray, i))+1
                if current > current_shan:
                    current_shan = current

            for i in set_pairs:
                current = splits_nogroups(resulting_hand(handArray, i))+1
>>>>>>> Stashed changes
                if current>current_shan:
                    current_shan = current

            for i in set_insequences:
                current = splits_nogroups(resulting_hand(hand, i))[0]+1
                if current > current_shan:
                    current_shan = current
                    pair_bool = False

            return current_shan, pair_bool


        def splits(g, handArray):          #******
            current_g_n = g
<<<<<<< Updated upstream
            current_i_n = 0 
            pair_presance = False                            
            set_pairs = pairs(hand)
            set_seq = complete_sequences(hand)
            set_triplets = triplets(hand)

            if len(set_seq) == 0  and len(set_triplets) == 0:
                return g, splits_nogroups(hand)[0], splits_nogroups(hand)[1]
=======
            current_i_n = 0                             
            set_pairs = pairs(handArray)
            set_seq = complete_sequences(handArray)
            set_triplets = triplets(handArray)

            if len(set_seq) == 0  and len(set_triplets) == 0:
                return g, splits_nogroups(handArray)

>>>>>>> Stashed changes

            for j in set_seq:
                current = splits(g+1, resulting_hand(handArray, j))[0]
                if current>current_g_n:
                    current_g_n = current
<<<<<<< Updated upstream
                    current_i_n = splits(g+1,resulting_hand(hand, j))[1]
                    pair_presance = splits(g+1,resulting_hand(hand, j))[2] #*
                elif current == current_g_n:
                    if splits(g+1,resulting_hand(hand, j))[1] > current_i_n:
                        current_i_n = splits(g+1,resulting_hand(hand, j))[1]
                        pair_presance = splits(g+1,resulting_hand(hand, j))[2] #*
=======
                    current_i_n = splits(g+1,resulting_hand(handArray, j))[1]
                elif current == current_g_n:
                    if splits(g+1,resulting_hand(handArray, j))[1] > current_i_n:
                        current_i_n = splits(g+1,resulting_hand(handArray, j))[1]

>>>>>>> Stashed changes

            for j in set_triplets:
                current = splits(g+1,resulting_hand(handArray, j))[0]
                if current>current_g_n:
                    current_g_n = current
<<<<<<< Updated upstream
                    current_i_n = splits(g+1,resulting_hand(hand, j))[1]
                    pair_presance = splits(g+1,resulting_hand(hand, j))[2] #*
                elif current == current_g_n:
                    if splits(g+1,resulting_hand(hand, j))[1] > current_i_n:
                        current_i_n = splits(g+1,resulting_hand(hand, j))[1]
                        pair_presance = splits(g+1,resulting_hand(hand, j))[2] #*

            return current_g_n,current_i_n,pair_presance
        

        def splits_fullhand(hand):
            current_split = [0,0,False]
            for i in hand[:3]:
                current_arr = splits(0, i)
                current_split[0] += current_arr[0]
                current_split[1] += current_arr[1]
                if current_arr[2] == True:
                    current_split[2] = True

            for i in hand[3]:
=======
                    current_i_n = splits(g+1,resulting_hand(handArray, j))[1]
                elif current == current_g_n:
                    if splits(g+1,resulting_hand(handArray, j))[1] > current_i_n:
                        current_i_n = splits(g+1,resulting_hand(handArray, j))[1]
            return current_g_n, current_i_n
    
        def splits_fullhand(handArray):
            current_split = [0,0]
            for i in handArray[:3]:
                current_split[0] += splits(0, i)[0]
                current_split[1] += splits(0, i)[1]
            for i in handArray[3]:
>>>>>>> Stashed changes
                if i == 3:
                    current_split[0] += 1
                elif i == 2:
                    current_split[1] +=1
            return current_split

<<<<<<< Updated upstream

        def shanten(hand):
            split_arr = splits_fullhand(hand)
=======
        def shanten(handArray):
            split_arr = splits_fullhand(handArray)
>>>>>>> Stashed changes
            i = split_arr[1]
            g = split_arr[0]
            pair_presence = split_arr[2]

            #checking for the edge case:
            if g == 3 and pair_presence == False:
                return 1
            return 8 - 2*g - min(i, 4-g) - min(1, max(0,i-4+g))
        
<<<<<<< Updated upstream

        return shanten(hand)
    


    def calcTileEff(self, hand):
=======
        return shanten(handArray)
    

    def calcTileEff(self, handArray):
>>>>>>> Stashed changes
        return random.randint(1,30)